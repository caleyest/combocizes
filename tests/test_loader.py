import pytest

from combocizes.loader import load_exercises

_EXERCISE_FILE_TEMPLATE = """
from combocizes.schema import Exercise, PrimaryCue

EXERCISE = Exercise(
    name={name!r},
    movement_pattern="pull",
    body_region="upper",
    muscle_group="biceps",
    body_position="standing_narrow",
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

    assert set(pool) == {"reverse_lunge", "hammer_curl"}
    assert pool["reverse_lunge"].name == "reverse_lunge"


def test_load_exercises_rejects_duplicate_names(tmp_path) -> None:
    (tmp_path / "a.py").write_text(_EXERCISE_FILE_TEMPLATE.format(name="same_name"))
    (tmp_path / "b.py").write_text(_EXERCISE_FILE_TEMPLATE.format(name="same_name"))

    with pytest.raises(ValueError, match="duplicate exercise name"):
        load_exercises(tmp_path)
