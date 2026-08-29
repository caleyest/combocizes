from combocizes.utils import PROJECT_ROOT, ensure_dir, get_logger


def test_project_root_points_at_repo() -> None:
    assert (PROJECT_ROOT / "pyproject.toml").is_file()


def test_get_logger_is_idempotent() -> None:
    first = get_logger("combocizes.test")
    second = get_logger("combocizes.test")

    assert first is second
    assert len(first.handlers) == 1


def test_ensure_dir_creates_and_returns(tmp_path) -> None:
    target = tmp_path / "nested" / "dir"

    assert ensure_dir(target) == target
    assert target.is_dir()
