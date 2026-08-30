"""Cross body curl — MoveBank: 2) Pull / Cross body curl."""

from combocizes.constants import HEAVY_DUMBBELLS, LIGHT_DUMBBELLS
from combocizes.schema import BodyPosition, Exercise, PrimaryCue

EXERCISE = Exercise(
    name="cross_body_curl",
    movement_pattern="pull",
    body_region="upper",
    muscle_group="biceps",
    body_positions=[
        BodyPosition.held("seated"),
        BodyPosition.held("kneeling"),
        BodyPosition.held("standing_narrow"),
        BodyPosition.held("standing_wide"),
    ],
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
    location_start="extended",
    direction_start="palms_front",
    location_end="shoulder",
    direction_end="palms_back",
    primary_cue=PrimaryCue(
        breath="Exhale",
        action="curl",
        action_pool_key="curl_up",
        direction="up across your body",
    ),
)
