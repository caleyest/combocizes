"""Burpees — MoveBank: 7) Plyo / Burpees."""

from combocizes.constants import NO_EQUIPMENT
from combocizes.schema import BodyPosition, Exercise, PrimaryCue

EXERCISE = Exercise(
    name="burpees",
    movement_pattern="plyo",
    body_region="full",
    muscle_group="plyo",
    body_positions=[BodyPosition("plank", "standing_narrow")],
    unilateral=False,
    impact="high",
    equipment_options=[
        dict(NO_EQUIPMENT),
    ],
    # mover is "legs" (plural, bilateral) -- both feet drive from the
    # plank back up to standing (with a jump). The squat/push-up phases in
    # between aren't separately modeled -- this exercise's defining
    # transition is plank -> standing.
    mover="legs",
    location_start="plank",
    direction_start=None,
    location_end="standing",
    direction_end=None,
    primary_cue=PrimaryCue(
        breath="Exhale",
        action="drive",
        action_pool_key="drive_up",
        direction="up to standing",
    ),
)
