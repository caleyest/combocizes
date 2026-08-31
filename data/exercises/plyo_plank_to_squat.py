"""Plank to squat — MoveBank: 7) Plyo / Plank to squat."""

from combocizes.constants import NO_EQUIPMENT
from combocizes.schema import BodyPosition, Exercise, PrimaryCue

EXERCISE = Exercise(
    name="plank_to_squat",
    movement_pattern="plyo",
    body_region="full",
    muscle_group="plyo",
    body_positions=[BodyPosition("plank", "squat")],
    unilateral=False,
    impact="high",
    equipment_options=[
        dict(NO_EQUIPMENT),
    ],
    # mover is "legs" (plural, bilateral) -- both feet jump forward from
    # the plank into the squat together.
    mover="legs",
    location_start="plank",
    direction_start=None,
    location_end="squat",
    direction_end=None,
    primary_cue=PrimaryCue(
        breath="Exhale",
        action="jump",
        action_pool_key="jump_in",
        direction="forward into a squat",
    ),
)
