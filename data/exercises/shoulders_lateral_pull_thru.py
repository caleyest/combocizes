"""Lateral pull thru — MoveBank: 2) Pull / Lateral pull thru.

Low confidence: uncertain exact form (a supine banded lateral raise is
assumed here). Worth confirming.
"""

from combocizes.constants import HEAVY_DUMBBELLS
from combocizes.schema import BodyPosition, Exercise, PrimaryCue

EXERCISE = Exercise(
    name="lateral_pull_thru",
    movement_pattern="pull",
    body_region="upper",
    muscle_group="shoulders",
    body_positions=[BodyPosition.held("supine")],
    unilateral=True,
    impact="low",
    equipment_options=[
        dict(HEAVY_DUMBBELLS),
    ],
    mover="equipment",
    mover_position_start="hanging_palms_in",
    mover_position_end="extended",
    primary_cue=PrimaryCue(
        breath="Exhale",
        action="raise",
        action_pool_key="raise_out",
        direction="out to the side",
    ),
)
