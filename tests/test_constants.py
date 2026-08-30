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


def test_mover_locations_has_an_entry_for_equipment_and_every_list_is_nonempty() -> None:
    assert "equipment" in constants.MOVER_LOCATIONS
    assert all(constants.MOVER_LOCATIONS.values())


def test_mover_directions_movers_are_a_subset_of_mover_locations_movers() -> None:
    assert set(constants.MOVER_DIRECTIONS) <= set(constants.MOVER_LOCATIONS)


def test_dumbbell_flags_are_a_subset_of_equipment_flags() -> None:
    assert set(constants.DUMBBELL_FLAGS) <= set(constants.EQUIPMENT_FLAGS)


def test_equipment_phrases_cover_dumbbell_and_band_flags() -> None:
    dumbbell_and_band_flags = {f for f in constants.EQUIPMENT_FLAGS if f != "block"}
    assert set(constants.EQUIPMENT_PHRASES) == dumbbell_and_band_flags


def test_body_position_tiers_cover_every_body_position() -> None:
    assert set(constants.BODY_POSITION_TIERS) == set(constants.BODY_POSITIONS)


def test_low_body_positions_are_the_non_tier_1_positions() -> None:
    assert constants.LOW_BODY_POSITIONS == {
        position for position, tier in constants.BODY_POSITION_TIERS.items() if tier != 1
    }
