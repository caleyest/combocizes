import pytest

from combocizes.schema import (
    BodyPosition,
    Exercise,
    PrimaryCue,
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
        mover="leg",
        location_start="standing",
        direction_start="forward",
        location_end="lunge",
        direction_end="back",
    )
    assert resolve_moved_object(exercise, {"heavy_dumbbells": True}) == "your leg"
    assert resolve_moved_object(exercise, {}) == "your leg"


def test_resolve_moved_object_derives_equipment_phrase(make_exercise) -> None:
    exercise = make_exercise(
        mover="equipment",
        location_start="extended",
        direction_start="palms_in",
        location_end="shoulder",
        direction_end=None,
    )
    assert resolve_moved_object(exercise, {"heavy_dumbbells": True}) == "your dumbbells"
    assert resolve_moved_object(exercise, {"light_band": True}) == "the band"


def test_resolve_moved_object_singularizes_for_single(make_exercise) -> None:
    exercise = make_exercise(
        mover="equipment",
        location_start="extended",
        direction_start="palms_in",
        location_end="shoulder",
        direction_end=None,
    )
    assert (
        resolve_moved_object(exercise, {"heavy_dumbbells": True, "single": True}) == "your dumbbell"
    )


def test_resolve_moved_object_raises_when_equipment_mover_has_no_equipment(make_exercise) -> None:
    exercise = make_exercise(
        mover="equipment",
        location_start="extended",
        direction_start="palms_in",
        location_end="shoulder",
        direction_end=None,
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
        make_exercise(
            mover="wing",
            location_start="tucked",
            direction_start=None,
            location_end="spread",
            direction_end=None,
        )


def test_rejects_location_not_in_movers_vocabulary(make_exercise) -> None:
    with pytest.raises(ValueError, match="invalid location_start"):
        make_exercise(
            mover="leg",
            location_start="hanging",
            direction_start=None,
            location_end="standing",
            direction_end=None,
        )


def test_rejects_direction_for_a_mover_with_no_direction_axis(make_exercise) -> None:
    with pytest.raises(ValueError, match="invalid direction_start"):
        make_exercise(
            mover="hip",
            location_start="neutral",
            direction_start="left",
            location_end="hinged",
            direction_end=None,
        )


def test_accepts_none_direction_on_any_mover(make_exercise) -> None:
    exercise = make_exercise(
        mover="hip",
        location_start="neutral",
        direction_start=None,
        location_end="hinged",
        direction_end=None,
    )
    assert exercise.direction_start is None
    assert exercise.direction_end is None


def test_accepts_valid_equipment_location_and_direction(make_exercise) -> None:
    exercise = make_exercise(
        mover="equipment",
        location_start="extended",
        direction_start="palms_in",
        location_end="shoulder",
        direction_end=None,
    )
    assert exercise.location_end == "shoulder"
    assert exercise.direction_start == "palms_in"


def test_accepts_valid_leg_location_and_direction(make_exercise) -> None:
    exercise = make_exercise(
        mover="leg",
        location_start="standing",
        direction_start="forward",
        location_end="lunge",
        direction_end="back",
    )
    assert exercise.location_end == "lunge"
    assert exercise.direction_end == "back"


def test_requires_direction_end_to_be_passed_explicitly() -> None:
    # Constructs Exercise directly, bypassing make_exercise's fixture
    # defaults, since those would silently backfill the omitted field.
    with pytest.raises(TypeError):
        Exercise(
            name="test_exercise",
            movement_pattern="pull",
            body_region="upper",
            muscle_group="biceps",
            body_positions=[BodyPosition.held("standing_narrow")],
            unilateral=False,
            impact="low",
            equipment_options=[{}],
            mover="leg",
            location_start="standing",
            location_end="lunge",
            direction_start="forward",
            # direction_end intentionally omitted -- required, not defaulted.
            primary_cue=PrimaryCue(
                breath="Exhale", action="curl", action_pool_key="curl_up", direction="up"
            ),
        )
