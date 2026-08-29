# Environment setup

One-time setup. Everything after this is a `just` recipe.

## 1. Install the toolchain

| Tool       | Purpose                              | Install (Windows)                                           |
| ---------- | ------------------------------------ | ----------------------------------------------------------- |
| **Git**    | Version control                      | `winget install Git.Git`                                    |
| **uv**     | Python + dependency management       | `winget install astral-sh.uv`                               |
| **just**   | Task runner (reads the `justfile`)   | `winget install Casey.Just`                                 |
| **Quarto** | Renders `.qmd` reports               | `winget install Posit.Quarto`                               |

On macOS or Linux, `brew install git uv just quarto` covers all four.

!!! note "Restart your shell"
    `winget` updates `PATH` for *new* shells only. Close and reopen your
    terminal (and VS Code) before the next step, or the commands won't be found.

Verify:

```powershell
git --version; uv --version; just --version; quarto --version
```

## 2. Create the environment

`uv` reads `pyproject.toml` and `uv.lock`, downloads the right Python, and
builds a `.venv/` — no manual virtualenv step:

```powershell
uv sync
```

This installs runtime dependencies, the `dev` group, and `combocizes` itself in
editable mode, so edits under `src/` take effect immediately.

## 3. Install the pre-commit hook

```powershell
just install-hooks
```

Ruff now lints and formats staged files on every `git commit`. If a hook
rewrites a file the commit aborts — re-stage and commit again.

## 4. Configure secrets (optional)

```powershell
Copy-Item .env.example .env
```

Fill in any API keys. `.env` is gitignored; `just` loads it automatically, and
`python-dotenv` picks it up inside scripts and notebooks.

## 5. Confirm it works

```powershell
just check
```

Green output means pre-commit and the test suite both pass — you're set.

## PDF rendering (optional)

Quarto needs a LaTeX distribution for `--to pdf`. Install the bundled one once:

```powershell
quarto install tinytex
```

HTML rendering works without it.
