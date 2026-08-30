# Project Guidelines

## General

- Combocizes builds full-body workout class scripts — combinations of dumbbell,
  bodyweight, and resistance band exercises — from a structured exercise
  dictionary, for instructors and coaches planning class sequences.
- Source code lives in `src/combocizes/`, runnable entry points in `scripts/`,
  Quarto reports in `quarto/`, prose documentation in `docs/`.
- Logic flows one way: scripts and reports import the package; the package never
  imports them. When a script or report accumulates reusable logic, move it into
  `src/combocizes/` and import it back.

## Code Style

- Use polars over pandas for data manipulation.
- Type hints on all function signatures.
- Google-style docstrings with `Args`, `Returns`, and `Raises`.
- Create reusable functions for repeatable tasks — don't duplicate logic.
- Keep functions focused and single-purpose.
- Resolve paths through `combocizes.utils` (`PROJECT_ROOT`, `DATA_DIR`,
  `OUTPUT_DIR`) — never hardcode a relative path.
- Ruff: 100-character lines, target py312.

## Testing

- Tests mirror source: `src/combocizes/core.py` → `tests/test_core.py`.
- Cover the error paths, not just the happy path.
- Run via `just test`; run everything with `just check` before pushing.

## Documentation

- `docs/` follows the [Diátaxis](https://diataxis.fr/) framework.
  - **How-to guides** (`docs/how-to/`): step-by-step instructions for tasks.
  - **Reference** (`docs/reference/`): technical descriptions of modules and processes.
- When a substantial new module lands in `src/combocizes/`, add a corresponding
  reference page and link it from `mkdocs.yml`'s `nav:`.
- Keep docs concise and in sync with the code.

## Quarto

- Reports live in `quarto/` as `.qmd` files and import from `combocizes`.
- `quarto/_quarto.yaml` sets `echo: false` and `warning: false` globally;
  override per chunk with `#| echo: true`.
- Label figures `fig-*` and tables `tbl-*` so they can be cross-referenced.
- Prefer importing package functions over pasting logic into a chunk.

## Commands

- Dependencies: `uv` — `just sync`
- Run a script: `just run <name>`
- Tests: `just test` · everything: `just check`
- Render a report: `just render-one <name>` · preview: `just preview <name>`
- Docs site: `just docs-serve`
- GitHub CLI (`gh`) is installed but not on PATH in tool shells — invoke it via
  its full path: `C:\Program Files\GitHub CLI\gh.exe`. Use it for repo tasks
  (issues, PRs) instead of assuming it's unavailable.
