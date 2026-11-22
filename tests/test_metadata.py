import json
import re
import tomllib
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def _load_pyproject() -> dict:
    return tomllib.loads((REPO_ROOT / "pyproject.toml").read_text(encoding="utf-8"))


def test_version_parity():
    """Verify version in pyproject.toml matches ellmos-module.v2.json exactly."""
    manifest_path = REPO_ROOT / "ellmos-module.v2.json"
    assert manifest_path.is_file(), "ellmos-module.v2.json missing"
    with manifest_path.open("r", encoding="utf-8") as f:
        manifest = json.load(f)

    data = _load_pyproject()
    pyproject_version = data["project"]["version"]
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
    assert m["visibility"] == "private"
    assert m["entrypoints"] == {"library": "agents_heart"}
    assert m["boundaries"]["network"] == "none"
    assert m["boundaries"]["data"] == "user-local"
    assert set(m["boundaries"]["platforms"]) == {"windows", "macos", "linux"}
    assert m["source_of_truth"]["repository"] == "https://github.com/ellmos-ai/agents-heart"


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
    required = [
        "__pycache__",
        "*.pyc",
        ".env",
        "*.db",
        ".venv/",
        ".idea/",
        ".vscode/",
        "data/",
        ".pytest_temp/",
        "*MARKETING-LOG.txt",
        "LOCK-CACHE.*",
    ]
    for req in required:
        assert req in patterns, f"Missing required .gitignore pattern: {req}"


def test_pep561_typing_marker():
    """Verify py.typed marker is present in src/agents_heart."""
    marker_path = REPO_ROOT / "src" / "agents_heart" / "py.typed"
    assert marker_path.is_file(), "py.typed missing"


def test_no_hardcoded_personal_paths():
    """Verify zero hardcoded personal user paths in tracked sources and docs."""
    personal_pattern = re.compile(r"C:[/\\]Users[/\\](?:lukas|User)", re.IGNORECASE)
    for p in REPO_ROOT.rglob("*"):
        if (
            p.is_dir()
            or ".git" in p.parts
            or "__pycache__" in p.parts
            or ".pytest_cache" in p.parts
            or ".pytest_temp" in p.parts
            or ".ruff_cache" in p.parts
        ):
            continue
        text = p.read_text(encoding="utf-8", errors="ignore")
        rel_path = p.relative_to(REPO_ROOT)
        assert not personal_pattern.search(text), f"Personal path found in {rel_path}"


def test_german_umlauts_in_docs():
    """Verify genuine German umlauts in German documentation and TODO."""
    for doc in ["README_de.md", "TODO.md", "CONTRIBUTING.md", "SECURITY.md", "CODE_OF_CONDUCT.md"]:
        path = REPO_ROOT / doc
        assert path.is_file(), f"{doc} missing"
        content = path.read_text(encoding="utf-8")
        assert any(c in content for c in ["ä", "ö", "ü", "ß"]), f"No genuine umlauts in {doc}"


def test_pep621_and_pep639_metadata_without_duplicate_osi_classifier():
    """Verify PEP 621 URLs/keywords and PEP 639 license without OSI classifier."""
    data = _load_pyproject()
    project = data["project"]
    assert project["license"] == "MIT"
    assert project["license-files"] == ["LICENSE"]
    classifiers = project["classifiers"]
    assert not any(c.startswith("License ::") for c in classifiers)
    assert "Programming Language :: Python :: 3.13" in classifiers
    assert "keywords" in project and len(project["keywords"]) >= 5
    urls = project["urls"]
    for key in ["Homepage", "Repository", "Changelog", "Contributing", "Security"]:
        assert key in urls, f"Missing [project.urls] key: {key}"


def test_pytest_config_has_no_relative_basetemp():
    """Ensure addopts never sets a relative --basetemp (T-20261114-932985855)."""
    data = _load_pyproject()
    pytest_cfg = data["tool"]["pytest"]["ini_options"]
    addopts = pytest_cfg.get("addopts", [])
    addopts_str = " ".join(addopts) if isinstance(addopts, list) else str(addopts)
    assert "--basetemp" not in addopts_str
    assert ".pytest_temp" in pytest_cfg.get("norecursedirs", [])


def test_ci_workflow_and_dependabot_present():
    """Verify cross-OS CI matrix workflow, Dependabot, and issue templates exist."""
    ci_path = REPO_ROOT / ".github" / "workflows" / "ci.yml"
    assert ci_path.is_file(), ".github/workflows/ci.yml missing"
    ci_text = ci_path.read_text(encoding="utf-8")
    for token in [
        "workflow_dispatch",
        "contents: read",
        "ubuntu-latest",
        "windows-latest",
        "macos-latest",
        "3.11",
        "3.12",
        "3.13",
        "ruff check .",
        "pytest -ra -v",
    ]:
        assert token in ci_text, f"Missing CI token: {token}"

    dependabot_path = REPO_ROOT / ".github" / "dependabot.yml"
    assert dependabot_path.is_file(), ".github/dependabot.yml missing"
    dep_text = dependabot_path.read_text(encoding="utf-8")
    assert "github-actions" in dep_text and "pip" in dep_text

    for tmpl in ["config.yml", "bug_report.md", "feature_request.md"]:
        assert (REPO_ROOT / ".github" / "ISSUE_TEMPLATE" / tmpl).is_file()


def test_governance_and_llm_entrypoint_files_present():
    """Verify required governance and LLM entrypoint files exist."""
    for rel in [
        "README.md",
        "README_de.md",
        "LICENSE",
        "CHANGELOG.md",
        "CODE_OF_CONDUCT.md",
        "SECURITY.md",
        "CONTRIBUTING.md",
        "SKILL.md",
        "llms.txt",
        "llm.txt",
    ]:
        path = REPO_ROOT / rel
        assert path.is_file(), f"Missing required file: {rel}"


def test_changelog_unreleased_entry_present():
    """Verify CHANGELOG.md documents unreleased hygiene changes."""
    changelog = (REPO_ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
    assert "## [Unreleased]" in changelog
