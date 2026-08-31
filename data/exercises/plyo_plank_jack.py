"""Plank jack — MoveBank: 7) Plyo / Plank jack."""

from combocizes.constants import NO_EQUIPMENT
from combocizes.schema import BodyPosition, Exercise, PrimaryCue

EXERCISE = Exercise(
    name="plank_jack",
    movement_pattern="plyo",
    body_region="full",
    muscle_group="plyo",
    body_positions=[BodyPosition.held("plank")],
    unilateral=False,
    impact="high",
    equipment_options=[
        dict(NO_EQUIPMENT),
    ],
    # mover is "feet" -- both feet jump apart and back together at once,
    # the exact vocabulary jumping_jacks.py already uses, just from a plank
    # instead of standing.
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
