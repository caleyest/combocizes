import random

import pytest

from combocizes.combo_selector import exercise_count_for_duration, select_combo
from combocizes.constants import SECONDS_PER_EXERCISE


def test_exercise_count_for_duration_basic_math() -> None:
    minutes = (SECONDS_PER_EXERCISE * 4) / 60
    assert exercise_count_for_duration(minutes) == 4


def test_exercise_count_for_duration_floors_at_one() -> None:
    assert exercise_count_for_duration(0.001) == 1


def test_select_combo_filters_by_equipment(make_exercise) -> None:
    pool = {
        "a": make_exercise(name="a", equipment_options=[{"heavy_dumbbells": True}]),
        "b": make_exercise(name="b", equipment_options=[{"heavy_band": True}]),
    }

    selection = select_combo(pool, {"heavy_dumbbells": True}, count=1)

    assert selection.exercises == [pool["a"]]
    assert selection.equipment == {"heavy_dumbbells": True}


def test_select_combo_applies_pool_filter(make_exercise) -> None:
    pool = {
        "a": make_exercise(name="a", muscle_group="biceps"),
        "b": make_exercise(name="b", muscle_group="triceps"),
    }

    selection = select_combo(
        pool, {"heavy_dumbbells": True}, count=1, pool_filter=lambda e: e.muscle_group == "triceps"
    )

    assert selection.exercises == [pool["b"]]


def test_select_combo_raises_when_pool_too_small(make_exercise) -> None:
    pool = {"a": make_exercise(name="a")}

    with pytest.raises(ValueError, match="only 1 eligible"):
        select_combo(pool, {"heavy_dumbbells": True}, count=2)


def test_select_combo_prefers_chaining_over_variety(make_exercise) -> None:
    first = make_exercise(
        name="first",
        movement_pattern="pull",
        mover="equipment",
        mover_position_start="hanging_palms_in",
        mover_position_end="shoulder",
    )
    chains = make_exercise(
        name="chains",
        movement_pattern="pull",
        mover="equipment",
        mover_position_start="shoulder",
        mover_position_end="overhead",
    )
    would_win_on_variety = make_exercise(
        name="would_win_on_variety",
        movement_pattern="push",
        mover="equipment",
        mover_position_start="racked",
        mover_position_end="overhead",
    )
    pool = {e.name: e for e in [first, chains, would_win_on_variety]}
    rng = random.Random(0)

    selection = select_combo(pool, {"heavy_dumbbells": True}, count=2, rng=rng)

    if selection.exercises[0].name == "first":
        # "chains" must win the second slot even though "would_win_on_variety"
        # has a less-used movement_pattern, since chaining is primary.
        assert selection.exercises[1].name == "chains"


def test_select_combo_falls_back_to_variety_when_nothing_chains(make_exercise) -> None:
    first = make_exercise(
        name="first",
        movement_pattern="pull",
        mover="equipment",
        mover_position_start="hanging_palms_in",
        mover_position_end="shoulder",
    )
    no_chain_a = make_exercise(
        name="no_chain_a",
        movement_pattern="pull",
        mover="equipment",
        mover_position_start="racked",
        mover_position_end="racked",
    )
    no_chain_b = make_exercise(
        name="no_chain_b",
        movement_pattern="push",
        mover="equipment",
        mover_position_start="racked",
        mover_position_end="racked",
    )
    pool = {e.name: e for e in [first, no_chain_a, no_chain_b]}
    rng = random.Random(0)

    selection = select_combo(pool, {"heavy_dumbbells": True}, count=2, rng=rng)

    if selection.exercises[0].name == "first":
        # Neither remaining candidate chains from "first" (its
        # mover_position_end "shoulder" matches neither's start), so variety
        # picks the exercise whose pattern ("push") hasn't been used yet.
        assert selection.exercises[1].name == "no_chain_b"


def test_select_combo_maximizes_pattern_variety_with_no_chaining_signal(make_exercise) -> None:
    pool = {}
    for pattern in ["push", "pull", "hinge", "squat"]:
        for i in range(3):
            name = f"{pattern}_{i}"
            pool[name] = make_exercise(
                name=name,
                movement_pattern=pattern,
                mover="equipment",
                mover_position_start="racked",
                mover_position_end="racked",
            )
    rng = random.Random(42)

    selection = select_combo(pool, {"heavy_dumbbells": True}, count=8, rng=rng)

    usage: dict[str, int] = {}
    for exercise in selection.exercises:
        usage[exercise.movement_pattern] = usage.get(exercise.movement_pattern, 0) + 1

    assert max(usage.values()) - min(usage.values()) <= 1
