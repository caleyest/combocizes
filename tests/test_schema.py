import pytest

from combocizes.constants import EQUIPMENT_MOVER
from combocizes.schema import (
    Exercise,
    PrimaryCue,
    equipment_combo_key,
    resolve_exercise,
    resolve_moved_object,
)


def make_exercise(**overrides) -> Exercise:
    fields = {
        "name": "test_exercise",
        "movement_pattern": "pull",
        "body_region": "upper",
        "muscle_group": "biceps",
        "body_position": "standing_narrow",
        "unilateral": False,
        "impact": "low",
        "equipment_options": [{}, {"heavy_dumbbells": True}],
        "mover": "arm",
        "mover_position_start": "hanging_front",
        "mover_position_end": "shoulder",
        "primary_cue": PrimaryCue(
            breath="Exhale", action="curl", action_pool_key="curl_up", direction="up"
        ),
    }
    fields.update(overrides)
    return Exercise(**fields)


def test_equipment_combo_key_is_order_independent() -> None:
    a = equipment_combo_key({"heavy_dumbbells": True, "single": True})
    b = equipment_combo_key({"single": True, "heavy_dumbbells": True})
    assert a == b == (("heavy_dumbbells", True), ("single", True))


def test_resolve_exercise_merges_matching_override() -> None:
    exercise = make_exercise(
        equipment_options=[{"heavy_dumbbells": True, "single": True}],
        overrides={
            equipment_combo_key({"heavy_dumbbells": True, "single": True}): {"unilateral": True}
        },
    )

    resolved = resolve_exercise(exercise, {"heavy_dumbbells": True, "single": True})

    assert resolved["unilateral"] is True


def test_resolve_exercise_is_a_noop_without_a_matching_override() -> None:
    exercise = make_exercise()

    resolved = resolve_exercise(exercise, {})

    assert resolved["unilateral"] is False


def test_resolve_moved_object_uses_mover_when_not_equipment() -> None:
    exercise = make_exercise(mover="leg")
    assert resolve_moved_object(exercise, {"heavy_dumbbells": True}) == "your leg"
    assert resolve_moved_object(exercise, {}) == "your leg"


def test_resolve_moved_object_derives_equipment_phrase() -> None:
    exercise = make_exercise(mover=EQUIPMENT_MOVER)
    assert resolve_moved_object(exercise, {"heavy_dumbbells": True}) == "your dumbbells"
    assert resolve_moved_object(exercise, {"light_band": True}) == "the band"


def test_resolve_moved_object_singularizes_for_single() -> None:
    exercise = make_exercise(mover=EQUIPMENT_MOVER)
    assert (
        resolve_moved_object(exercise, {"heavy_dumbbells": True, "single": True}) == "your dumbbell"
    )


def test_resolve_moved_object_raises_when_equipment_mover_has_no_equipment() -> None:
    exercise = make_exercise(mover=EQUIPMENT_MOVER)
    with pytest.raises(KeyError, match="no equipment phrase"):
        resolve_moved_object(exercise, {})


def test_rejects_invalid_movement_pattern() -> None:
    with pytest.raises(ValueError, match="movement_pattern"):
        make_exercise(movement_pattern="nope")


def test_rejects_invalid_muscle_group() -> None:
    with pytest.raises(ValueError, match="muscle_group"):
        make_exercise(muscle_group="nope")


def test_rejects_empty_equipment_options() -> None:
    with pytest.raises(ValueError, match="equipment_options must list at least one combo"):
        make_exercise(equipment_options=[])


def test_rejects_unknown_equipment_flag() -> None:
    with pytest.raises(ValueError, match="unknown equipment flag"):
        make_exercise(equipment_options=[{"kettlebell": True}])


def test_rejects_single_without_a_dumbbell_flag() -> None:
    with pytest.raises(ValueError, match="requires a dumbbell flag"):
        make_exercise(equipment_options=[{"heavy_band": True, "single": True}])


def test_rejects_override_key_with_no_matching_combo() -> None:
    with pytest.raises(ValueError, match="match no equipment_options combo"):
        make_exercise(overrides={equipment_combo_key({"heavy_band": True}): {"unilateral": True}})


def test_rejects_unknown_refinement_cue_id() -> None:
    with pytest.raises(ValueError, match="unknown refinement_cue_ids"):
        make_exercise(refinement_cue_ids=["not_a_real_cue"])
