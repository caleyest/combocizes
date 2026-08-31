"""Punches / upper cut — MoveBank: 7) Plyo / Punches / upper cut."""

from combocizes.constants import LIGHT_DUMBBELLS, NO_EQUIPMENT
from combocizes.schema import BodyPosition, Exercise, PrimaryCue

EXERCISE = Exercise(
    name="punches_upper_cut",
    movement_pattern="plyo",
    body_region="full",
    muscle_group="plyo",
    body_positions=[BodyPosition("standing_wide", "standing_wide")],
    unilateral=True,
    impact="low",
    equipment_options=[
        dict(NO_EQUIPMENT),
        dict(LIGHT_DUMBBELLS),
    ],
    # mover is "arm" (not "equipment"): keeps a bodyweight option viable
    # (resolve_moved_object has nothing to name for mover="equipment"
    # without equipment held -- see plyo_pull_throughs.py's docstring).
    mover="arm",
    location_start="bent",
    direction_start="right",
    location_end="overhead",
    direction_end="left",
    primary_cue=PrimaryCue(
        breath="Exhale",
        action="drive",
        action_pool_key="drive_uppercut",
        direction="up",
    ),
)
