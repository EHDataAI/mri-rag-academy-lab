"""Respuesta extractiva por defecto; opcional Ollama con citas validadas."""

from __future__ import annotations

import json
from http.client import HTTPConnection, HTTPException
from urllib.parse import urlsplit

from .corpus import load_corpus
from .generation_guard import assess_generated_answer, build_grounded_prompt
from .retrieval import search_hybrid, search_sparse
from .security import checked_ollama_url, screen_question

NOTICE = "Material educativo, no diagnóstico ni autorización para procedimientos clínicos."


def _request_local_ollama(url: str, payload: bytes) -> dict:
    """Call only validated local Ollama; redirects are never followed."""
    safe = checked_ollama_url(url)
    parsed = urlsplit(safe)
    host = parsed.hostname
    if host is None:
        raise ValueError("Ollama host inválido")
    if host == "localhost":
        host = "127.0.0.1"

    connection = HTTPConnection(host, parsed.port or 11434, timeout=45)
    try:
        connection.request(
            "POST",
            "/api/generate",
            body=payload,
            headers={"Content-Type": "application/json", "Accept": "application/json"},
        )
        response = connection.getresponse()
        if response.status != 200:
            raise ValueError(f"Respuesta HTTP inesperada: {response.status}")
        max_bytes = 512 * 1024
        raw = response.read(max_bytes + 1)
        if len(raw) > max_bytes:
            raise ValueError("Respuesta Ollama demasiado grande")
        result = json.loads(raw)
        if not isinstance(result, dict):
            raise ValueError("Respuesta Ollama con formato inválido")
        return result
    finally:
        connection.close()


def ask(
    question: str,
    *,
    root=None,
    mode: str = "sparse",
    llm: str = "none",
    model: str = "qwen3:1.7b",
    ollama_url: str = "http://127.0.0.1:11434",
    top_k: int = 3,
) -> dict:
    good, why = screen_question(question)
    if not good:
        return {"status": "blocked", "answer": why, "citations": [], "hits": [], "notice": NOTICE}
    if mode not in {"sparse", "hybrid"} or llm not in {"none", "ollama"}:
        raise ValueError("Modo inválido")
    if top_k not in range(1, 9):
        raise ValueError("top_k debe estar entre 1 y 8")
    hits = (
        search_sparse(question, root, limit=top_k)
        if mode == "sparse"
        else search_hybrid(question, root, limit=top_k)
    )
    if not hits:
        return {
            "status": "insufficient_evidence",
            "answer": "No encuentro evidencia suficiente en el corpus local para responder. "
            "Reformule la pregunta o consulte las fuentes oficiales.",
            "citations": [],
            "hits": [],
            "notice": NOTICE,
        }
    _, sources = load_corpus(root)
    citations = []
    for i, h in enumerate(hits, 1):
        for sid in h["source_ids"]:
            source = sources[sid]
            citations.append(
                {
                    "ref": f"S{i}",
                    "card_id": h["id"],
                    "source_id": sid,
                    "title": source["title"],
                    "url": source["url"],
                    "rights": source["rights"],
                }
            )
    extractive = "\n\n".join(f"[S{i}] {h['title']}: {h['text']}" for i, h in enumerate(hits, 1))
    response = extractive
    engine_status = "extractive"
    if llm == "ollama":
        url = checked_ollama_url(ollama_url)
        prompt = build_grounded_prompt(question, hits)
        payload = json.dumps(
            {
                "model": model,
                "prompt": prompt,
                "stream": False,
                "options": {"temperature": 0, "num_predict": 300},
                "think": False,
            }
        ).encode()
        try:
            output = _request_local_ollama(url, payload)
            result = output.get("response")
            assessment = assess_generated_answer(result, hits)
            if assessment == "accepted":
                response = result.strip()
                engine_status = "ollama_verbatim_source_span_verified"
            elif assessment == "citation_invalid":
                engine_status = "ollama_citation_invalid_extractive_fallback"
            else:
                engine_status = "ollama_unverified_extractive_fallback"
        except (OSError, ValueError, KeyError, TimeoutError, HTTPException):
            engine_status = "ollama_unavailable_extractive_fallback"
    return {
        "status": "ok",
        "answer": response,
        "citations": citations,
        "hits": [
            {
                "id": x["id"],
                "title": x["title"],
                "module": x["module"],
                "coverage": x.get("term_coverage"),
                "rrf": x.get("rrf_score"),
            }
            for x in hits
        ],
        "engine_status": engine_status,
        "notice": NOTICE,
    }
