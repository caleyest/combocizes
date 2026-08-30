import pytest

from combocizes.cues import RefinementCue, _build_cue_bank


def test_refinement_cue_accepts_known_tags() -> None:
    cue = RefinementCue(text="Keep your elbows pinned.", tags={"region": "upper"})
    assert cue.tags == {"region": "upper"}


def test_refinement_cue_rejects_unknown_tag_key() -> None:
    with pytest.raises(ValueError, match="unknown cue tag key"):
        RefinementCue(text="...", tags={"joint_focus": "elbow"})


def test_refinement_cue_rejects_unknown_tag_value() -> None:
    with pytest.raises(ValueError, match="invalid 'region' tag value"):
        RefinementCue(text="...", tags={"region": "uppr"})


def test_refinement_cue_accepts_list_tag_values() -> None:
    cue = RefinementCue(text="...", tags={"movement_pattern": ["pull", "hinge"]})
    assert cue.tags == {"movement_pattern": ["pull", "hinge"]}


def test_build_cue_bank_merges_category_files(tmp_path) -> None:
    (tmp_path / "upper.py").write_text(
        "from combocizes.cues import RefinementCue\nUPPER = {'a': RefinementCue(text='A')}\n"
    )
    (tmp_path / "lower.py").write_text(
        "from combocizes.cues import RefinementCue\nLOWER = {'b': RefinementCue(text='B')}\n"
    )

    bank = _build_cue_bank(tmp_path)

    assert set(bank) == {"a", "b"}
    assert bank["a"].text == "A"


def test_build_cue_bank_rejects_duplicate_ids(tmp_path) -> None:
    (tmp_path / "upper.py").write_text(
        "from combocizes.cues import RefinementCue\nUPPER = {'dup': RefinementCue(text='A')}\n"
    )
    (tmp_path / "lower.py").write_text(
        "from combocizes.cues import RefinementCue\nLOWER = {'dup': RefinementCue(text='B')}\n"
    )

    with pytest.raises(ValueError, match="duplicate cue id"):
        _build_cue_bank(tmp_path)
