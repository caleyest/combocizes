"""Cuban press — MoveBank: 1) Push / Cuban press."""

from combocizes.constants import LIGHT_DUMBBELLS
from combocizes.schema import BodyPosition, Exercise, PrimaryCue

EXERCISE = Exercise(
    name="cuban_press",
    movement_pattern="push",
    body_region="upper",
    muscle_group="shoulders",
    body_positions=[BodyPosition.held("standing_narrow"), BodyPosition.held("standing_wide")],
    unilateral=False,
    impact="low",
    equipment_options=[
        dict(LIGHT_DUMBBELLS),
    ],
    # No bodyweight entry: there's nothing to press against without
    # dumbbells or a band, so a bodyweight combo wouldn't mean anything here.
    mover="equipment",
    location_start="extended",
    direction_start="palms_back",
    location_end="overhead",
    direction_end="palms_front",
    primary_cue=PrimaryCue(
        breath="Exhale",
        action="press",
        action_pool_key="press_overhead",
        direction="overhead",
    ),
    # Elbow-rotation setup detail moved out of the primary cue (action +
    # mover + where, kept minimal) and into a refinement cue instead.
)
