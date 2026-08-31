import random

import pytest

from combocizes.combo_selector import (
    _impact_sequence,
    exercise_count_for_duration,
    select_combo,
    select_plyo_burst,
)
from combocizes.constants import SECONDS_PER_EXERCISE
from combocizes.schema import BodyPosition


def test_exercise_count_for_duration_basic_math() -> None:
    minutes = (SECONDS_PER_EXERCISE * 4) / 60
    assert exercise_count_for_duration(minutes) == 4


def test_exercise_count_for_duration_floors_at_one() -> None:
    assert exercise_count_for_duration(0.001) == 1


def test_exercise_count_for_duration_respects_custom_seconds_per_exercise() -> None:
    minutes = 4 * 30 / 60
    assert exercise_count_for_duration(minutes, seconds_per_exercise=30) == 4
    # Same minutes, default (45s) slice: fewer exercises fit.
    assert exercise_count_for_duration(minutes) == 2


def test_select_combo_filters_by_equipment(make_exercise) -> None:
    pool = {
        "a": make_exercise(name="a", equipment_options=[{"heavy_dumbbells": True}]),
        "b": make_exercise(name="b", equipment_options=[{"heavy_band": True}]),
    }

    selection = select_combo(pool, {"heavy_dumbbells": True}, count=1)

    assert selection.exercises == [pool["a"]]
    assert selection.equipment == {"heavy_dumbbells": True}


def test_select_combo_applies_pool_filter(make_exercise) -> None:
    pool = {
        "a": make_exercise(name="a", muscle_group="biceps"),
        "b": make_exercise(name="b", muscle_group="triceps"),
    }

    selection = select_combo(
        pool, {"heavy_dumbbells": True}, count=1, pool_filter=lambda e: e.muscle_group == "triceps"
    )

    assert selection.exercises == [pool["b"]]


def test_select_combo_raises_when_pool_too_small(make_exercise) -> None:
    pool = {"a": make_exercise(name="a")}

    with pytest.raises(ValueError, match="only 1 eligible"):
        select_combo(pool, {"heavy_dumbbells": True}, count=2)


def test_select_combo_prefers_chaining_over_variety(make_exercise) -> None:
    first = make_exercise(
        name="first",
        movement_pattern="pull",
        mover="equipment",
        location_start="extended",
        location_end="shoulder",
    )
    chains = make_exercise(
        name="chains",
        movement_pattern="pull",
        mover="equipment",
        location_start="shoulder",
        location_end="overhead",
    )
    would_win_on_variety = make_exercise(
        name="would_win_on_variety",
        movement_pattern="push",
        mover="equipment",
        location_start="racked",
        location_end="overhead",
    )
    pool = {e.name: e for e in [first, chains, would_win_on_variety]}
    rng = random.Random(0)

    selection = select_combo(pool, {"heavy_dumbbells": True}, count=2, rng=rng)

    if selection.exercises[0].name == "first":
        # "chains" must win the second slot even though "would_win_on_variety"
        # has a less-used movement_pattern, since chaining is primary.
        assert selection.exercises[1].name == "chains"


def test_select_combo_prefers_exact_match_over_mover_chaining(make_exercise) -> None:
    first = make_exercise(
        name="first",
        body_positions=[BodyPosition.held("standing_narrow")],
        movement_pattern="pull",
        mover="equipment",
        location_start="extended",
        location_end="shoulder",
    )
    would_win_on_chaining = make_exercise(
        name="would_win_on_chaining",
        # Tier 1, same as "first" -- passes the guardrail and the
        # same-tier preference, but "standing_wide" != "standing_narrow"
        # exactly, so it still shouldn't beat an exact match. This also
        # demonstrates the "plane" guardrail: narrow/wide aren't
        # interchangeable just because both are tier 1.
        body_positions=[BodyPosition.held("standing_wide")],
        movement_pattern="pull",
        mover="equipment",
        location_start="shoulder",
        location_end="overhead",
    )
    same_stance = make_exercise(
        name="same_stance",
        body_positions=[BodyPosition.held("standing_narrow")],
        movement_pattern="push",
        mover="equipment",
        location_start="racked",
        location_end="overhead",
    )
    pool = {e.name: e for e in [first, would_win_on_chaining, same_stance]}
    rng = random.Random(0)

    selection = select_combo(pool, {"heavy_dumbbells": True}, count=2, rng=rng)

    if selection.exercises[0].name == "first":
        # "same_stance" must win the second slot even though
        # "would_win_on_chaining" chains on location, since an exact
        # body-position match is now the primary preference.
        assert selection.exercises[1].name == "same_stance"


def test_select_combo_falls_back_to_variety_when_nothing_chains(make_exercise) -> None:
    first = make_exercise(
        name="first",
        movement_pattern="pull",
        mover="equipment",
        location_start="extended",
        location_end="shoulder",
    )
    no_chain_a = make_exercise(
        name="no_chain_a",
        movement_pattern="pull",
        mover="equipment",
        location_start="racked",
        location_end="racked",
    )
    no_chain_b = make_exercise(
        name="no_chain_b",
        movement_pattern="push",
        mover="equipment",
        location_start="racked",
        location_end="racked",
    )
    pool = {e.name: e for e in [first, no_chain_a, no_chain_b]}
    rng = random.Random(0)

    selection = select_combo(pool, {"heavy_dumbbells": True}, count=2, rng=rng)

    if selection.exercises[0].name == "first":
        # Neither remaining candidate chains from "first" (its
        # location_end "shoulder" matches neither's start), so variety
        # picks the exercise whose pattern ("push") hasn't been used yet.
        assert selection.exercises[1].name == "no_chain_b"


def test_select_combo_location_match_wins_even_without_a_direction_match(make_exercise) -> None:
    # The direct regression test for the bug that motivated the
    # location/direction split: hammer_curl ends at bare location "shoulder"
    # (no stated direction), and overhead_press_narrow starts at "shoulder"
    # with direction "palms_in" -- location alone must be enough to chain.
    first = make_exercise(
        name="first",
        movement_pattern="pull",
        mover="equipment",
        location_start="hearts_center",
        direction_start=None,
        location_end="shoulder",
        direction_end=None,
    )
    location_chains = make_exercise(
        name="location_chains",
        movement_pattern="push",
        mover="equipment",
        location_start="shoulder",
        direction_start="palms_in",
        location_end="overhead",
        direction_end="palms_in",
    )
    no_match = make_exercise(
        name="no_match",
        movement_pattern="push",
        mover="equipment",
        location_start="racked",
        direction_start=None,
        location_end="racked",
        direction_end=None,
    )
    pool = {e.name: e for e in [first, location_chains, no_match]}
    rng = random.Random(0)

    selection = select_combo(pool, {"heavy_dumbbells": True}, count=2, rng=rng)

    if selection.exercises[0].name == "first":
        assert selection.exercises[1].name == "location_chains"


def test_select_combo_direction_match_refines_a_location_match(make_exercise) -> None:
    first = make_exercise(
        name="first",
        movement_pattern="pull",
        mover="equipment",
        location_start="hearts_center",
        direction_start="palms_in",
        location_end="shoulder",
        direction_end="palms_in",
    )
    location_only = make_exercise(
        name="location_only",
        movement_pattern="push",
        mover="equipment",
        location_start="shoulder",
        direction_start="palms_front",
        location_end="overhead",
        direction_end="palms_front",
    )
    full_match = make_exercise(
        name="full_match",
        movement_pattern="push",
        mover="equipment",
        location_start="shoulder",
        direction_start="palms_in",
        location_end="overhead",
        direction_end="palms_in",
    )
    pool = {e.name: e for e in [first, location_only, full_match]}
    rng = random.Random(0)

    selection = select_combo(pool, {"heavy_dumbbells": True}, count=2, rng=rng)

    if selection.exercises[0].name == "first":
        # Both candidates chain on location, but "full_match" also matches
        # grip -- full match beats location-only, same shape as the
        # body_positions exact-match preference.
        assert selection.exercises[1].name == "full_match"


def test_select_combo_chains_on_the_previous_picks_own_start_transition_point(
    make_exercise,
) -> None:
    # A single exercise has two transition points, its own start and its
    # own end -- either is a plausible physical handoff into the next pick
    # (e.g. a set that returns to the start position on its last rep).
    first = make_exercise(
        name="first",
        movement_pattern="pull",
        mover="equipment",
        location_start="racked",
        direction_start="palms_in",
        location_end="overhead",
        direction_end="palms_front",
    )
    chains_via_start = make_exercise(
        name="chains_via_start",
        movement_pattern="push",
        mover="equipment",
        location_start="racked",
        direction_start="palms_in",
        location_end="floor",
        direction_end=None,
    )
    no_match = make_exercise(
        name="no_match",
        movement_pattern="push",
        mover="equipment",
        location_start="floor",
        direction_start=None,
        location_end="floor",
        direction_end=None,
    )
    pool = {e.name: e for e in [first, chains_via_start, no_match]}
    rng = random.Random(0)

    selection = select_combo(pool, {"heavy_dumbbells": True}, count=2, rng=rng)

    if selection.exercises[0].name == "first":
        assert selection.exercises[1].name == "chains_via_start"


def test_select_combo_pairs_location_and_direction_within_one_transition_point(
    make_exercise,
) -> None:
    # A candidate can't combine a location match on one of "first"'s
    # transition points with a direction match on the *other* -- the pair
    # has to come from the same point for a full match.
    first = make_exercise(
        name="first",
        movement_pattern="pull",
        mover="equipment",
        location_start="racked",
        direction_start="palms_in",
        location_end="overhead",
        direction_end="palms_front",
    )
    mismatched_pairing = make_exercise(
        name="mismatched_pairing",
        movement_pattern="push",
        mover="equipment",
        # location matches "first"'s end ("overhead"), but direction only
        # matches "first"'s start ("palms_in") -- not a real pair.
        location_start="overhead",
        direction_start="palms_in",
        location_end="floor",
        direction_end=None,
    )
    full_match_via_end = make_exercise(
        name="full_match_via_end",
        movement_pattern="push",
        mover="equipment",
        location_start="overhead",
        direction_start="palms_front",
        location_end="floor",
        direction_end=None,
    )
    pool = {e.name: e for e in [first, mismatched_pairing, full_match_via_end]}
    rng = random.Random(0)

    selection = select_combo(pool, {"heavy_dumbbells": True}, count=2, rng=rng)

    if selection.exercises[0].name == "first":
        assert selection.exercises[1].name == "full_match_via_end"


def test_select_combo_chains_on_location_alone_when_mover_has_no_direction_axis(
    make_exercise,
) -> None:
    # "hip" has no entry in MOVER_DIRECTIONS at all -- the majority case,
    # since most movers have no direction axis and both sides are always None.
    first = make_exercise(
        name="first",
        movement_pattern="squat",
        mover="hip",
        location_start="neutral",
        direction_start=None,
        location_end="hinged",
        direction_end=None,
    )
    chains = make_exercise(
        name="chains",
        movement_pattern="hinge",
        mover="hip",
        location_start="hinged",
        direction_start=None,
        location_end="neutral",
        direction_end=None,
    )
    would_lose = make_exercise(
        name="would_lose",
        movement_pattern="hinge",
        mover="hip",
        location_start="raised",
        direction_start=None,
        location_end="neutral",
        direction_end=None,
    )
    pool = {e.name: e for e in [first, chains, would_lose]}
    rng = random.Random(0)

    selection = select_combo(pool, {"heavy_dumbbells": True}, count=2, rng=rng)

    if selection.exercises[0].name == "first":
        assert selection.exercises[1].name == "chains"


def test_select_combo_records_shared_stance_when_available(make_exercise) -> None:
    first = make_exercise(
        name="first",
        body_positions=[BodyPosition.held("standing_narrow"), BodyPosition.held("standing_wide")],
        movement_pattern="pull",
        mover="equipment",
        location_start="extended",
        location_end="shoulder",
    )
    same_stance = make_exercise(
        name="same_stance",
        body_positions=[BodyPosition.held("standing_narrow"), BodyPosition.held("standing_wide")],
        movement_pattern="push",
        mover="equipment",
        location_start="racked",
        location_end="overhead",
    )
    pool = {e.name: e for e in [first, same_stance]}
    rng = random.Random(0)

    selection = select_combo(pool, {"heavy_dumbbells": True}, count=2, rng=rng)

    assert len(selection.body_positions) == 2
    assert selection.body_positions[0] in first.body_positions
    if selection.exercises[1].name == "same_stance":
        # Both exercises support both stances, so the second pick's recorded
        # pair must be whichever one the first pick actually recorded — not
        # just any pair from its own list.
        assert selection.body_positions[1] == selection.body_positions[0]


def test_select_combo_records_own_stance_when_nothing_shared(make_exercise) -> None:
    first = make_exercise(
        name="first",
        body_positions=[BodyPosition.held("standing_narrow")],
        movement_pattern="pull",
        mover="equipment",
        location_start="extended",
        location_end="shoulder",
    )
    no_shared_stance = make_exercise(
        name="no_shared_stance",
        body_positions=[BodyPosition.held("supine")],
        movement_pattern="push",
        mover="equipment",
        location_start="racked",
        location_end="overhead",
    )
    pool = {e.name: e for e in [first, no_shared_stance]}
    rng = random.Random(0)

    selection = select_combo(pool, {"heavy_dumbbells": True}, count=2, rng=rng)

    if selection.exercises[1].name == "no_shared_stance":
        # "supine" (tier 3) is a banned jump from "standing_narrow" (tier
        # 1), but it's the only option left, so the guardrail is silently
        # skipped rather than blocking the pick.
        assert selection.body_positions[1] == BodyPosition.held("supine")


def test_select_combo_stays_on_the_same_specific_stance_whenever_possible(make_exercise) -> None:
    # Mirrors a real bug: without this, "row_narrow" (recorded "plank") ->
    # "tricep_kickbacks" (recorded "hinge") looked like a stance change even
    # though "row_narrow" could equally have been recorded "hinge", which
    # "tricep_kickbacks" also supports. Recording always tries an exact
    # match to the previous pick's recorded end first, so a run of picks
    # that could all share one specific value (here "hinge") stays on it.
    pool = {
        "row_narrow": make_exercise(
            name="row_narrow",
            body_positions=[BodyPosition.held("plank"), BodyPosition.held("hinge")],
            movement_pattern="pull",
            mover="equipment",
            location_start="extended",
            location_end="shoulder",
        ),
        "tricep_kickbacks": make_exercise(
            name="tricep_kickbacks",
            body_positions=[BodyPosition.held("kneeling"), BodyPosition.held("hinge")],
            movement_pattern="push",
            mover="equipment",
            location_start="racked",
            location_end="overhead",
        ),
        "chest_fly": make_exercise(
            name="chest_fly",
            body_positions=[BodyPosition.held("standing_wide"), BodyPosition.held("hinge")],
            movement_pattern="squat",
            mover="equipment",
            location_start="racked",
            location_end="racked",
        ),
    }

    for seed in range(20):
        selection = select_combo(pool, {"heavy_dumbbells": True}, count=3, rng=random.Random(seed))
        for i in range(1, len(selection.exercises)):
            previous_end = selection.body_positions[i - 1].end
            next_pairs = selection.exercises[i].body_positions
            if any(pair.start == previous_end for pair in next_pairs):
                assert selection.body_positions[i].start == previous_end


def test_select_combo_maximizes_pattern_variety_with_no_chaining_signal(make_exercise) -> None:
    pool = {}
    for pattern in ["push", "pull", "hinge", "squat"]:
        for i in range(3):
            name = f"{pattern}_{i}"
            pool[name] = make_exercise(
                name=name,
                movement_pattern=pattern,
                mover="equipment",
                location_start="racked",
                location_end="racked",
            )
    rng = random.Random(42)

    selection = select_combo(pool, {"heavy_dumbbells": True}, count=8, rng=rng)

    usage: dict[str, int] = {}
    for exercise in selection.exercises:
        usage[exercise.movement_pattern] = usage.get(exercise.movement_pattern, 0) + 1

    assert max(usage.values()) - min(usage.values()) <= 1


def test_select_combo_guardrail_excludes_banned_tier_jump(make_exercise) -> None:
    first = make_exercise(name="first", body_positions=[BodyPosition.held("standing_narrow")])
    banned = make_exercise(name="banned", body_positions=[BodyPosition.held("plank")])
    compliant = make_exercise(name="compliant", body_positions=[BodyPosition.held("kneeling")])
    pool = {e.name: e for e in [first, banned, compliant]}

    for seed in range(20):
        selection = select_combo(pool, {"heavy_dumbbells": True}, count=2, rng=random.Random(seed))
        if selection.exercises[0].name == "first":
            # "banned" (tier 3) is a disallowed direct jump from "first"'s
            # tier 1, so it's excluded outright, regardless of pattern
            # usage or mover chaining — only "compliant" (tier 2, the
            # bridge) is left.
            assert selection.exercises[1].name == "compliant"


def test_select_combo_guardrail_falls_back_when_no_compliant_candidate_exists(
    make_exercise,
) -> None:
    first = make_exercise(name="first", body_positions=[BodyPosition.held("standing_narrow")])
    only_option = make_exercise(name="only_option", body_positions=[BodyPosition.held("plank")])
    pool = {e.name: e for e in [first, only_option]}

    for seed in range(20):
        selection = select_combo(pool, {"heavy_dumbbells": True}, count=2, rng=random.Random(seed))
        if selection.exercises[0].name == "first":
            # "only_option" requires a banned tier-1 -> tier-3 jump, but
            # it's the only candidate left, so the guardrail is silently
            # skipped for this pick instead of the selection failing.
            assert selection.exercises[1].name == "only_option"


def test_select_combo_allows_tier_2_bridge_transitions(make_exercise) -> None:
    kneeling_first = make_exercise(
        name="kneeling_first", body_positions=[BodyPosition.held("kneeling")]
    )
    floor_next = make_exercise(name="floor_next", body_positions=[BodyPosition.held("plank")])
    pool = {e.name: e for e in [kneeling_first, floor_next]}

    for seed in range(20):
        selection = select_combo(pool, {"heavy_dumbbells": True}, count=2, rng=random.Random(seed))
        if selection.exercises[0].name == "kneeling_first":
            # tier 2 (kneeling) -> tier 3 (plank) isn't a banned jump.
            assert selection.exercises[1].name == "floor_next"


def test_select_combo_prefers_same_tier_over_bridge_tier(make_exercise) -> None:
    first = make_exercise(name="first", body_positions=[BodyPosition.held("standing_narrow")])
    same_tier = make_exercise(name="same_tier", body_positions=[BodyPosition.held("standing_wide")])
    bridge_tier = make_exercise(name="bridge_tier", body_positions=[BodyPosition.held("kneeling")])
    pool = {e.name: e for e in [first, same_tier, bridge_tier]}

    for seed in range(20):
        selection = select_combo(pool, {"heavy_dumbbells": True}, count=2, rng=random.Random(seed))
        if selection.exercises[0].name == "first":
            # Both "same_tier" and "bridge_tier" are legal from tier 1
            # (standing_narrow), but crossing into the bridge tier is legal,
            # not free — staying in tier 1 wins.
            assert selection.exercises[1].name == "same_tier"


def test_select_combo_exercise_spanning_tiers_chains_on_both_ends(make_exercise) -> None:
    narrow_source = make_exercise(
        name="narrow_source", body_positions=[BodyPosition.held("standing_narrow")]
    )
    spanning = make_exercise(
        name="spanning", body_positions=[BodyPosition("standing_narrow", "standing_wide")]
    )
    wide_sink = make_exercise(name="wide_sink", body_positions=[BodyPosition.held("standing_wide")])
    pool = {e.name: e for e in [narrow_source, spanning, wide_sink]}

    for seed in range(20):
        selection = select_combo(pool, {"heavy_dumbbells": True}, count=3, rng=random.Random(seed))
        names = [e.name for e in selection.exercises]
        positions = selection.body_positions
        for i in range(1, len(names)):
            if names[i - 1] == "narrow_source" and names[i] == "spanning":
                # "spanning"'s own start/end absorbs the narrow -> wide
                # plane change.
                assert positions[i] == BodyPosition("standing_narrow", "standing_wide")
            if names[i - 1] == "spanning" and names[i] == "wide_sink":
                assert positions[i].start == "standing_wide"


def test_select_plyo_burst_filters_to_plyo_movement_pattern(make_exercise) -> None:
    plyo = make_exercise(name="plyo1", movement_pattern="plyo", impact="high")
    not_plyo = make_exercise(name="not_plyo", movement_pattern="push", impact="high")
    pool = {"plyo1": plyo, "not_plyo": not_plyo}

    selection = select_plyo_burst(pool, {"heavy_dumbbells": True}, count=1)

    assert selection.exercises == [plyo]


def test_select_plyo_burst_raises_when_pool_too_small(make_exercise) -> None:
    # A burst repeats a small set of exercises (needs only ceil(count / 2)
    # distinct ones), so count=3 (needs 2 distinct) is the smallest count
    # that a 1-exercise pool can't satisfy.
    pool = {"a": make_exercise(name="a", movement_pattern="plyo", impact="high")}

    with pytest.raises(ValueError, match="only 1 eligible.*need at least 2"):
        select_plyo_burst(pool, {"heavy_dumbbells": True}, count=3)


def test_select_plyo_burst_repeats_exercises_within_a_burst(make_exercise) -> None:
    pool = {
        "a": make_exercise(name="a", movement_pattern="plyo", impact="high"),
        "b": make_exercise(name="b", movement_pattern="plyo", impact="low"),
    }

    # count=4 only needs ceil(4 / 2) = 2 distinct exercises -- exactly what
    # the pool has -- so filling all 4 slots requires reusing at least one.
    selection = select_plyo_burst(pool, {"heavy_dumbbells": True}, count=4, rng=random.Random(0))

    assert len(selection.exercises) == 4
    assert {e.name for e in selection.exercises} == {"a", "b"}


def test_select_plyo_burst_raises_when_missing_an_impact_level(make_exercise) -> None:
    pool = {
        "a": make_exercise(name="a", movement_pattern="plyo", impact="high"),
        "b": make_exercise(name="b", movement_pattern="plyo", impact="high"),
    }

    with pytest.raises(ValueError, match="need both high- and low-impact"):
        select_plyo_burst(pool, {"heavy_dumbbells": True}, count=2)


def test_select_plyo_burst_follows_a_2_or_3_to_1_high_low_pattern(make_exercise) -> None:
    pool = {}
    for i in range(10):
        pool[f"high_{i}"] = make_exercise(name=f"high_{i}", movement_pattern="plyo", impact="high")
        pool[f"low_{i}"] = make_exercise(name=f"low_{i}", movement_pattern="plyo", impact="low")
    rng = random.Random(1)

    selection = select_plyo_burst(pool, {"heavy_dumbbells": True}, count=9, rng=rng)

    impacts = [e.impact for e in selection.exercises]
    assert impacts in (_impact_sequence(9, 2), _impact_sequence(9, 3))


def test_select_plyo_burst_prefers_mat_orientation_chaining(make_exercise) -> None:
    # count=2 is always ["high", "high"] regardless of the burst's internal
    # high:low ratio draw, so a lone low-impact filler keeps the "need both
    # impact levels" check satisfied without affecting which of these three
    # gets picked.
    filler_low = make_exercise(name="filler_low", movement_pattern="plyo", impact="low")
    first = make_exercise(
        name="first", movement_pattern="plyo", impact="high", mat_orientation_end="right"
    )
    chains = make_exercise(
        name="chains", movement_pattern="plyo", impact="high", mat_orientation_start="right"
    )
    would_lose = make_exercise(name="would_lose", movement_pattern="plyo", impact="high")
    pool = {e.name: e for e in [filler_low, first, chains, would_lose]}
    rng = random.Random(0)

    selection = select_plyo_burst(pool, {"heavy_dumbbells": True}, count=2, rng=rng)

    if selection.exercises[0].name == "first":
        assert selection.exercises[1].name == "chains"
