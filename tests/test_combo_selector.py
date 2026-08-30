import random

import pytest

from combocizes.combo_selector import (
    _impact_sequence,
    exercise_count_for_duration,
    select_combo,
    select_plyo_burst,
)
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


def test_select_plyo_burst_filters_to_plyo_movement_pattern(make_exercise) -> None:
    plyo = make_exercise(name="plyo1", movement_pattern="plyo", impact="high")
    not_plyo = make_exercise(name="not_plyo", movement_pattern="push", impact="high")
    pool = {"plyo1": plyo, "not_plyo": not_plyo}

    selection = select_plyo_burst(pool, {"heavy_dumbbells": True}, count=1)

    assert selection.exercises == [plyo]


def test_select_plyo_burst_raises_when_pool_too_small(make_exercise) -> None:
    pool = {"a": make_exercise(name="a", movement_pattern="plyo", impact="high")}

    with pytest.raises(ValueError, match="only 1 eligible"):
        select_plyo_burst(pool, {"heavy_dumbbells": True}, count=2)


def test_select_plyo_burst_raises_when_missing_an_impact_level(make_exercise) -> None:
    pool = {
        "a": make_exercise(name="a", movement_pattern="plyo", impact="high"),
        "b": make_exercise(name="b", movement_pattern="plyo", impact="high"),
    }

    with pytest.raises(ValueError, match="need both high- and low-impact"):
        select_plyo_burst(pool, {"heavy_dumbbells": True}, count=2)


def test_select_plyo_burst_follows_a_2_or_3_to_1_high_low_pattern(make_exercise) -> None:
    pool = {}
    for i in range(10):
        pool[f"high_{i}"] = make_exercise(name=f"high_{i}", movement_pattern="plyo", impact="high")
        pool[f"low_{i}"] = make_exercise(name=f"low_{i}", movement_pattern="plyo", impact="low")
    rng = random.Random(1)

    selection = select_plyo_burst(pool, {"heavy_dumbbells": True}, count=9, rng=rng)

    impacts = [e.impact for e in selection.exercises]
    assert impacts in (_impact_sequence(9, 2), _impact_sequence(9, 3))


def test_select_plyo_burst_prefers_mat_orientation_chaining(make_exercise) -> None:
    # count=2 is always ["high", "high"] regardless of the burst's internal
    # high:low ratio draw, so a lone low-impact filler keeps the "need both
    # impact levels" check satisfied without affecting which of these three
    # gets picked.
    filler_low = make_exercise(name="filler_low", movement_pattern="plyo", impact="low")
    first = make_exercise(
        name="first", movement_pattern="plyo", impact="high", mat_orientation_end="right"
    )
    chains = make_exercise(
        name="chains", movement_pattern="plyo", impact="high", mat_orientation_start="right"
    )
    would_lose = make_exercise(name="would_lose", movement_pattern="plyo", impact="high")
    pool = {e.name: e for e in [filler_low, first, chains, would_lose]}
    rng = random.Random(0)

    selection = select_plyo_burst(pool, {"heavy_dumbbells": True}, count=2, rng=rng)

    if selection.exercises[0].name == "first":
        assert selection.exercises[1].name == "chains"
