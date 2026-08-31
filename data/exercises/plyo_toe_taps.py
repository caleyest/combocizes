"""Toe taps — MoveBank: 7) Plyo / Plank jack.

A low-impact duplicate of `plank_jack` (same MoveBank row) for the
low-impact side of a plyo burst's high:low pattern.
"""

from combocizes.constants import NO_EQUIPMENT
from combocizes.schema import BodyPosition, Exercise, PrimaryCue

EXERCISE = Exercise(
    name="toe_taps",
    movement_pattern="plyo",
    body_region="full",
    muscle_group="plyo",
    body_positions=[BodyPosition.held("plank")],
    unilateral=False,
    impact="low",
    equipment_options=[
        dict(NO_EQUIPMENT),
    ],
    mover="feet",
    location_start="together",
    direction_start=None,
    location_end="apart",
    direction_end=None,
    primary_cue=PrimaryCue(
        breath="Exhale",
        action="jump",
        action_pool_key="jump_out",
        direction="apart",
    ),
)
