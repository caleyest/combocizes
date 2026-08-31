"""Pull throughs — MoveBank: 7) Plyo / Pull throughs.

Mirrors `core_pull_thru.py`'s shape (same plank/quadruped stance, same
mover="equipment" with the band swept floor-level from side to side) at a
brisker, continuous plyo tempo instead of a slow core-focused pace, and
with a resistance band instead of a dumbbell -- a distinct exercise from
`pull_thru`, not a duplicate (MoveBank lists the plyo version separately,
under its own "Plyo" row rather than "Pull").
"""

from combocizes.constants import HEAVY_BAND, LIGHT_BAND
from combocizes.schema import BodyPosition, Exercise, PrimaryCue

EXERCISE = Exercise(
    name="pull_throughs",
    movement_pattern="plyo",
    body_region="full",
    muscle_group="plyo",
    # Held: the whole-body stance stays in plank throughout -- only the
    # band's position (captured by direction, not location) changes.
    body_positions=[BodyPosition.held("plank")],
    unilateral=False,
    impact="low",
    equipment_options=[
        dict(HEAVY_BAND),
        dict(LIGHT_BAND),
    ],
    mover="equipment",
    location_start="floor",
    direction_start="right",
    location_end="floor",
    direction_end="left",
    primary_cue=PrimaryCue(
        breath="Exhale",
        action="pull",
        action_pool_key="pull_through",
        direction="through to the other side",
    ),
)
