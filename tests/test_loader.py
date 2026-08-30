import pytest

from combocizes.cues import RefinementCue
from combocizes.loader import load_exercises

_EXERCISE_FILE_TEMPLATE = """
from combocizes.schema import Exercise, PrimaryCue

EXERCISE = Exercise(
    name={name!r},
    movement_pattern="pull",
    body_region="upper",
    muscle_group="biceps",
    body_positions=["standing_narrow"],
    unilateral=False,
    impact="low",
    equipment_options=[{{}}],
    mover="arm",
    mover_position_start="at_sides",
    mover_position_end="bent",
    primary_cue=PrimaryCue(
        breath="Exhale", action="curl", action_pool_key="curl_up", direction="up"
    ),
)
"""


def test_load_exercises_returns_the_example_pool() -> None:
    pool = load_exercises()

    # Not an exact-set check: data/exercises/ grows as exercises are authored.
    assert {"reverse_lunge", "hammer_curl"} <= set(pool)
    assert pool["reverse_lunge"].name == "reverse_lunge"


def test_load_exercises_rejects_duplicate_names(tmp_path) -> None:
    (tmp_path / "a.py").write_text(_EXERCISE_FILE_TEMPLATE.format(name="same_name"))
    (tmp_path / "b.py").write_text(_EXERCISE_FILE_TEMPLATE.format(name="same_name"))

    with pytest.raises(ValueError, match="duplicate exercise name"):
        load_exercises(tmp_path)


def test_load_exercises_rejects_cue_with_unknown_exercise_id(tmp_path) -> None:
    (tmp_path / "a.py").write_text(_EXERCISE_FILE_TEMPLATE.format(name="hammer_curl"))
    cue_bank = [RefinementCue(text="...", exercise_ids=["not_a_real_exercise"])]

    with pytest.raises(ValueError, match="unknown exercise_ids"):
        load_exercises(tmp_path, cue_bank=cue_bank)


def test_load_exercises_accepts_cue_with_known_exercise_id(tmp_path) -> None:
    (tmp_path / "a.py").write_text(_EXERCISE_FILE_TEMPLATE.format(name="hammer_curl"))
    cue_bank = [RefinementCue(text="...", exercise_ids=["hammer_curl"])]

    pool = load_exercises(tmp_path, cue_bank=cue_bank)

    assert "hammer_curl" in pool
