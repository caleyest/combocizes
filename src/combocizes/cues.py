"""Refinement cues: reusable, exercise-tagged coaching lines.

Cues are grouped into category files under `data/cues/` (e.g. `upper.py`,
`lower.py`) for browsability, each exposing a flat `list[RefinementCue]`.
`build_cue_bank` merges every category file into one list. It isn't built
eagerly at import time: a cue's `exercise_ids` can only be cross-checked once
the exercise pool exists, and that pool isn't assembled until
`combocizes.loader.load_exercises` runs — so `build_cue_bank` is called from
there instead, as a local variable, not a module-level constant here.
"""

import importlib.util
from dataclasses import dataclass, field
from pathlib import Path

from combocizes.utils import DATA_DIR


@dataclass
class RefinementCue:
    """A single reusable refinement cue.

    Args:
        text: The cue as spoken to the class.
        exercise_ids: Names of the exercises this cue applies to. May be
            empty while a cue is still being authored. Not validated here —
            the exercise pool doesn't exist yet at cue-construction time —
            but cross-checked against it in `combocizes.loader.load_exercises`.
    """

    text: str
    exercise_ids: list[str] = field(default_factory=list)


def _load_cue_category(path: Path) -> list[RefinementCue]:
    """Dynamically import one `data/cues/*.py` file and return its cue list.

    Args:
        path: Path to the category file, imported dynamically via `importlib.util`.

    Returns:
        The single `list[RefinementCue]` the file exposes as a module-level
        variable.

    Raises:
        ValueError: If the file exposes zero or more than one such list.
    """
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    candidates = [
        value
        for value in vars(module).values()
        if isinstance(value, list) and all(isinstance(v, RefinementCue) for v in value)
    ]
    if len(candidates) != 1:
        raise ValueError(
            f"{path} must expose exactly one list[RefinementCue], found {len(candidates)}"
        )
    return candidates[0]


def build_cue_bank(cues_dir: Path | None = None) -> list[RefinementCue]:
    """Glob and merge every category file in `cues_dir` into one cue list.

    Args:
        cues_dir: Directory of category files. Defaults to `data/cues/`.

    Returns:
        Every cue across all category files.
    """
    cues_dir = cues_dir or (DATA_DIR / "cues")
    return [cue for path in sorted(cues_dir.glob("*.py")) for cue in _load_cue_category(path)]
