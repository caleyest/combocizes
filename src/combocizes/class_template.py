"""Assembles a full class: segment timing, ordering, and equipment.

See DESIGN.md section 4. Builds on `combocizes.combo_selector`'s per-segment
selection functions — this module decides how many segments of each kind
exist, how long each is, what order they go in, and which equipment combo
each one uses. No CLI or rendering here; `build_class` returns structured
data.
"""

import random
from dataclasses import dataclass

from combocizes.combo_selector import (
    ComboSelection,
    exercise_count_for_duration,
    select_combo,
    select_plyo_burst,
)
from combocizes.constants import (
    ABS_MINUTES,
    ABS_MUSCLE_GROUPS,
    ARMS_MINUTES,
    ARMS_MUSCLE_GROUPS,
    COOLDOWN_MINUTES,
    EQUIPMENT_CHOICES,
    FIXED_SEGMENT_MINUTES,
    FULL_BODY_STRETCH_TARGET_MINUTES,
    HEAVY_BAND,
    HEAVY_DUMBBELLS,
    LEGS_MINUTES,
    LEGS_MUSCLE_GROUPS,
    LIGHT_BAND,
    LIGHT_DUMBBELLS,
    MIN_PLYO_BURST_EXERCISES,
    NO_EQUIPMENT,
    PLYO_TOTAL_MINUTES,
    WARMUP_MINUTES,
)
from combocizes.schema import EquipmentCombo, Exercise


@dataclass
class ClassSegment:
    """One segment of a built class.

    Args:
        kind: `"warmup"`, `"plyo"`, `"arms"`, `"legs"`, `"abs"`,
            `"full_body"`, or `"cooldown"`.
        selection: The exercises and equipment combo for this segment.
        duration_minutes: This segment's share of the class's time budget.
    """

    kind: str
    selection: ComboSelection
    duration_minutes: float


def _select_for_kind(
    pool: dict[str, Exercise],
    kind: str,
    equipment: EquipmentCombo,
    count: int,
    rng: random.Random,
) -> ComboSelection:
    """Dispatch to the right selection function/pool_filter for `kind`."""
    if kind == "plyo":
        return select_plyo_burst(pool, equipment, max(count, MIN_PLYO_BURST_EXERCISES), rng=rng)
    if kind == "arms":
        return select_combo(
            pool,
            equipment,
            count,
            pool_filter=lambda e: e.muscle_group in ARMS_MUSCLE_GROUPS,
            rng=rng,
        )
    if kind == "legs":
        return select_combo(
            pool,
            equipment,
            count,
            pool_filter=lambda e: e.muscle_group in LEGS_MUSCLE_GROUPS,
            rng=rng,
        )
    if kind == "abs":
        return select_combo(
            pool,
            equipment,
            count,
            pool_filter=lambda e: e.muscle_group in ABS_MUSCLE_GROUPS,
            rng=rng,
        )
    return select_combo(pool, equipment, count, rng=rng)  # "full_body"


def build_class(
    pool: dict[str, Exercise],
    minutes: float,
    rng: random.Random | None = None,
) -> list[ClassSegment]:
    """Assemble a full class: warmup, a shuffled/plyo-interspersed middle, cooldown.

    Args:
        pool: The exercise pool to select from, e.g. from
            `combocizes.loader.load_exercises`.
        minutes: Total class length.
        rng: Source of randomness for every random choice this makes
            (burst count, ordering, equipment assignment, and each
            segment's own selection). Defaults to a fresh `random.Random()`.

    Returns:
        Segments in class order: `warmup`, then a middle stretch mixing
        plyo bursts, `arms`, `legs`, `abs`, and full-body-combo stretches,
        then `cooldown`.

        Ordering guarantees: no two plyo bursts are ever adjacent, and the
        segment immediately before cooldown is never a plyo burst.
        Everything else (focus songs, full-body-combo stretches, and plyo
        next to any of those) may appear in any order, including back to
        back — e.g. two full-body-combo songs in a row, useful for hitting
        a unilateral move on one side then the other.

        Equipment: warmup and cooldown always use no equipment. Every
        other segment is equipment-eligible; heavy dumbbells, light
        dumbbells, and band (either weight) are each guaranteed to be used
        by at least one segment.

    Raises:
        ValueError: If `minutes` is too short to fit the fixed-duration
            segments, or if `pool` doesn't have enough eligible exercises
            for some segment (propagated from
            `select_combo`/`select_plyo_burst`).
    """
    rng = rng or random.Random()

    full_body_total_minutes = minutes - FIXED_SEGMENT_MINUTES
    if full_body_total_minutes <= 0:
        raise ValueError(
            f"{minutes} minutes is too short to fit the fixed segments "
            f"({FIXED_SEGMENT_MINUTES} minutes)"
        )

    plyo_burst_count = rng.randint(3, 4)
    num_combo_stretches = max(1, round(full_body_total_minutes / FULL_BODY_STRETCH_TARGET_MINUTES))

    plyo_specs = [
        {"kind": "plyo", "duration": PLYO_TOTAL_MINUTES / plyo_burst_count}
        for _ in range(plyo_burst_count)
    ]
    non_plyo_specs = [
        {"kind": "arms", "duration": ARMS_MINUTES},
        {"kind": "legs", "duration": LEGS_MINUTES},
        {"kind": "abs", "duration": ABS_MINUTES},
        *(
            {"kind": "full_body", "duration": full_body_total_minutes / num_combo_stretches}
            for _ in range(num_combo_stretches)
        ),
    ]
    rng.shuffle(non_plyo_specs)

    num_non_plyo = len(non_plyo_specs)
    if plyo_burst_count > num_non_plyo:
        raise ValueError(
            f"{plyo_burst_count} plyo bursts need at least that many non-plyo segments "
            f"to stay non-adjacent, only {num_non_plyo} available"
        )

    # K+1 gaps exist around K non-plyo items (before each, plus one at the
    # very end); excluding the final gap guarantees a plyo burst never
    # lands last, so the segment right before cooldown is never plyo.
    plyo_gaps = set(rng.sample(range(num_non_plyo), plyo_burst_count))
    plyo_iter = iter(plyo_specs)
    ordered_specs = []
    for i, spec in enumerate(non_plyo_specs):
        if i in plyo_gaps:
            ordered_specs.append(next(plyo_iter))
        ordered_specs.append(spec)

    # Equipment: guarantee heavy dumbbells, light dumbbells, and band each
    # appear at least once by assigning them to three distinct segments up
    # front; every other segment gets a random combo (bodyweight included).
    assignable = list(ordered_specs)
    rng.shuffle(assignable)
    band_combo = dict(rng.choice([HEAVY_BAND, LIGHT_BAND]))
    required_combos = [dict(HEAVY_DUMBBELLS), dict(LIGHT_DUMBBELLS), band_combo]
    for spec, combo in zip(assignable[:3], required_combos, strict=False):
        spec["equipment"] = combo
    for spec in assignable[3:]:
        spec["equipment"] = rng.choice(EQUIPMENT_CHOICES)

    no_equipment = dict(NO_EQUIPMENT)
    warmup = ClassSegment(
        kind="warmup",
        selection=select_combo(
            pool,
            no_equipment,
            exercise_count_for_duration(WARMUP_MINUTES),
            pool_filter=lambda e: e.body_region == "full",
            rng=rng,
        ),
        duration_minutes=WARMUP_MINUTES,
    )
    cooldown = ClassSegment(
        kind="cooldown",
        selection=select_combo(
            pool,
            no_equipment,
            exercise_count_for_duration(COOLDOWN_MINUTES),
            pool_filter=lambda e: e.body_region == "full",
            rng=rng,
        ),
        duration_minutes=COOLDOWN_MINUTES,
    )

    middle = [
        ClassSegment(
            kind=spec["kind"],
            selection=_select_for_kind(
                pool,
                spec["kind"],
                spec["equipment"],
                exercise_count_for_duration(spec["duration"]),
                rng,
            ),
            duration_minutes=spec["duration"],
        )
        for spec in ordered_specs
    ]

    return [warmup, *middle, cooldown]
