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
    LOW_BODY_POSITIONS,
    NO_EQUIPMENT,
)
from combocizes.schema import BodyPosition, equipment_combo_key

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


def test_build_class_never_assigns_heavy_dumbbells_to_plyo(full_pool) -> None:
    # full_pool's plyo exercises do support heavy_dumbbells (like every
    # other combo) -- this checks build_class's own assignment logic keeps
    # heavy dumbbells away from plyo regardless, not that the pool lacks it.
    for seed in range(20):
        segments = build_class(full_pool, minutes=60, rng=random.Random(seed))
        for segment in segments:
            if segment.kind == "plyo":
                assert equipment_combo_key(segment.selection.equipment) != equipment_combo_key(
                    dict(HEAVY_DUMBBELLS)
                )


def test_build_class_raises_when_minutes_too_short(full_pool) -> None:
    with pytest.raises(ValueError, match="too short to fit the fixed segments"):
        build_class(full_pool, minutes=10, rng=random.Random(0))


@pytest.fixture
def pool_with_low_ending_options(make_exercise):
    """A pool where every non-plyo segment kind can only end low.

    Every exercise a focus song or full-body stretch could draw holds a
    single `LOW_BODY_POSITIONS` stance — deliberately no standing
    alternative — so every non-plyo segment's own selection is guaranteed
    to end low regardless of `select_combo`'s own randomness. That isolates
    the pre-cooldown ordering rule itself (DESIGN.md section 4/7: does
    `build_class` correctly place a low-ending segment last and read its
    actual recorded ending position) from `select_combo`'s independent,
    already-covered chaining behavior.
    """
    pool = {}
    low_position = next(iter(LOW_BODY_POSITIONS))
    muscle_groups = [*ARMS_MUSCLE_GROUPS, *LEGS_MUSCLE_GROUPS, *ABS_MUSCLE_GROUPS]

    for group in muscle_groups:
        for i in range(10):
            pool[f"low_{group}_{i}"] = make_exercise(
                name=f"low_{group}_{i}",
                muscle_group=group,
                body_region="full",
                body_positions=[BodyPosition.held(low_position)],
                equipment_options=_ALL_EQUIPMENT_OPTIONS,
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


def test_build_class_ends_pre_cooldown_segment_low_when_the_pool_allows_it(
    pool_with_low_ending_options,
) -> None:
    for seed in range(10):
        segments = build_class(pool_with_low_ending_options, minutes=60, rng=random.Random(seed))
        pre_cooldown = segments[-2]

        assert pre_cooldown.selection.body_positions
        assert pre_cooldown.selection.body_positions[-1].end in LOW_BODY_POSITIONS
