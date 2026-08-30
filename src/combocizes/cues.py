"""Shared refinement-cue bank.

`CUE_BANK` is built once, at import time, by merging every category file
under `data/cues/`. It must be populated before any `combocizes.schema.Exercise`
is constructed, since `Exercise.__post_init__` validates `refinement_cue_ids`
against it — including exercises instantiated at module-load time inside
`data/exercises/*.py` files. Importing `combocizes.cues` (directly, or via the
`CUE_BANK` reference in `combocizes.schema`) is what triggers that build.
"""

import importlib.util
from dataclasses import dataclass, field
from pathlib import Path

from combocizes.constants import BODY_REGIONS, MOVEMENT_PATTERNS, MUSCLE_GROUPS
from combocizes.utils import DATA_DIR

# Cue tags are code-driven, not picked from an authoring shortlist, so each
# key is restricted to one of combocizes's own existing vocabularies rather
# than free text.
_TAG_VOCAB = {
    "movement_pattern": MOVEMENT_PATTERNS,
    "region": BODY_REGIONS,
    "muscle_group": MUSCLE_GROUPS,
}


@dataclass
class RefinementCue:
    """A single reusable refinement cue.

    Args:
        text: The cue as spoken to the class.
        tags: Hints for finding this cue by category, e.g.
            `{"movement_pattern": ["pull"], "region": "upper"}`. Keys must be
            one of `movement_pattern`, `region`, `muscle_group`; values must
            be drawn from the matching constant in `combocizes.constants`.
            Never used to auto-inject cues at generation time.

    Raises:
        ValueError: If a tag key is unrecognized or a tag value isn't in
            that key's vocabulary.
    """

    text: str
    tags: dict[str, str | list[str]] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for key, value in self.tags.items():
            if key not in _TAG_VOCAB:
                raise ValueError(f"unknown cue tag key {key!r}, expected one of {list(_TAG_VOCAB)}")
            values = value if isinstance(value, list) else [value]
            invalid = [v for v in values if v not in _TAG_VOCAB[key]]
            if invalid:
                raise ValueError(
                    f"invalid {key!r} tag value(s) {invalid}, expected one of {_TAG_VOCAB[key]}"
                )


def _load_cue_category(path: Path) -> dict[str, RefinementCue]:
    """Dynamically import one `data/cues/*.py` file and return its cue dict.

    Args:
        path: Path to the category file, imported dynamically via `importlib.util`.

    Returns:
        The single `dict[str, RefinementCue]` the file exposes as a
        module-level variable.

    Raises:
        ValueError: If the file exposes zero or more than one such dict.
    """
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    candidates = [
        value
        for value in vars(module).values()
        if isinstance(value, dict) and all(isinstance(v, RefinementCue) for v in value.values())
    ]
    if len(candidates) != 1:
        raise ValueError(
            f"{path} must expose exactly one dict[str, RefinementCue], found {len(candidates)}"
        )
    return candidates[0]


def _build_cue_bank(cues_dir: Path | None = None) -> dict[str, RefinementCue]:
    """Glob and merge every category file in `cues_dir` into one cue bank.

    Args:
        cues_dir: Directory of category files. Defaults to `data/cues/`.

    Returns:
        Every cue, keyed by ID, across all category files.

    Raises:
        ValueError: If the same cue ID appears in more than one category file.
    """
    cues_dir = cues_dir or (DATA_DIR / "cues")
    bank: dict[str, RefinementCue] = {}
    for path in sorted(cues_dir.glob("*.py")):
        for cue_id, cue in _load_cue_category(path).items():
            if cue_id in bank:
                raise ValueError(f"duplicate cue id {cue_id!r} in {path}")
            bank[cue_id] = cue
    return bank


CUE_BANK = _build_cue_bank()
