import random

import pytest

from combocizes.class_template import build_class
from combocizes.constants import (
    ABS_MUSCLE_GROUPS,
    ARMS_MUSCLE_GROUPS,
    HEAVY_BAND,
    HEAVY_DUMBBELLS,
    LEGS_MUSCLE_GROUPS,
    LIGHT_BAND,
    LIGHT_DUMBBELLS,
    NO_EQUIPMENT,
)
from combocizes.schema import equipment_combo_key

_ALL_EQUIPMENT_OPTIONS = [
    dict(NO_EQUIPMENT),
    dict(HEAVY_DUMBBELLS),
    dict(LIGHT_DUMBBELLS),
    dict(HEAVY_BAND),
    dict(LIGHT_BAND),
]


@pytest.fixture
def full_pool(make_exercise):
    """A pool with generous coverage for every build_class segment kind.

    Every exercise supports all five equipment combos, so any equipment
    assignment the class-template makes finds enough candidates regardless
    of which combo lands where.
    """
    pool = {}

    for i in range(20):
        pool[f"full_{i}"] = make_exercise(
            name=f"full_{i}", body_region="full", equipment_options=_ALL_EQUIPMENT_OPTIONS
        )
    for group in ARMS_MUSCLE_GROUPS:
        for i in range(15):
            name = f"arms_{group}_{i}"
            pool[name] = make_exercise(
                name=name, muscle_group=group, equipment_options=_ALL_EQUIPMENT_OPTIONS
            )
    for group in LEGS_MUSCLE_GROUPS:
        for i in range(15):
            name = f"legs_{group}_{i}"
            pool[name] = make_exercise(
                name=name, muscle_group=group, equipment_options=_ALL_EQUIPMENT_OPTIONS
            )
    for group in ABS_MUSCLE_GROUPS:
        for i in range(15):
            name = f"abs_{group}_{i}"
            pool[name] = make_exercise(
                name=name, muscle_group=group, equipment_options=_ALL_EQUIPMENT_OPTIONS
            )
    for impact in ["high", "low"]:
        for i in range(20):
            name = f"plyo_{impact}_{i}"
            pool[name] = make_exercise(
                name=name,
                movement_pattern="plyo",
                impact=impact,
                equipment_options=_ALL_EQUIPMENT_OPTIONS,
            )

    return pool


def test_build_class_starts_with_warmup_and_ends_with_cooldown(full_pool) -> None:
    segments = build_class(full_pool, minutes=60, rng=random.Random(0))

    assert segments[0].kind == "warmup"
    assert segments[-1].kind == "cooldown"


def test_build_class_never_has_two_adjacent_plyo_segments(full_pool) -> None:
    for seed in range(10):
        segments = build_class(full_pool, minutes=60, rng=random.Random(seed))
        kinds = [s.kind for s in segments]
        for a, b in zip(kinds, kinds[1:], strict=False):
            assert not (a == "plyo" and b == "plyo")


def test_build_class_never_puts_plyo_right_before_cooldown(full_pool) -> None:
    for seed in range(10):
        segments = build_class(full_pool, minutes=60, rng=random.Random(seed))
        assert segments[-2].kind != "plyo"


def test_build_class_warmup_and_cooldown_use_no_equipment(full_pool) -> None:
    segments = build_class(full_pool, minutes=60, rng=random.Random(0))

    assert segments[0].selection.equipment == {}
    assert segments[-1].selection.equipment == {}


def test_build_class_guarantees_equipment_coverage(full_pool) -> None:
    segments = build_class(full_pool, minutes=60, rng=random.Random(0))

    used_keys = {equipment_combo_key(s.selection.equipment) for s in segments}
    assert equipment_combo_key(dict(HEAVY_DUMBBELLS)) in used_keys
    assert equipment_combo_key(dict(LIGHT_DUMBBELLS)) in used_keys
    assert (
        equipment_combo_key(dict(HEAVY_BAND)) in used_keys
        or equipment_combo_key(dict(LIGHT_BAND)) in used_keys
    )


def test_build_class_raises_when_minutes_too_short(full_pool) -> None:
    with pytest.raises(ValueError, match="too short to fit the fixed segments"):
        build_class(full_pool, minutes=10, rng=random.Random(0))
