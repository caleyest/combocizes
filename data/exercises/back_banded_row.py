"""Banded row — MoveBank: 2) Pull / Banded row."""

from combocizes.constants import LIGHT_BAND
from combocizes.schema import BodyPosition, Exercise, PrimaryCue

EXERCISE = Exercise(
    name="banded_row",
    movement_pattern="pull",
    body_region="upper",
    muscle_group="back",
    body_positions=[BodyPosition.held("seated")],
    unilateral=False,
    impact="low",
    equipment_options=[
        dict(LIGHT_BAND),
    ],
    mover="equipment",
    location_start="pressed",
    direction_start="palms_in",
    location_end="bent",
    direction_end="palms_in",
    primary_cue=PrimaryCue(
        breath="Exhale",
        action="row",
        action_pool_key="row_back",
        direction="back to your ribs",
    ),
)
