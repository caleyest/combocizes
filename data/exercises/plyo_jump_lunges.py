"""Jump lunge — MoveBank: 7) Plyo / Jump lunge."""

from combocizes.constants import LIGHT_DUMBBELLS, NO_EQUIPMENT
from combocizes.schema import BodyPosition, Exercise, PrimaryCue

EXERCISE = Exercise(
    name="jump_lunges",
    movement_pattern="plyo",
    body_region="full",
    muscle_group="plyo",
    # Dynamic, not held: each jump switches which leg lands forward, even
    # though both ends share the "lunge" label.
    body_positions=[BodyPosition("lunge", "lunge")],
    unilateral=True,
    impact="high",
    equipment_options=[
        dict(NO_EQUIPMENT),
        dict(LIGHT_DUMBBELLS),
    ],
    # mover is "leg" (singular, unilateral) -- the switch jump swaps which
    # leg is forward each rep, same framing as reverse_lunge.py.
    # No direction stated: unlike reverse_lunge's controlled step, a switch
    # jump doesn't have a clean single forward/back axis to name.
    mover="leg",
    location_start="lunge",
    direction_start=None,
    location_end="lunge",
    direction_end=None,
    primary_cue=PrimaryCue(
        breath="Exhale",
        action="switch",
        action_pool_key="switch_jump",
        direction="in the air",
    ),
)
