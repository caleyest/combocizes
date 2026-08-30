import pytest

from combocizes.cues import RefinementCue, build_cue_bank


def test_refinement_cue_exercise_ids_defaults_to_empty() -> None:
    cue = RefinementCue(text="...")
    assert cue.exercise_ids == []


def test_refinement_cue_accepts_exercise_ids() -> None:
    cue = RefinementCue(text="...", exercise_ids=["squat_to_fold", "reverse_lunge"])
    assert cue.exercise_ids == ["squat_to_fold", "reverse_lunge"]


def test_build_cue_bank_merges_category_files(tmp_path) -> None:
    (tmp_path / "upper.py").write_text(
        "from combocizes.cues import RefinementCue\nUPPER = [RefinementCue(text='A')]\n"
    )
    (tmp_path / "lower.py").write_text(
        "from combocizes.cues import RefinementCue\nLOWER = [RefinementCue(text='B')]\n"
    )

    bank = build_cue_bank(tmp_path)

    assert {cue.text for cue in bank} == {"A", "B"}


def test_build_cue_bank_rejects_file_with_no_cue_list(tmp_path) -> None:
    (tmp_path / "empty.py").write_text("VALUE = 1\n")

    with pytest.raises(ValueError, match="must expose exactly one list"):
        build_cue_bank(tmp_path)


def test_build_cue_bank_rejects_file_with_multiple_cue_lists(tmp_path) -> None:
    (tmp_path / "ambiguous.py").write_text(
        "from combocizes.cues import RefinementCue\n"
        "A = [RefinementCue(text='A')]\n"
        "B = [RefinementCue(text='B')]\n"
    )

    with pytest.raises(ValueError, match="must expose exactly one list"):
        build_cue_bank(tmp_path)
