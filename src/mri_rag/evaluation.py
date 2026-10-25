"""Benchmark de recuperación; sin falsas métricas generativas."""

from __future__ import annotations

import json
from pathlib import Path

from .corpus import default_root
from .retrieval import search_sparse


def evaluate(*, root: Path | None = None, split: str = "test", k: int = 3) -> dict:
    root = root or default_root()
    if split not in {"dev", "test", "all"}:
        raise ValueError("split debe ser dev, test o all")
    if k < 1 or k > 8:
        raise ValueError("k debe estar entre 1 y 8")
    cases = [
        json.loads(line)
        for line in (root / "eval/questions.jsonl").read_text(encoding="utf-8").splitlines()
    ]
    cases = [c for c in cases if split == "all" or c["split"] == split]
    positives = [c for c in cases if c["gold_id"] is not None]
    negatives = [c for c in cases if c["gold_id"] is None]
    hits = 0
    reciprocal = 0.0
    abstentions = 0
    results = []
    for c in cases:
        returned = search_sparse(c["question"], root=root, limit=k)
        ids = [hit["id"] for hit in returned]
        if c["gold_id"]:
            found = c["gold_id"] in ids
            hits += int(found)
            if found:
                reciprocal += 1 / (ids.index(c["gold_id"]) + 1)
        else:
            abstentions += int(not ids)
        results.append(
            {
                "id": c["id"],
                "gold": c["gold_id"],
                "retrieved": ids,
                "hit": c["gold_id"] in ids if c["gold_id"] else not ids,
            }
        )
    return {
        "split": split,
        "k": k,
        "n": len(cases),
        "n_answerable": len(positives),
        "n_ood": len(negatives),
        "hit_at_k": round(hits / len(positives), 4) if positives else None,
        "mrr_at_k": round(reciprocal / len(positives), 4) if positives else None,
        "ood_abstention_rate": round(abstentions / len(negatives), 4) if negatives else None,
        "cases": results,
        "limitations": "Muestra pequeña y redactada por los autores; no mide exactitud clínica ni fidelidad generativa.",
    }
