"""Build a standalone arms-focus sequence. Run with: just run arms_sequence

Scripts are thin — they load inputs, call into `combocizes`, and write outputs.
Keep reusable logic in `src/combocizes/`, not here.
"""

import random

from combocizes.combo_selector import exercise_count_for_duration, select_combo
from combocizes.constants import ARMS_MINUTES, ARMS_MUSCLE_GROUPS, LIGHT_DUMBBELLS
from combocizes.loader import load_exercises
from combocizes.schema import resolve_exercise, resolve_moved_object
from combocizes.utils import get_logger

log = get_logger(__name__)


def main() -> None:
    pool = load_exercises()
    rng = random.Random()
    equipment = dict(LIGHT_DUMBBELLS)

    selection = select_combo(
        pool,
        equipment,
        exercise_count_for_duration(ARMS_MINUTES),
        pool_filter=lambda e: e.muscle_group in ARMS_MUSCLE_GROUPS,
        rng=rng,
    )

    log.info(
        "built %d-exercise arms sequence with equipment %s",
        len(selection.exercises),
        equipment,
    )
    for exercise, body_position in zip(selection.exercises, selection.body_positions, strict=True):
        resolved = resolve_exercise(exercise, equipment)
        cue = resolved["primary_cue"]
        moved_object = resolve_moved_object(exercise, equipment)

        print(f"{exercise.name} ({exercise.muscle_group}) [{body_position}]")
        print(
            f"  {cue['breath']}, {exercise.name}, {cue['action']} "
            f"{moved_object} {cue['direction']}."
        )


if __name__ == "__main__":
    main()
