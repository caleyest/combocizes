"""Band pulldown — MoveBank: 2) Pull / Band pulldown."""

from combocizes.constants import LIGHT_BAND
from combocizes.schema import BodyPosition, Exercise, PrimaryCue

EXERCISE = Exercise(
    name="band_pulldown",
    movement_pattern="pull",
    body_region="upper",
    muscle_group="shoulders",
    body_positions=[
        BodyPosition.held("seated"),
        BodyPosition.held("kneeling"),
        BodyPosition.held("standing_narrow"),
        BodyPosition.held("standing_wide"),
        BodyPosition.held("hinge"),
    ],
    unilateral=False,
    impact="low",
    equipment_options=[
        dict(LIGHT_BAND),
    ],
    mover="equipment",
    mover_position_start="overhead",
    mover_position_end="shoulder",
    primary_cue=PrimaryCue(
        breath="Exhale",
        action="pull",
        action_pool_key="pull_down",
        direction="down",
    ),
)
