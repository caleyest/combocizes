"""Bird dog — MoveBank: 6) Core / Bird dog."""

from combocizes.constants import NO_EQUIPMENT
from combocizes.schema import Exercise, PrimaryCue

EXERCISE = Exercise(
    name="bird_dog",
    movement_pattern="core",
    body_region="core",
    muscle_group="core",
    # "plank" stands in for quadruped/tabletop, same bucket MoveBank itself
    # uses for donkey kick, fire hydrant, and down dog.
    body_positions=["plank"],
    unilateral=True,
    impact="low",
    equipment_options=[
        dict(NO_EQUIPMENT),
    ],
    # No dumbbell/band entries: bird dog isn't typically loaded in this
    # class's equipment set.
    # mover is "torso", not "leg" or "arm": movement_pattern is "core",
    # which has no limb of its own — its job is torso stability, not a limb
    # reach. Naming either limb would also be an arbitrary tie-break (arm
    # and leg move simultaneously and symmetrically; neither is primary),
    # so both go in the refinement cue instead. Start and end are the same
    # ("upright") since the torso's job here is to not move.
    mover="torso",
    mover_position_start="upright",
    mover_position_end="upright",
    primary_cue=PrimaryCue(
        breath="Exhale",
        action="brace",
        action_pool_key="brace_steady",
        direction="steady",
    ),
    refinement_cue_ids=["opposite_arm_and_leg_extend"],
)
