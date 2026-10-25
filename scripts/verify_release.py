"""Preflight offline del artefacto listo para auditoría."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from mri_rag.corpus import load_corpus, verify_manifest  # noqa: E402

cards, sources = load_corpus(ROOT)
checks = verify_manifest(ROOT)
print(
    json.dumps(
        {
            "cards": len(cards),
            "sources": len(sources),
            "hash_ok": all(checks.values()),
            "sha256_results": checks,
        },
        indent=2,
    )
)
raise SystemExit(0 if all(checks.values()) else 1)
