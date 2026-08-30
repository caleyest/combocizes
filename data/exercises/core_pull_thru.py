"""Pull thru — MoveBank: 2) Pull / Pull thru.

Low confidence: MoveBank marks this Plank, unusual for what's normally a
standing hip-hinge movement — treating it as a plank/quadruped-based pull
rather than the standard standing pull-through. Worth confirming.
"""

from combocizes.constants import LIGHT_DUMBBELLS
from combocizes.schema import Exercise, PrimaryCue

EXERCISE = Exercise(
    name="pull_thru",
    movement_pattern="pull",
    body_region="core",
    muscle_group="core",
    body_positions=["plank"],
    unilateral=False,
    impact="low",
    equipment_options=[
        dict(LIGHT_DUMBBELLS),
    ],
    mover="hip",
    mover_position_start="hinged",
    mover_position_end="extended",
    primary_cue=PrimaryCue(
        breath="Exhale",
        action="drive",
        action_pool_key="drive_forward",
        direction="forward",
    ),
)
