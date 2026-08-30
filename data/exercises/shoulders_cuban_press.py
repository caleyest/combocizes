"""Cuban press — MoveBank: 1) Push / Cuban press."""

from combocizes.constants import LIGHT_DUMBBELLS
from combocizes.schema import Exercise, PrimaryCue

EXERCISE = Exercise(
    name="cuban_press",
    movement_pattern="push",
    body_region="upper",
    muscle_group="shoulders",
    body_positions=["standing_narrow", "standing_wide"],
    unilateral=False,
    impact="low",
    equipment_options=[
        dict(LIGHT_DUMBBELLS),
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
)
