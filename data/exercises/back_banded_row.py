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
    mover_position_start="extended",
    mover_position_end="hanging_palms_back",
    primary_cue=PrimaryCue(
        breath="Exhale",
        action="row",
        action_pool_key="row_back",
        direction="back to your ribs",
    ),
)
