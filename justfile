
# Default recipe to 'help' to display this help screen
default: help

# ==============================================================================
# Configuration & Variables
# ==============================================================================

set ignore-comments := true

# ==============================================================================
# Setup & Maintenance
# ==============================================================================

# Install/refresh all Python dependencies using uv.
[group('maintenance')]
setup:
    @echo "{{ BOLD }}--- Installing/ validating dependencies ---{{ NORMAL }}"
    @uv sync --managed-python --all-groups --all-extras --all-packages --compile-bytecode

# Clean up all caches, build artifacts, and the venv
[group('maintenance')]
clean:
    @echo "{{ BOLD }}--- Removing .venv/, build/, dist/ directories, and other caches ---{{ NORMAL }}"
    @rm -rf .venv/ build/ dist/ .pytest_cache/ .mypy_cache/ .hypothesis/ .ruff_cache/
    @echo "{{ BOLD }}--- Removing Python bytecode and compiled extensions ---{{ NORMAL }}"
    @find . -type f -name '*.py[co]' -delete \
        -o -type d -name __pycache__ -exec rm -rf {} + \
        -o -type f -name '*.so' -delete
    # @just clean-stubs

# ==================================
# Dev & Build
# ==================================

# Update python packages in .venv and uv.lock
[group('dev')]
update-py: setup
    @echo "{{ BOLD }}--- Upgrading Python dependencies ---{{ NORMAL }}"
    @uv sync --managed-python --all-groups --all-extras --all-packages --compile-bytecode --upgrade
    @just stubs

# Build all packages
[group('dev')]
build: setup
    @echo "{{ BOLD }}--- Building all packages ---{{ NORMAL }}"
    @uv build --all-packages

# Execute pytests
[group('dev')]
test: setup
    @echo "{{ BOLD }}--- Running all tests ---{{ NORMAL }}"
    @uv run pytest

# ==============================================================================
# Code Quality & Formatting
# ==============================================================================

# Run all lint checks
[group('lint')]
lint: setup
    @echo "{{ BOLD }}--- Running Python linter (Ruff) ---{{ NORMAL }}"
    @uv run ruff check
    @echo "{{ BOLD }}--- Running Misc linter (dprint) ---{{ NORMAL }}"
    @dprint check --allow-no-files
    @just --fmt --unstable --check

# Attempt to fix all lints
[group('lint')]
lint-fix: setup
    @echo "{{ BOLD }}--- Running Python lint fix (Ruff) ---{{ NORMAL }}"
    @uv run ruff check --fix
    @just fmt

# Format all code
[group('lint')]
fmt: setup
    @echo "{{ BOLD }}--- Formatting Python ---{{ NORMAL }}"
    @uv run ruff format --quiet
    @echo "{{ BOLD }}--- Formatting Misc ---{{ NORMAL }}"
    @dprint fmt
    @just --fmt --unstable

# Run all code formatting and quality checks
[group('lint')]
pre-commit: fmt lint test

# Display this help screen
help:
    @just --list
