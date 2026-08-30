"""The parameterized combo-selection function.

See DESIGN.md section 5: one function — "select N exercises from a filtered
pool, chained by mover position and varied by movement pattern, fit to a
time budget" — reused for plyo bursts, focus songs, and full-body combos,
configured differently per segment (pool filter, exercise count, equipment).
"""

import random
from collections.abc import Callable
from dataclasses import dataclass

from combocizes.constants import SECONDS_PER_EXERCISE
from combocizes.schema import EquipmentCombo, Exercise, equipment_combo_key


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
    """

    exercises: list[Exercise]
    equipment: EquipmentCombo


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

        Each pick after the first prefers candidates whose
        `mover_position_start` matches the previous pick's
        `mover_position_end` — in-song chaining, the primary preference.
        Among whichever set that leaves (the chained candidates, or the full
        remaining pool if none chain), the candidate whose `movement_pattern`
        has been used least so far in this selection is preferred; further
        ties break randomly via `rng`. Both chaining and pattern counts reset
        per call — scoped to one song, not the whole class.

    Raises:
        ValueError: If fewer than `count` exercises remain after filtering.
    """
    rng = rng or random.Random()
    combo_key = equipment_combo_key(equipment)
    candidates = [
        exercise
        for exercise in pool.values()
        if combo_key in (equipment_combo_key(combo) for combo in exercise.equipment_options)
    ]
    if pool_filter is not None:
        candidates = [exercise for exercise in candidates if pool_filter(exercise)]

    if len(candidates) < count:
        raise ValueError(
            f"only {len(candidates)} eligible exercise(s) for equipment {equipment!r}, need {count}"
        )

    remaining = list(candidates)
    pattern_usage: dict[str, int] = {}
    selected: list[Exercise] = []
    previous: Exercise | None = None

    for _ in range(count):
        eligible = remaining
        if previous is not None:
            chained = [
                e for e in remaining if e.mover_position_start == previous.mover_position_end
            ]
            if chained:
                eligible = chained

        least_used = min(pattern_usage.get(e.movement_pattern, 0) for e in eligible)
        tied = [e for e in eligible if pattern_usage.get(e.movement_pattern, 0) == least_used]
        choice = rng.choice(tied)

        selected.append(choice)
        remaining.remove(choice)
        pattern_usage[choice.movement_pattern] = pattern_usage.get(choice.movement_pattern, 0) + 1
        previous = choice

    return ComboSelection(exercises=selected, equipment=equipment)
