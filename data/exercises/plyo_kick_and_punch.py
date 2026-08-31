"""Kick and punch — MoveBank: 7) Plyo / Kick and punch."""

from combocizes.constants import LIGHT_DUMBBELLS, NO_EQUIPMENT
from combocizes.schema import BodyPosition, Exercise, PrimaryCue

EXERCISE = Exercise(
    name="kick_and_punch",
    movement_pattern="plyo",
    body_region="full",
    muscle_group="plyo",
    body_positions=[BodyPosition("standing_narrow", "standing_narrow")],
    unilateral=True,
    impact="low",
    equipment_options=[
        dict(NO_EQUIPMENT),
        dict(LIGHT_DUMBBELLS),
    ],
    # mover is "leg" (singular), naming the kick; the opposite-arm punch
    # that accompanies it lives in a refinement cue instead. No direction
    # stated -- same reasoning as high_knees.py.
    mover="leg",
    location_start="standing",
    direction_start=None,
    location_end="raised_straight",
    direction_end=None,
    primary_cue=PrimaryCue(
        breath="Exhale",
        action="kick",
        action_pool_key="kick_and_punch",
        direction="out and punch",
    ),
)
