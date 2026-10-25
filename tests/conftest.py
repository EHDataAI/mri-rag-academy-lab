from pathlib import Path

import pytest

from mri_rag.retrieval import build_index


@pytest.fixture
def corpus_root() -> Path:
    return Path(__file__).resolve().parents[1]


@pytest.fixture
def temp_index(tmp_path: Path, corpus_root: Path) -> Path:
    index = tmp_path / "idx.sqlite3"
    build_index(corpus_root, index)
    return index
