"""The parameterized combo-selection function.

See DESIGN.md section 5: one function — "select N exercises from a filtered
pool, chained by mover position and varied by movement pattern, fit to a
time budget" — reused for plyo bursts, focus songs, and full-body combos,
configured differently per segment (pool filter, exercise count, equipment).
"""

import random
from collections.abc import Callable
from dataclasses import dataclass, field

from combocizes.constants import BODY_POSITION_TIERS, SECONDS_PER_EXERCISE
from combocizes.schema import BodyPosition, EquipmentCombo, Exercise, equipment_combo_key

# The only banned direct stance-transition jump (DESIGN.md section 5): tier
# 1 (upright) <-> tier 3 (floor) skips the tier-2 bridge stance
# (kneeling/seated) either direction needs. Everything else is unrestricted.
_BANNED_TIER_JUMP = frozenset({1, 3})


def exercise_count_for_duration(minutes: float) -> int:
    """Convert a segment's minute budget into an exercise count.

    Args:
        minutes: The segment's time budget, in minutes.

    Returns:
        How many exercises fit that budget at `SECONDS_PER_EXERCISE` each,
        rounded down to at least 1.
    """
    return max(1, int(minutes * 60 // SECONDS_PER_EXERCISE))


@dataclass
class ComboSelection:
    """The result of one `select_combo` call — one song's worth of exercises.

    Args:
        exercises: The selected exercises, in order.
        equipment: The single equipment combo used for all of them.
        body_positions: The specific start/end `BodyPosition` pair recorded
            for each exercise in `exercises`, same order and length. Only
            populated by `select_combo` — `select_plyo_burst` doesn't chain
            on stance, so it leaves this empty.
    """

    exercises: list[Exercise]
    equipment: EquipmentCombo
    body_positions: list[BodyPosition] = field(default_factory=list)


def _filter_pool(
    pool: dict[str, Exercise],
    equipment: EquipmentCombo,
    pool_filter: Callable[[Exercise], bool] | None,
) -> list[Exercise]:
    """Narrow `pool` to exercises supporting `equipment`, then `pool_filter`.

    Args:
        pool: Candidate exercises.
        equipment: The equipment combo to require support for.
        pool_filter: Optional extra filter, applied after the equipment filter.

    Returns:
        The filtered exercises, in `pool`'s iteration order.
    """
    combo_key = equipment_combo_key(equipment)
    candidates = [
        exercise
        for exercise in pool.values()
        if combo_key in (equipment_combo_key(combo) for combo in exercise.equipment_options)
    ]
    if pool_filter is not None:
        candidates = [exercise for exercise in candidates if pool_filter(exercise)]
    return candidates


def _is_banned_tier_jump(start_tier: int, end_tier: int) -> bool:
    """Whether a direct transition between two stance tiers is disallowed."""
    return frozenset({start_tier, end_tier}) == _BANNED_TIER_JUMP


def _passes_stance_guardrail(exercise: Exercise, previous_end_tier: int) -> bool:
    """Whether `exercise` has any pair reachable from `previous_end_tier`."""
    return any(
        not _is_banned_tier_jump(BODY_POSITION_TIERS[pair.start], previous_end_tier)
        for pair in exercise.body_positions
    )


def _reaches_tier(exercise: Exercise, tier: int) -> bool:
    """Whether any of `exercise`'s pairs starts in stance tier `tier`."""
    return any(BODY_POSITION_TIERS[pair.start] == tier for pair in exercise.body_positions)


def _guardrail_compliant_pairs(exercise: Exercise, previous_end_tier: int) -> list[BodyPosition]:
    """`exercise`'s own pairs that don't require a banned tier jump.

    Falls back to all of `exercise`'s pairs if none are compliant, mirroring
    the pool-level guardrail's own "silently skip, don't fail the pick"
    fallback (DESIGN.md section 5).
    """
    compliant = [
        pair
        for pair in exercise.body_positions
        if not _is_banned_tier_jump(BODY_POSITION_TIERS[pair.start], previous_end_tier)
    ]
    return compliant or list(exercise.body_positions)


def select_combo(
    pool: dict[str, Exercise],
    equipment: EquipmentCombo,
    count: int,
    pool_filter: Callable[[Exercise], bool] | None = None,
    rng: random.Random | None = None,
) -> ComboSelection:
    """Select `count` exercises from `pool`, chained and movement-pattern varied.

    Args:
        pool: Candidate exercises, e.g. from `combocizes.loader.load_exercises`.
        equipment: The equipment combo this whole selection will use. Only
            exercises whose `equipment_options` includes this combo are
            eligible — one equipment combo per song, not per exercise.
        count: How many exercises to select.
        pool_filter: Optional extra filter (e.g. restrict to a muscle group
            for a focus song), applied after the equipment filter.
        rng: Source of randomness for tie-breaking. Defaults to a fresh
            `random.Random()`.

    Returns:
        The selection: `count` exercises and the equipment combo used.

        Each pick after the first is narrowed by a sequence of filters —
        see DESIGN.md section 5 for the full rationale, this is the short
        version:
        0. Stance-transition guardrail (legality): candidates that can only
           reach the previous pick's recorded end position via a banned
           tier jump (tier 1 upright <-> tier 3 floor) are excluded. If
           this would leave nothing, it's skipped for this one pick rather
           than failing the selection.
        0.5. Same-tier preference: among whatever step 0 left, candidates
           that can stay in the previous pick's own tier are preferred
           over ones that can only continue via a different (but legal)
           tier — crossing tiers is allowed, not free.
        1. Exact match: candidates with a `body_positions` pair whose
           `.start` equals the previous pick's recorded `.end` exactly —
           same specific stance, no transition needed. This is also what
           makes narrow/wide stances non-interchangeable even though both
           are tier 1 (the "plane" guardrail): they're just never equal.
        2. Among whichever candidates that leaves, one whose
           `mover_position_start` matches the previous pick's
           `mover_position_end` — in-song chaining.
        3. Among whichever candidates that leaves, the one whose
           `movement_pattern` has been used least so far in this
           selection; further ties break randomly via `rng`.
        Every step reset per call — scoped to one song, not the whole class.

        `ComboSelection.body_positions` records the one `BodyPosition` pair
        actually assumed for each pick, parallel to `exercises`. Choosing
        it mirrors the same legality -> same-tier -> exact-match ordering
        above, applied to the winning candidate's own pairs rather than the
        pool: a pair reachable from the previous pick's tier without a
        banned jump (falling back to all of the candidate's pairs if none
        qualify), preferring an exact `.start` match, then a same-tier
        match, then `rng.choice` among what's left. The first pick has no
        previous position to reach from, so it's always `rng.choice`d from
        its own pairs unrestricted.

    Raises:
        ValueError: If fewer than `count` exercises remain after filtering.
    """
    rng = rng or random.Random()
    candidates = _filter_pool(pool, equipment, pool_filter)

    if len(candidates) < count:
        raise ValueError(
            f"only {len(candidates)} eligible exercise(s) for equipment {equipment!r}, need {count}"
        )

    remaining = list(candidates)
    pattern_usage: dict[str, int] = {}
    selected: list[Exercise] = []
    selected_positions: list[BodyPosition] = []
    previous: Exercise | None = None
    previous_end: str | None = None

    for _ in range(count):
        eligible = remaining
        if previous is not None:
            previous_end_tier = BODY_POSITION_TIERS[previous_end]

            guardrail_ok = [e for e in remaining if _passes_stance_guardrail(e, previous_end_tier)]
            if guardrail_ok:
                eligible = guardrail_ok

            same_tier = [e for e in eligible if _reaches_tier(e, previous_end_tier)]
            if same_tier:
                eligible = same_tier

            exact_match = [
                e for e in eligible if any(pair.start == previous_end for pair in e.body_positions)
            ]
            if exact_match:
                eligible = exact_match

            chained = [e for e in eligible if e.mover_position_start == previous.mover_position_end]
            if chained:
                eligible = chained

        least_used = min(pattern_usage.get(e.movement_pattern, 0) for e in eligible)
        tied = [e for e in eligible if pattern_usage.get(e.movement_pattern, 0) == least_used]
        choice = rng.choice(tied)

        if previous is None:
            position = rng.choice(choice.body_positions)
        else:
            candidate_pairs = _guardrail_compliant_pairs(choice, previous_end_tier)
            exact = [pair for pair in candidate_pairs if pair.start == previous_end]
            if exact:
                position = rng.choice(exact)
            else:
                same_tier_pairs = [
                    pair
                    for pair in candidate_pairs
                    if BODY_POSITION_TIERS[pair.start] == previous_end_tier
                ]
                position = rng.choice(same_tier_pairs or candidate_pairs)

        selected.append(choice)
        selected_positions.append(position)
        remaining.remove(choice)
        pattern_usage[choice.movement_pattern] = pattern_usage.get(choice.movement_pattern, 0) + 1
        previous = choice
        previous_end = position.end

    return ComboSelection(
        exercises=selected, equipment=equipment, body_positions=selected_positions
    )


def _impact_sequence(count: int, high_to_low_ratio: int) -> list[str]:
    """Build a repeating high/low impact pattern, e.g. high, high, low, ...

    Args:
        count: How many slots to generate.
        high_to_low_ratio: How many "high" slots precede each "low" one.

    Returns:
        `count` values of `"high"`/`"low"`, cycling every `high_to_low_ratio + 1` slots.
    """
    cycle = high_to_low_ratio + 1
    return ["low" if (i + 1) % cycle == 0 else "high" for i in range(count)]


def select_plyo_burst(
    pool: dict[str, Exercise],
    equipment: EquipmentCombo,
    count: int,
    rng: random.Random | None = None,
) -> ComboSelection:
    """Select `count` plyo exercises, mostly high impact with recovery breaks.

    Movement-pattern variety doesn't apply here — every plyo-pool candidate
    already shares `movement_pattern == "plyo"`. The structuring rule
    (DESIGN.md section 4: "active recovery via alternating high/low
    impact") is a repeating pattern of 2 or 3 high-impact exercises
    followed by one low-impact recovery exercise, not strict 1:1
    alternation. Within whichever impact a slot requires, a candidate
    whose `mat_orientation_start` matches the previous pick's
    `mat_orientation_end` is preferred, since a burst has no rest between
    exercises and shouldn't force an unplanned turn mid-burst.

    Args:
        pool: Candidate exercises, filtered here to `movement_pattern == "plyo"`.
        equipment: The equipment combo this burst uses.
        count: How many exercises to select.
        rng: Source of randomness for the high:low ratio, tie-breaking, and
            orientation-chaining fallback. Defaults to a fresh `random.Random()`.

    Returns:
        The selection: `count` exercises following a 2:1 or 3:1 high:low
        impact pattern (e.g. high, high, low, high, high, low, ...,
        starting high), and the equipment combo used.

    Raises:
        ValueError: If fewer than `count` plyo exercises support `equipment`,
            or (when `count > 1`) either impact level has no candidates,
            making the pattern impossible.
    """
    rng = rng or random.Random()
    candidates = _filter_pool(pool, equipment, lambda e: e.movement_pattern == "plyo")

    if len(candidates) < count:
        raise ValueError(
            f"only {len(candidates)} eligible plyo exercise(s) for equipment {equipment!r}, "
            f"need {count}"
        )
    if count > 1:
        has_high = any(e.impact == "high" for e in candidates)
        has_low = any(e.impact == "low" for e in candidates)
        if not (has_high and has_low):
            raise ValueError(
                f"need both high- and low-impact plyo exercises for equipment {equipment!r} "
                "for the burst's impact pattern"
            )

    impact_sequence = _impact_sequence(count, high_to_low_ratio=rng.randint(2, 3))

    remaining = list(candidates)
    selected: list[Exercise] = []
    previous: Exercise | None = None

    for impact in impact_sequence:
        same_impact = [e for e in remaining if e.impact == impact]
        bucket = same_impact or remaining

        eligible = bucket
        if previous is not None:
            chained = [e for e in bucket if e.mat_orientation_start == previous.mat_orientation_end]
            if chained:
                eligible = chained

        choice = rng.choice(eligible)
        selected.append(choice)
        remaining.remove(choice)
        previous = choice

    return ComboSelection(exercises=selected, equipment=equipment)
