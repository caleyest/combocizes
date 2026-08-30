"""Lying Maltese press — MoveBank: 1) Push / Lying Maltese Press.

Low confidence: an uncommon move: uncertain enough about exact form that
mover_position start/end are an approximation, not a confirmed read.
"""

from combocizes.constants import LIGHT_DUMBBELLS
from combocizes.schema import Exercise, PrimaryCue, equipment_combo_key

_HEAVY_SINGLE = equipment_combo_key({"heavy_dumbbells": True, "single": True})
_LIGHT_SINGLE = equipment_combo_key({"light_dumbbells": True, "single": True})

EXERCISE = Exercise(
    name="lying_maltese_press",
    movement_pattern="push",
    body_region="upper",
    muscle_group="chest",
    body_positions=["supine"],
    unilateral=False,
    impact="low",
    equipment_options=[
        dict(LIGHT_DUMBBELLS),
        {"heavy_dumbbells": True, "single": True},
        {"light_dumbbells": True, "single": True},
    ],
    mover="equipment",
    mover_position_start="extended",
    mover_position_end="overhead",
    primary_cue=PrimaryCue(
        breath="Exhale",
        action="press",
        action_pool_key="press_together",
        direction="up toward the sky",
    ),
    overrides={
        _LIGHT_SINGLE: {"unilateral": True},
    },
)
