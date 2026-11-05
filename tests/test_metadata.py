# -*- coding: utf-8 -*-
import json
from pathlib import Path
import re

REPO_ROOT = Path(__file__).resolve().parent.parent


def test_version_parity():
    """Verify version in pyproject.toml matches ellmos-module.v2.json exactly."""
    manifest_path = REPO_ROOT / "ellmos-module.v2.json"
    assert manifest_path.is_file(), "ellmos-module.v2.json missing"
    with manifest_path.open("r", encoding="utf-8") as f:
        manifest = json.load(f)

    pyproject_path = REPO_ROOT / "pyproject.toml"
    assert pyproject_path.is_file(), "pyproject.toml missing"
    content = pyproject_path.read_text(encoding="utf-8")
    match = re.search(r'version\s*=\s*"([^"]+)"', content)
    assert match is not None, "Version not found in pyproject.toml"
    pyproject_version = match.group(1)

    assert manifest["version"] == pyproject_version
    assert manifest["version"] == "0.2.0"


def test_manifest_schema_and_boundaries():
    """Verify ellmos-module.v2.json schema, category and boundaries."""
    manifest_path = REPO_ROOT / "ellmos-module.v2.json"
    with manifest_path.open("r", encoding="utf-8") as f:
        m = json.load(f)

    assert m["schema"] == "ellmos.module.v2"
    assert m["id"] == "agents-heart"
    assert m["category"] == "control"
    assert m["kind"] == "library"
    assert m["status"] == "active"
    assert m["entrypoints"] == {"library": "agents_heart"}
    assert m["boundaries"]["network"] == "none"
    assert m["boundaries"]["data"] == "user-local"


def test_license_exists_and_is_mit():
    """Verify LICENSE file exists and specifies MIT license."""
    license_path = REPO_ROOT / "LICENSE"
    assert license_path.is_file(), "LICENSE missing"
    text = license_path.read_text(encoding="utf-8")
    assert "MIT License" in text
    assert "Copyright (c) 2026" in text


def test_todo_contains_status_table():
    """Verify TODO.md exists and contains the standard STATUS table."""
    todo_path = REPO_ROOT / "TODO.md"
    assert todo_path.is_file(), "TODO.md missing"
    content = todo_path.read_text(encoding="utf-8")
    assert "STATUS" in content.upper()
    assert "| Category" in content or "| category" in content
    assert "Audit-Datum" in content or "Audit Date" in content


def test_gitignore_contains_required_patterns():
    """Verify .gitignore contains minimum entries checked by release gates."""
    gitignore_path = REPO_ROOT / ".gitignore"
    assert gitignore_path.is_file(), ".gitignore missing"
    patterns = gitignore_path.read_text(encoding="utf-8")
    for req in ["__pycache__", "*.pyc", ".env", "*.db", ".venv/", ".idea/", ".vscode/", "data/"]:
        assert req in patterns, f"Missing required .gitignore pattern: {req}"


def test_pep561_typing_marker():
    """Verify py.typed marker is present in src/agents_heart."""
    marker_path = REPO_ROOT / "src" / "agents_heart" / "py.typed"
    assert marker_path.is_file(), "py.typed missing"


def test_no_hardcoded_personal_paths():
    """Verify zero hardcoded personal user paths in tracked sources and docs."""
    personal_pattern = re.compile(r"C:[/\\]Users[/\\](?:lukas|User)", re.IGNORECASE)
    for p in REPO_ROOT.rglob("*"):
        if p.is_dir() or ".git" in p.parts or "__pycache__" in p.parts or ".pytest_cache" in p.parts:
            continue
        text = p.read_text(encoding="utf-8", errors="ignore")
        assert not personal_pattern.search(text), f"Personal path found in {p.relative_to(REPO_ROOT)}"


def test_german_umlauts_in_docs():
    """Verify genuine German umlauts in German documentation and TODO."""
    for doc in ["README_de.md", "TODO.md"]:
        path = REPO_ROOT / doc
        assert path.is_file(), f"{doc} missing"
        content = path.read_text(encoding="utf-8")
        assert any(c in content for c in ["ä", "ö", "ü", "ß"]), f"No genuine umlauts found in {doc}"
