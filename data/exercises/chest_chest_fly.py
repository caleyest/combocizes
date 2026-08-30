"""Chest fly — MoveBank: 1) Push / Chest fly.

MoveBank's Body column lists "Back" for this row, which looks like a data
entry error — a chest fly targets chest, not back. Using muscle_group=
"chest" (physically correct) rather than propagating the likely typo;
worth checking the source sheet.
"""

from combocizes.constants import LIGHT_DUMBBELLS
from combocizes.schema import Exercise, PrimaryCue, equipment_combo_key

_HEAVY_SINGLE = equipment_combo_key({"heavy_dumbbells": True, "single": True})
_LIGHT_SINGLE = equipment_combo_key({"light_dumbbells": True, "single": True})

EXERCISE = Exercise(
    name="chest_fly",
    movement_pattern="push",
    body_region="upper",
    muscle_group="chest",
    body_positions=["standing_wide", "hinge"],
    unilateral=False,
    impact="low",
    equipment_options=[
        dict(LIGHT_DUMBBELLS),
        {"heavy_dumbbells": True, "single": True},
        {"light_dumbbells": True, "single": True},
    ],
    mover="equipment",
    mover_position_start="extended",
    mover_position_end="heart's center",
    primary_cue=PrimaryCue(
        breath="Exhale",
        action="squeeze",
        action_pool_key="squeeze_together",
        direction="together",
    ),
    overrides={
        _LIGHT_SINGLE: {"unilateral": True},
    },
)
