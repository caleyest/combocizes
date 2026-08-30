"""Loads the exercise pool from `data/exercises/`.

Each file exposes one module-level `EXERCISE: Exercise` instance. Loading
globs the directory, dynamically imports every file, and combines the
results — cheap, and run once at startup rather than per-generation, per
DESIGN.md section 3.

Loading is also the point where `RefinementCue.exercise_ids` (see
`combocizes.cues`) gets built and validated: the cue bank isn't a module-level
constant, since a cue can't check its own exercise_ids against real exercise
names until the pool assembled here exists.
"""

import importlib.util
from pathlib import Path

from combocizes.cues import RefinementCue, build_cue_bank
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


def _validate_cue_exercise_ids(pool: dict[str, Exercise], cue_bank: list[RefinementCue]) -> None:
    """Cross-check every cue's `exercise_ids` against a loaded exercise pool.

    Args:
        pool: The loaded exercise pool, keyed by exercise name.
        cue_bank: The cues to validate.

    Raises:
        ValueError: If a cue's `exercise_ids` names an exercise not in `pool`.
    """
    for cue in cue_bank:
        unknown = [exercise_id for exercise_id in cue.exercise_ids if exercise_id not in pool]
        if unknown:
            raise ValueError(f"cue {cue.text!r} references unknown exercise_ids {unknown}")


def load_exercises(
    exercises_dir: Path | None = None,
    cue_bank: list[RefinementCue] | None = None,
) -> dict[str, Exercise]:
    """Glob and load every exercise file into one pool, keyed by name.

    Args:
        exercises_dir: Directory of exercise files. Defaults to `data/exercises/`.
        cue_bank: Cues to cross-validate `exercise_ids` against. Defaults to
            `combocizes.cues.build_cue_bank()`; overridable for tests.

    Returns:
        Every exercise, keyed by `Exercise.name`.

    Raises:
        ValueError: If two files declare the same exercise name, or a cue in
            `cue_bank` references an exercise name not in the pool.
    """
    exercises_dir = exercises_dir or (DATA_DIR / "exercises")
    cue_bank = build_cue_bank() if cue_bank is None else cue_bank
    pool: dict[str, Exercise] = {}
    for path in sorted(exercises_dir.glob("*.py")):
        exercise = _load_exercise_file(path)
        if exercise.name in pool:
            raise ValueError(f"duplicate exercise name {exercise.name!r} in {path}")
        pool[exercise.name] = exercise
    _validate_cue_exercise_ids(pool, cue_bank)
    return pool
