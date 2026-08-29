# Contributing

## Setup

Install Git, [uv](https://docs.astral.sh/uv/), [just](https://just.systems), and
[Quarto](https://quarto.org), then:

```powershell
uv sync
just install-hooks
```

Full walkthrough: [Environment setup](docs/how-to/environment-setup.md).

## Workflow

1. Branch off `main`: `git switch -c feature/short-description`
2. Make the change. Put reusable logic in `src/combocizes/`, not in a script or
   a report.
3. Add or update tests in `tests/`.
4. Update `docs/` if you changed a process or added a module.
5. Run `just check` — this is exactly what CI runs.
6. Open a PR and fill in the template.

## Standards

- **Type hints** on every function signature.
- **Google-style docstrings** with `Args`, `Returns`, and `Raises`.
- **polars over pandas** for data manipulation.
- **Ruff** handles linting and formatting — 100-character lines, py312 target.
  The pre-commit hook fixes what it can; if it rewrites a file the commit
  aborts, so re-stage and commit again.
- **Absolute paths** via `combocizes.utils`, never bare relative paths.

## Tests

```powershell
just test       # fast
just coverage   # with a line-by-line coverage report
```

Test files mirror source files: `src/combocizes/core.py` is covered by
`tests/test_core.py`. Cover error paths, not just the happy path.

## Dependencies

Add with `uv add <package>` (or `uv add --dev <package>` for tooling). Both
update `pyproject.toml` and `uv.lock` — **commit the lockfile**, it's what keeps
CI and every clone resolving identically.

## Documentation

`docs/` follows [Diátaxis](https://diataxis.fr/):

- `docs/how-to/` — task-oriented, step-by-step
- `docs/reference/` — descriptive and factual

Preview locally with `just docs-serve`. New pages must be added to `nav:` in
`mkdocs.yml`, or `mkdocs build --strict` fails in CI.

## Reports

Quarto reports live in `quarto/`. See
[Creating Quarto reports](docs/how-to/creating-quarto-reports.md). Reports
should import from `combocizes` rather than defining logic inline.

## Commits

Short imperative subject lines, optionally prefixed by area:

```
add rolling-window summariser
docs: clarify PDF rendering prerequisites
ci: pin codecov action to v5
```
