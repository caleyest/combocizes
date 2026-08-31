"""Plank surrenders — MoveBank: 7) Plyo / Shoulder taps.

A high-impact duplicate of `shoulder_taps` (same MoveBank row) for the
high-impact side of a plyo burst's high:low pattern.
"""

from combocizes.constants import NO_EQUIPMENT
from combocizes.schema import BodyPosition, Exercise, PrimaryCue

EXERCISE = Exercise(
    name="plank_surrenders",
    movement_pattern="plyo",
    body_region="full",
    muscle_group="plyo",
    body_positions=[BodyPosition.held("plank")],
    unilateral=True,
    impact="high",
    equipment_options=[
        dict(NO_EQUIPMENT),
    ],
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
