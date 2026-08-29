# combocizes task runner
# Install just: https://github.com/casey/just#installation

set windows-shell := ["powershell", "-NoLogo", "-NoProfile", "-Command"]
set dotenv-load := true

# List available recipes
default:
    @just --list

# --- Development ---

# Install/sync the environment from uv.lock
sync:
    uv sync

# Install the git pre-commit hook (run once after cloning)
install-hooks:
    uv run pre-commit install

# Run pre-commit hooks and the test suite
check:
    uv run pre-commit run --all-files
    uv run pytest

# Run the test suite
test:
    uv run pytest

# Run tests with a coverage report
coverage:
    uv run pytest --cov=combocizes --cov-report=term-missing

# Lint
lint:
    uv run ruff check .

# Auto-format
format:
    uv run ruff format .

# --- Scripts ---

# Run a script: just run run_example
run name:
    uv run python scripts/{{name}}.py

# --- Quarto ---

# Render every .qmd in quarto/ to HTML
render:
    uv run quarto render quarto/ --to html

# Render every .qmd in quarto/ to PDF (requires TinyTeX: quarto install tinytex)
render-pdf:
    uv run quarto render quarto/ --to pdf

# Render one report to HTML: just render-one report
render-one name:
    uv run quarto render quarto/{{name}}.qmd --to html

# Render one report to PDF: just render-one-pdf report
render-one-pdf name:
    uv run quarto render quarto/{{name}}.qmd --to pdf

# Live-preview one report while you edit: just preview report
preview name:
    uv run quarto preview quarto/{{name}}.qmd

# --- Documentation ---

# Serve the docs site locally with live reload
docs-serve:
    uv run mkdocs serve

# Build the docs site to site/
docs-build:
    uv run mkdocs build --strict

# Build docs and copy rendered Quarto reports in, mirroring the CI deploy
docs-full: render docs-build
    New-Item -ItemType Directory -Force site/quarto | Out-Null
    Copy-Item quarto/*.html site/quarto/
