from combocizes import constants


def test_vocab_lists_are_nonempty() -> None:
    vocabs = [
        constants.MOVEMENT_PATTERNS,
        constants.BODY_REGIONS,
        constants.MUSCLE_GROUPS,
        constants.BODY_POSITIONS,
        constants.IMPACT_LEVELS,
        constants.DUMBBELL_POSITIONS,
        constants.BAND_POSITIONS,
        constants.EQUIPMENT_FLAGS,
        constants.DUMBBELL_FLAGS,
    ]
    assert all(vocabs)


def test_dumbbell_flags_are_a_subset_of_equipment_flags() -> None:
    assert set(constants.DUMBBELL_FLAGS) <= set(constants.EQUIPMENT_FLAGS)


def test_equipment_phrases_cover_dumbbell_and_band_flags() -> None:
    dumbbell_and_band_flags = {f for f in constants.EQUIPMENT_FLAGS if f != "block"}
    assert set(constants.EQUIPMENT_PHRASES) == dumbbell_and_band_flags
