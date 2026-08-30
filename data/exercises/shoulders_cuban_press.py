"""Cuban press — MoveBank: 1) Push / Cuban press."""

from combocizes.constants import HEAVY_DUMBBELLS, LIGHT_BAND, LIGHT_DUMBBELLS
from combocizes.schema import Exercise, PrimaryCue

EXERCISE = Exercise(
    name="cuban_press",
    movement_pattern="push",
    body_region="upper",
    muscle_group="shoulders",
    body_positions=["standing_narrow"],
    unilateral=False,
    impact="low",
    equipment_options=[
        dict(LIGHT_DUMBBELLS),
        dict(HEAVY_DUMBBELLS),
        dict(LIGHT_BAND),
    ],
    # No bodyweight entry: there's nothing to press against without
    # dumbbells or a band, so a bodyweight combo wouldn't mean anything here.
    mover="equipment",
    mover_position_start="heart's center",
    mover_position_end="overhead",
    primary_cue=PrimaryCue(
        breath="Exhale",
        action="press",
        action_pool_key="press_overhead",
        direction="overhead",
    ),
    # Elbow-rotation setup detail moved out of the primary cue (action +
    # mover + where, kept minimal) and into a refinement cue instead.
    refinement_cue_ids=["elbows_rotate_out"],
)
