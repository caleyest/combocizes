from combocizes import constants


def test_vocab_lists_are_nonempty() -> None:
    vocabs = [
        constants.MOVEMENT_PATTERNS,
        constants.BODY_REGIONS,
        constants.MUSCLE_GROUPS,
        constants.BODY_POSITIONS,
        constants.IMPACT_LEVELS,
        constants.EQUIPMENT_FLAGS,
        constants.DUMBBELL_FLAGS,
    ]
    assert all(vocabs)


def test_mover_positions_has_an_entry_for_equipment_and_every_list_is_nonempty() -> None:
    assert "equipment" in constants.MOVER_POSITIONS
    assert all(constants.MOVER_POSITIONS.values())


def test_dumbbell_flags_are_a_subset_of_equipment_flags() -> None:
    assert set(constants.DUMBBELL_FLAGS) <= set(constants.EQUIPMENT_FLAGS)


def test_equipment_phrases_cover_dumbbell_and_band_flags() -> None:
    dumbbell_and_band_flags = {f for f in constants.EQUIPMENT_FLAGS if f != "block"}
    assert set(constants.EQUIPMENT_PHRASES) == dumbbell_and_band_flags
