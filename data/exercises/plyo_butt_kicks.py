"""Butt kicks — MoveBank: 7) Plyo / Butt kicks."""

from combocizes.constants import HEAVY_BAND, LIGHT_BAND, LIGHT_DUMBBELLS, NO_EQUIPMENT
from combocizes.schema import BodyPosition, Exercise, PrimaryCue

EXERCISE = Exercise(
    name="butt_kicks",
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
    # mover is "leg" (singular). No direction stated -- same reasoning as
    # high_knees.py: "leg"'s vocabulary has no left/right axis.
    mover="leg",
    location_start="standing",
    direction_start=None,
    location_end="butt_kick",
    direction_end=None,
    primary_cue=PrimaryCue(
        breath="Exhale",
        action="kick",
        action_pool_key="kick_back",
        direction="back to tap your heel",
    ),
)
