"""Jumping jacks — MoveBank: 7) Plyo / Jumping jacks."""

from combocizes.constants import NO_EQUIPMENT
from combocizes.schema import Exercise, PrimaryCue

EXERCISE = Exercise(
    name="jumping_jacks",
    movement_pattern="plyo",
    body_region="full",
    muscle_group="plyo",
    body_positions=["standing_wide"],
    unilateral=False,
    impact="high",
    equipment_options=[
        dict(NO_EQUIPMENT),
    ],
    # No dumbbell/band entries: a plyo cardio move, not loaded in this
    # class's equipment set.
    # mover is "feet", not "leg": both legs jump apart together, and "feet"
    # (plural noun) reads correctly where "leg" (singular) would wrongly
    # imply one side.
    mover="feet",
    mover_position_start="together",
    mover_position_end="apart",
    primary_cue=PrimaryCue(
        breath="Exhale",
        action="jump",
        action_pool_key="jump_out",
        direction="apart",
    ),
    refinement_cue_ids=["arms_reach_overhead"],
)
