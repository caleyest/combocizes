"""Tricep overhead extension — MoveBank: 1) Push / Tricep overhead."""

from combocizes.constants import HEAVY_DUMBBELLS, LIGHT_BAND, LIGHT_DUMBBELLS
from combocizes.schema import BodyPosition, Exercise, PrimaryCue, equipment_combo_key

_HEAVY_SINGLE = equipment_combo_key({"heavy_dumbbells": True, "single": True})
_LIGHT_SINGLE = equipment_combo_key({"light_dumbbells": True, "single": True})

EXERCISE = Exercise(
    name="tricep_overhead",
    movement_pattern="push",
    body_region="upper",
    muscle_group="triceps",
    body_positions=[
        BodyPosition.held("supine"),
        BodyPosition.held("seated"),
        BodyPosition.held("kneeling"),
        BodyPosition.held("standing_narrow"),
        BodyPosition.held("standing_wide"),
    ],
    unilateral=False,
    impact="low",
    equipment_options=[
        dict(HEAVY_DUMBBELLS),
        dict(LIGHT_DUMBBELLS),
        dict(LIGHT_BAND),
        {"heavy_dumbbells": True, "single": True},
        {"light_dumbbells": True, "single": True},
    ],
    # No bodyweight entry: nothing to press without added resistance.
    mover="equipment",
    mover_position_start="behind_head",
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
