"""Loads the exercise pool from `data/exercises/`.

Each file exposes one module-level `EXERCISE: Exercise` instance. Loading
globs the directory, dynamically imports every file, and combines the
results — cheap, and run once at startup rather than per-generation, per
DESIGN.md section 3.
"""

import importlib.util
from pathlib import Path

from combocizes.schema import Exercise
from combocizes.utils import DATA_DIR


def _load_exercise_file(path: Path) -> Exercise:
    """Import one `data/exercises/*.py` file and return its exercise.

    Args:
        path: Path to the exercise file, imported dynamically via `importlib.util`.

    Returns:
        The module's `EXERCISE` attribute.

    Raises:
        AttributeError: If the file doesn't expose an `EXERCISE` attribute.
    """
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    if not hasattr(module, "EXERCISE"):
        raise AttributeError(f"{path} must expose a module-level EXERCISE")
    return module.EXERCISE


def load_exercises(exercises_dir: Path | None = None) -> dict[str, Exercise]:
    """Glob and load every exercise file into one pool, keyed by name.

    Args:
        exercises_dir: Directory of exercise files. Defaults to `data/exercises/`.

    Returns:
        Every exercise, keyed by `Exercise.name`.

    Raises:
        ValueError: If two files declare the same exercise name.
    """
    exercises_dir = exercises_dir or (DATA_DIR / "exercises")
    pool: dict[str, Exercise] = {}
    for path in sorted(exercises_dir.glob("*.py")):
        exercise = _load_exercise_file(path)
        if exercise.name in pool:
            raise ValueError(f"duplicate exercise name {exercise.name!r} in {path}")
        pool[exercise.name] = exercise
    return pool
