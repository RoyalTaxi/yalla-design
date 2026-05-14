from __future__ import annotations
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TOKENS_DIR = ROOT / "tokens"
BUILD_DIR = ROOT / "build"
GENERATED_DIR = BUILD_DIR / "generated"

def get_default_projects_root() -> Path:
    return ROOT.parent
