"""Corpus local de fichas originales, validadas con metadatos trazables."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from urllib.parse import urlparse

ALLOWED_HOSTS = {
    "www.nibib.nih.gov",
    "www.fda.gov",
    "www.acr.org",
    "medlineplus.gov",
    "www.radiologyinfo.org",
    "www.radiologyresource.org",
    "www.medlineplus.gov",
    "openstax.org",
    "pmc.ncbi.nlm.nih.gov",
}


def default_root() -> Path:
    return Path(__file__).resolve().parents[2]


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load_corpus(root: Path | None = None) -> tuple[list[dict], dict[str, dict]]:
    root = root or default_root()
    lines = (root / "corpus/cards.jsonl").read_text(encoding="utf-8").splitlines()
    cards = [json.loads(line) for line in lines if line.strip()]
    items = json.loads((root / "corpus/sources.json").read_text(encoding="utf-8"))
    sources = {s["id"]: s for s in items}
    if len(sources) != len(items):
        raise ValueError("Identificadores duplicados de fuente")
    ids = set()
    for sid, source in sources.items():
        parsed = urlparse(source["url"])
        if parsed.scheme != "https" or parsed.hostname not in ALLOWED_HOSTS:
            raise ValueError(f"Host o esquema no autorizado: {sid}")
    for card in cards:
        if card["id"] in ids:
            raise ValueError(f"Ficha duplicada: {card['id']}")
        ids.add(card["id"])
        if not card["text"].strip() or len(card["text"]) > 7000:
            raise ValueError(f"Contenido inválido: {card['id']}")
        if not card["source_ids"] or any(s not in sources for s in card["source_ids"]):
            raise ValueError(f"Proveniencia inválida: {card['id']}")
        if card["authored"] != "original_spanish_summary":
            raise ValueError(f"Ficha no autorizada para indexar: {card['id']}")
    return cards, sources


def verify_manifest(root: Path | None = None) -> dict[str, bool]:
    root = root or default_root()
    manifest = json.loads((root / "corpus/manifest.json").read_text(encoding="utf-8"))
    out = {}
    for name, expected in manifest["sha256"].items():
        target = root / name
        out[name] = target.is_file() and sha256_bytes(target.read_bytes()) == expected
    return out
