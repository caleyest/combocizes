"""Skaters — MoveBank: 7) Plyo / Skaters."""

from combocizes.constants import NO_EQUIPMENT
from combocizes.schema import BodyPosition, Exercise, PrimaryCue

EXERCISE = Exercise(
    name="skaters",
    movement_pattern="plyo",
    body_region="full",
    muscle_group="plyo",
    # Dynamic, not held: each bound lands on the opposite leg in a mirrored
    # lunge, even though both ends share the "standing_wide" label.
    body_positions=[BodyPosition("standing_wide", "standing_wide")],
    unilateral=True,
    impact="high",
    equipment_options=[
        dict(NO_EQUIPMENT),
    ],
    # mover is "leg" (singular, unilateral) -- lands on one leg at a time,
    # alternating sides each bound.
    mover="leg",
    location_start="lunge",
    direction_start="lateral",
    location_end="lunge",
    direction_end="lateral",
    primary_cue=PrimaryCue(
        breath="Exhale",
        action="bound",
        action_pool_key="bound_lateral",
        direction="side to side",
    ),
)
