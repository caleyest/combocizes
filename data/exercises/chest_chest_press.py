"""Chest press — MoveBank: 1) Push / Chest press."""

from combocizes.constants import HEAVY_DUMBBELLS, LIGHT_BAND, LIGHT_DUMBBELLS
from combocizes.schema import BodyPosition, Exercise, PrimaryCue, equipment_combo_key

_HEAVY_SINGLE = equipment_combo_key({"heavy_dumbbells": True, "single": True})
_LIGHT_SINGLE = equipment_combo_key({"light_dumbbells": True, "single": True})

EXERCISE = Exercise(
    name="chest_press",
    movement_pattern="push",
    body_region="upper",
    muscle_group="chest",
    # Both held positions kept even though they imply different setups
    # (lying dumbbell press vs. standing band press in a lunge stance) —
    # same movement, different equipment, per DESIGN.md's additive
    # body_positions model.
    body_positions=[BodyPosition.held("supine"), BodyPosition.held("hinge")],
    unilateral=False,
    impact="low",
    equipment_options=[
        dict(HEAVY_DUMBBELLS),
        dict(LIGHT_DUMBBELLS),
        dict(LIGHT_BAND),
        {"heavy_dumbbells": True, "single": True},
        {"light_dumbbells": True, "single": True},
    ],
    mover="equipment",
    mover_position_start="shoulder",
    mover_position_end="extended",
    primary_cue=PrimaryCue(
        breath="Exhale",
        action="press",
        action_pool_key="press_forward",
        direction="forward",
    ),
    overrides={
        _HEAVY_SINGLE: {"unilateral": True},
        _LIGHT_SINGLE: {"unilateral": True},
    },
)
