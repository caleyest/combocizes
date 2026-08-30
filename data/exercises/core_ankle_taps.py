"""Ankle taps — MoveBank: 2) Pull / Ankle taps.

Low confidence: uncertain exactly which movement this is in MoveBank's own
vocabulary (a plank-position ankle reach is assumed here). "Weights" variation
folded in as an equipment option rather than a separate file.
"""

from combocizes.constants import LIGHT_DUMBBELLS, NO_EQUIPMENT
from combocizes.schema import BodyPosition, Exercise, PrimaryCue

EXERCISE = Exercise(
    name="ankle_taps",
    movement_pattern="pull",
    body_region="core",
    muscle_group="core",
    body_positions=[BodyPosition.held("plank")],
    unilateral=True,
    impact="low",
    equipment_options=[
        dict(NO_EQUIPMENT),
        dict(LIGHT_DUMBBELLS),
    ],
    mover="torso",
    mover_position_start="upright",
    mover_position_end="rotated_left",
    primary_cue=PrimaryCue(
        breath="Exhale",
        action="rotate",
        action_pool_key="rotate_tap",
        direction="to tap your ankle",
    ),
)
