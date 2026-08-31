"""Mountain climber (slow) — MoveBank: 7) Plyo / Mountain climber (fast).

A controlled-pace duplicate of `mountain_climbers` (same MoveBank row —
MoveBank doesn't list a separate slow variant) for the low-impact side of a
plyo burst's high:low pattern, the same way MoveBank's own "High knees"
row lists "march (slow)" as a variation of the fast move.
"""

from combocizes.constants import NO_EQUIPMENT
from combocizes.schema import BodyPosition, Exercise, PrimaryCue

EXERCISE = Exercise(
    name="mountain_climbers_slow",
    movement_pattern="plyo",
    body_region="full",
    muscle_group="plyo",
    body_positions=[BodyPosition.held("plank")],
    unilateral=True,
    impact="low",
    equipment_options=[
        dict(NO_EQUIPMENT),
    ],
    mover="knee",
    location_start="plank",
    direction_start="right",
    location_end="toward_elbow",
    direction_end="left",
    primary_cue=PrimaryCue(
        breath="Exhale",
        action="drive",
        action_pool_key="drive_knee_in",
        direction="toward your elbow",
    ),
)
