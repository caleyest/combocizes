# Project structure

```
combocizes/
├── .claude/                  Claude Code project instructions
├── .github/
│   ├── ISSUE_TEMPLATE/       Bug report and feature request forms
│   ├── workflows/
│   │   ├── ci.yml            Ruff + pytest on every push and PR
│   │   ├── codeql.yml        Static security analysis, weekly
│   │   └── docs.yml          Render Quarto + build MkDocs → GitHub Pages
│   ├── CODEOWNERS
│   └── dependabot.yml        Weekly dependency and action updates
├── data/                     Input data, committed when small and stable
├── docs/                     MkDocs source (this site)
│   ├── how-to/               Task-oriented guides
│   └── reference/            Descriptive, factual pages
├── output/                   Script output — gitignored
├── quarto/                   .qmd reports and their rendered HTML/PDF
├── scripts/                  Runnable entry points
├── src/combocizes/           The package — all reusable logic
├── tests/                    pytest suite, mirroring src/
├── justfile                  Task runner; `just` lists every recipe
├── mkdocs.yml                Docs site config
├── pyproject.toml            Metadata, dependencies, ruff, pytest, coverage
└── uv.lock                   Pinned dependency graph — committed
```

## The three-layer split

| Layer         | Location            | Contains                                        |
| ------------- | ------------------- | ----------------------------------------------- |
| Logic         | `src/combocizes/`   | Pure, importable, tested functions               |
| Execution     | `scripts/`          | Thin orchestration — load, call, write           |
| Communication | `quarto/`, `docs/`  | Reports and prose that import from the package   |

Logic flows one way: reports and scripts import the package; the package never
imports them. When a script or report accumulates logic worth reusing, move it
into `src/` and import it back.

## Package modules

| Module      | Responsibility                                                |
| ----------- | ------------------------------------------------------------- |
| `core.py`   | Primary domain logic. **Placeholder** — replace with the real thing. |
| `utils.py`  | `PROJECT_ROOT`, `DATA_DIR`, `OUTPUT_DIR`, logging, `ensure_dir`. |

As the project grows, split `core.py` by concern rather than letting it sprawl,
and add a reference page here for each substantial new module.

## Tooling

| Tool           | Role                                          | Configured in            |
| -------------- | --------------------------------------------- | ------------------------ |
| **uv**         | Python versions, dependencies, virtualenv     | `pyproject.toml`, `uv.lock` |
| **ruff**       | Linting and formatting                        | `pyproject.toml`         |
| **pytest**     | Tests and coverage                            | `pyproject.toml`         |
| **pre-commit** | Runs ruff on staged files at commit time      | `.pre-commit-config.yaml` |
| **just**       | Task runner                                   | `justfile`               |
| **Quarto**     | Executable reports → HTML/PDF/slides          | `quarto/_quarto.yaml`    |
| **MkDocs**     | This documentation site                       | `mkdocs.yml`             |

Ruff is set to a 100-character line length targeting Python 3.12, with the
pycodestyle, pyflakes, isort, bugbear, and pyupgrade rule sets enabled.

## Conventions

- **Type hints on function signatures.** Ruff won't enforce it; do it anyway.
- **Google-style docstrings** with `Args`, `Returns`, and `Raises`.
- **Tests mirror source** — `src/combocizes/core.py` is covered by
  `tests/test_core.py`.
- **Absolute paths via `utils`** — never a bare relative path.
- **`uv.lock` is committed** so CI and every clone resolve identically.
