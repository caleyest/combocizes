"""Squat to fold — MoveBank: 3) Squat / Squat to fold."""

from combocizes.constants import HEAVY_DUMBBELLS, LIGHT_BAND, LIGHT_DUMBBELLS, NO_EQUIPMENT
from combocizes.schema import BodyPosition, Exercise, PrimaryCue

EXERCISE = Exercise(
    name="squat_to_fold",
    movement_pattern="squat",
    body_region="lower",
    muscle_group="lower",
    body_positions=[BodyPosition("standing_narrow", "squat")],
    unilateral=False,
    impact="low",
    equipment_options=[
        dict(NO_EQUIPMENT),
        dict(HEAVY_DUMBBELLS),
        dict(LIGHT_DUMBBELLS),
        dict(LIGHT_BAND),
    ],
    # mover is "legs" (plural), not "leg" or "torso": movement_pattern is
    # "squat", whose canonical mover is the legs, and squat is bilateral —
    # both legs bend together, so "legs" (plural) is correct where "leg"
    # (singular) would wrongly imply one side. The fold that distinguishes
    # this from a plain squat is a refinement cue instead.
    mover="legs",
    mover_position_start="standing",
    mover_position_end="squat_bottom",
    primary_cue=PrimaryCue(
        # Inhale, not exhale: the cue captures the descent (eccentric), and
        # exhale belongs on exertion — the drive back up, not going down.
        breath="Inhale",
        action="squat",
        action_pool_key="squat_down",
        direction="down",
    ),
)
