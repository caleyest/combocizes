"""Fast feet — MoveBank: 7) Plyo / Fast feet."""

from combocizes.constants import HEAVY_BAND, LIGHT_BAND, LIGHT_DUMBBELLS, NO_EQUIPMENT
from combocizes.schema import BodyPosition, Exercise, PrimaryCue

EXERCISE = Exercise(
    name="fast_feet",
    movement_pattern="plyo",
    body_region="full",
    muscle_group="plyo",
    # Dynamic, not held: the squat depth stays constant while weight shifts
    # rapidly side to side.
    body_positions=[BodyPosition("squat", "squat")],
    unilateral=True,
    impact="low",
    equipment_options=[
        dict(NO_EQUIPMENT),
        dict(LIGHT_DUMBBELLS),
        dict(HEAVY_BAND),
        dict(LIGHT_BAND),
    ],
    mover="legs",
    location_start="squat",
    direction_start="right",
    location_end="squat",
    direction_end="left",
    primary_cue=PrimaryCue(
        breath="Exhale",
        action="tap",
        action_pool_key="tap_fast",
        direction="side to side",
    ),
)
