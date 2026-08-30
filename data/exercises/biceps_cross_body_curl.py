"""Cross body curl — MoveBank: 2) Pull / Cross body curl."""

from combocizes.constants import HEAVY_DUMBBELLS, LIGHT_DUMBBELLS
from combocizes.schema import Exercise, PrimaryCue

EXERCISE = Exercise(
    name="cross_body_curl",
    movement_pattern="pull",
    body_region="upper",
    muscle_group="biceps",
    body_positions=["seated", "kneeling", "standing_narrow", "standing_wide"],
    # Naturally unilateral (not via override): curling toward the opposite
    # shoulder one arm at a time is what makes it "cross body" — both arms
    # at once isn't really the same exercise.
    unilateral=True,
    impact="low",
    equipment_options=[
        dict(HEAVY_DUMBBELLS),
        dict(LIGHT_DUMBBELLS),
    ],
    mover="equipment",
    mover_position_start="hanging_palms_in",
    mover_position_end="shoulder",
    primary_cue=PrimaryCue(
        breath="Exhale",
        action="curl",
        action_pool_key="curl_up",
        direction="up across your body",
    ),
)
