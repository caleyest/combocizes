"""Overhead press, wide grip — MoveBank: 1) Push / Overhead press variation.

Decomposed from the base overhead press per grip: palms facing front.
"""

from combocizes.constants import HEAVY_DUMBBELLS, LIGHT_DUMBBELLS
from combocizes.schema import Exercise, PrimaryCue, equipment_combo_key

_HEAVY_SINGLE = equipment_combo_key({"heavy_dumbbells": True, "single": True})
_LIGHT_SINGLE = equipment_combo_key({"light_dumbbells": True, "single": True})

EXERCISE = Exercise(
    name="overhead_press_wide",
    movement_pattern="push",
    body_region="upper",
    muscle_group="shoulders",
    body_positions=["seated", "kneeling", "standing_narrow", "standing_wide"],
    unilateral=False,
    impact="low",
    equipment_options=[
        dict(HEAVY_DUMBBELLS),
        dict(LIGHT_DUMBBELLS),
        {"heavy_dumbbells": True, "single": True},
        {"light_dumbbells": True, "single": True},
    ],
    mover="equipment",
    mover_position_start="shoulder_palms_front",
    mover_position_end="overhead",
    primary_cue=PrimaryCue(
        breath="Exhale",
        action="press",
        action_pool_key="press_overhead",
        direction="overhead",
    ),
    overrides={
        _HEAVY_SINGLE: {"unilateral": True},
        _LIGHT_SINGLE: {"unilateral": True},
    },
)
