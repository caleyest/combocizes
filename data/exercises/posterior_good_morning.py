"""Good morning — MoveBank: 5) Hinge / Good morning."""

from combocizes.constants import LIGHT_BAND, LIGHT_DUMBBELLS, NO_EQUIPMENT
from combocizes.schema import BodyPosition, Exercise, PrimaryCue

EXERCISE = Exercise(
    name="good_morning",
    movement_pattern="hinge",
    body_region="lower",
    muscle_group="posterior",
    body_positions=[
        BodyPosition("standing_narrow", "hinge"),
        BodyPosition("standing_wide", "hinge"),
    ],
    unilateral=False,
    impact="low",
    equipment_options=[
        dict(NO_EQUIPMENT),
        dict(LIGHT_DUMBBELLS),
        dict(LIGHT_BAND),
    ],
    # No heavy_dumbbells entry: a heavily loaded good morning is a
    # form-sensitive, spine-loading lift not appropriate to propose as a
    # default group-class starting point. Flagging in case you disagree.
    # mover is "legs" (plural), not "torso" or "hip": the hinge is driven
    # by both legs together, same reasoning as squat_to_fold.
    mover="legs",
    location_start="standing",
    direction_start=None,
    location_end="hinge",
    direction_end=None,
    primary_cue=PrimaryCue(
        breath="Inhale",
        action="hinge",
        action_pool_key="hinge_forward",
        direction="forward",
    ),
)
