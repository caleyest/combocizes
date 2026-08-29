"""Shared helpers: project paths and logging setup."""

import logging
from pathlib import Path

# src/combocizes/utils.py -> src/combocizes -> src -> repo root
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"
OUTPUT_DIR = PROJECT_ROOT / "output"


def get_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    """Return a logger that prints to stderr, configuring it once."""
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)-8s %(name)s: %(message)s"))
        logger.addHandler(handler)
        logger.setLevel(level)
    return logger


def ensure_dir(path: Path) -> Path:
    """Create `path` (and parents) if absent, then return it."""
    path.mkdir(parents=True, exist_ok=True)
    return path
