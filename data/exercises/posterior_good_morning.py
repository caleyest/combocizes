"""Good morning — MoveBank: 5) Hinge / Good morning."""

from combocizes.constants import LIGHT_BAND, LIGHT_DUMBBELLS, NO_EQUIPMENT
from combocizes.schema import Exercise, PrimaryCue

EXERCISE = Exercise(
    name="good_morning",
    movement_pattern="hinge",
    body_region="lower",
    muscle_group="posterior",
    body_positions=["standing_narrow", "standing_wide"],
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
    # mover is "torso", not "hip": "hinge your hip forward" reads oddly as
    # a singular joint name, where "torso" is a clean unpaired noun.
    mover="torso",
    mover_position_start="upright",
    mover_position_end="flexed_forward",
    primary_cue=PrimaryCue(
        breath="Inhale",
        action="hinge",
        action_pool_key="hinge_forward",
        direction="forward",
    ),
)
