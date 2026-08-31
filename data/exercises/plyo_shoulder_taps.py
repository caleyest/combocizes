"""Shoulder taps — MoveBank: 7) Plyo / Shoulder taps."""

from combocizes.constants import NO_EQUIPMENT
from combocizes.schema import BodyPosition, Exercise, PrimaryCue

EXERCISE = Exercise(
    name="shoulder_taps",
    movement_pattern="plyo",
    body_region="full",
    muscle_group="plyo",
    body_positions=[BodyPosition.held("plank")],
    unilateral=True,
    impact="low",
    equipment_options=[
        dict(NO_EQUIPMENT),
    ],
    # mover is "arm" -- one arm lifts off the floor to tap the opposite
    # shoulder while the other supports; alternates sides.
    mover="arm",
    location_start="extended",
    direction_start="right",
    location_end="bent",
    direction_end="left",
    primary_cue=PrimaryCue(
        breath="Exhale",
        action="reach",
        action_pool_key="reach_across",
        direction="across to tap your opposite shoulder",
    ),
)
