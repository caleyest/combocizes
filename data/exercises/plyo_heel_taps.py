"""Heel taps — MoveBank: 7) Plyo / Heel taps.

Same mechanics as `run_in_place` (same mover/location/direction/equipment
shape) — a distinct named move in the pool for cueing variety, per its own
MoveBank row, with its own cue text.
"""

from combocizes.constants import HEAVY_BAND, LIGHT_BAND, LIGHT_DUMBBELLS, NO_EQUIPMENT
from combocizes.schema import BodyPosition, Exercise, PrimaryCue

EXERCISE = Exercise(
    name="heel_taps",
    movement_pattern="plyo",
    body_region="full",
    muscle_group="plyo",
    body_positions=[BodyPosition("standing_narrow", "standing_narrow")],
    unilateral=True,
    impact="low",
    equipment_options=[
        dict(NO_EQUIPMENT),
        dict(LIGHT_DUMBBELLS),
        dict(HEAVY_BAND),
        dict(LIGHT_BAND),
    ],
    mover="legs",
    location_start="standing",
    direction_start="right",
    location_end="standing",
    direction_end="left",
    primary_cue=PrimaryCue(
        breath="Exhale",
        action="tap",
        action_pool_key="tap_heel",
        direction="behind you",
    ),
)
