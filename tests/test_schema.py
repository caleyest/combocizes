import pytest

from combocizes.schema import (
    BodyPosition,
    equipment_combo_key,
    resolve_exercise,
    resolve_moved_object,
)


def test_equipment_combo_key_is_order_independent() -> None:
    a = equipment_combo_key({"heavy_dumbbells": True, "single": True})
    b = equipment_combo_key({"single": True, "heavy_dumbbells": True})
    assert a == b == (("heavy_dumbbells", True), ("single", True))


def test_resolve_exercise_merges_matching_override(make_exercise) -> None:
    exercise = make_exercise(
        equipment_options=[{"heavy_dumbbells": True, "single": True}],
        overrides={
            equipment_combo_key({"heavy_dumbbells": True, "single": True}): {"unilateral": True}
        },
    )

    resolved = resolve_exercise(exercise, {"heavy_dumbbells": True, "single": True})

    assert resolved["unilateral"] is True


def test_resolve_exercise_is_a_noop_without_a_matching_override(make_exercise) -> None:
    exercise = make_exercise()

    resolved = resolve_exercise(exercise, {})

    assert resolved["unilateral"] is False


def test_resolve_moved_object_uses_mover_when_not_equipment(make_exercise) -> None:
    exercise = make_exercise(
        mover="leg", mover_position_start="standing", mover_position_end="lunge_back"
    )
    assert resolve_moved_object(exercise, {"heavy_dumbbells": True}) == "your leg"
    assert resolve_moved_object(exercise, {}) == "your leg"


def test_resolve_moved_object_derives_equipment_phrase(make_exercise) -> None:
    exercise = make_exercise(
        mover="equipment", mover_position_start="hanging_palms_in", mover_position_end="shoulder"
    )
    assert resolve_moved_object(exercise, {"heavy_dumbbells": True}) == "your dumbbells"
    assert resolve_moved_object(exercise, {"light_band": True}) == "the band"


def test_resolve_moved_object_singularizes_for_single(make_exercise) -> None:
    exercise = make_exercise(
        mover="equipment", mover_position_start="hanging_palms_in", mover_position_end="shoulder"
    )
    assert (
        resolve_moved_object(exercise, {"heavy_dumbbells": True, "single": True}) == "your dumbbell"
    )


def test_resolve_moved_object_raises_when_equipment_mover_has_no_equipment(make_exercise) -> None:
    exercise = make_exercise(
        mover="equipment", mover_position_start="hanging_palms_in", mover_position_end="shoulder"
    )
    with pytest.raises(KeyError, match="no equipment phrase"):
        resolve_moved_object(exercise, {})


def test_rejects_invalid_movement_pattern(make_exercise) -> None:
    with pytest.raises(ValueError, match="movement_pattern"):
        make_exercise(movement_pattern="nope")


def test_rejects_invalid_muscle_group(make_exercise) -> None:
    with pytest.raises(ValueError, match="muscle_group"):
        make_exercise(muscle_group="nope")


def test_rejects_empty_body_positions(make_exercise) -> None:
    with pytest.raises(ValueError, match="body_positions must list at least one position"):
        make_exercise(body_positions=[])


def test_rejects_invalid_body_position_start(make_exercise) -> None:
    with pytest.raises(ValueError, match="invalid body_positions"):
        make_exercise(body_positions=[BodyPosition("upside_down", "standing_narrow")])


def test_rejects_invalid_body_position_end(make_exercise) -> None:
    with pytest.raises(ValueError, match="invalid body_positions"):
        make_exercise(body_positions=[BodyPosition("standing_narrow", "upside_down")])


def test_accepts_multiple_body_positions(make_exercise) -> None:
    pairs = [
        BodyPosition.held("standing_narrow"),
        BodyPosition.held("standing_wide"),
        BodyPosition("standing_narrow", "lunge"),
    ]
    exercise = make_exercise(body_positions=pairs)
    assert exercise.body_positions == pairs


def test_rejects_empty_equipment_options(make_exercise) -> None:
    with pytest.raises(ValueError, match="equipment_options must list at least one combo"):
        make_exercise(equipment_options=[])


def test_rejects_unknown_equipment_flag(make_exercise) -> None:
    with pytest.raises(ValueError, match="unknown equipment flag"):
        make_exercise(equipment_options=[{"kettlebell": True}])


def test_rejects_single_without_a_dumbbell_flag(make_exercise) -> None:
    with pytest.raises(ValueError, match="requires a dumbbell flag"):
        make_exercise(equipment_options=[{"heavy_band": True, "single": True}])


def test_rejects_override_key_with_no_matching_combo(make_exercise) -> None:
    with pytest.raises(ValueError, match="match no equipment_options combo"):
        make_exercise(overrides={equipment_combo_key({"heavy_band": True}): {"unilateral": True}})


def test_rejects_invalid_mover(make_exercise) -> None:
    with pytest.raises(ValueError, match="invalid mover"):
        make_exercise(mover="wing", mover_position_start="tucked", mover_position_end="spread")


def test_rejects_mover_position_not_in_movers_vocabulary(make_exercise) -> None:
    with pytest.raises(ValueError, match="invalid mover_position_start"):
        make_exercise(
            mover="leg", mover_position_start="hanging_palms_in", mover_position_end="standing"
        )


def test_accepts_valid_equipment_mover_position(make_exercise) -> None:
    exercise = make_exercise(
        mover="equipment", mover_position_start="hanging_palms_in", mover_position_end="shoulder"
    )
    assert exercise.mover_position_end == "shoulder"


def test_accepts_valid_leg_position(make_exercise) -> None:
    exercise = make_exercise(
        mover="leg", mover_position_start="standing", mover_position_end="lunge_back"
    )
    assert exercise.mover_position_end == "lunge_back"
