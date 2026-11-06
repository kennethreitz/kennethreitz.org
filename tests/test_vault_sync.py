"""Vault sync: overrides, stale hashes, history blocks, dry-run."""

import hashlib
import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import vaultsync  # noqa: E402


def _sha(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _note(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _vault(tmp_path):
    vault = tmp_path / "vault"
    _note(
        vault / "Knowledge" / "Psychology" / "Anxiety.md",
        "---\ntype: concept\n---\n\n# Anxiety\n\n"
        "Fear without an object. Sarah takes a pill.\n\n"
        "See [[Missing Page]] and [[The Self]].\n",
    )
    _note(
        vault / "Knowledge" / "Psychology" / "Plurality.md",
        "# Plurality\n\nThis is private.\n",
    )
    _note(
        vault / "Library" / "Books" / "Books.md",
        "---\ntype: library\n---\n\n# Books\n\nThe shelf.\n",
    )
    _note(
        vault / "Library" / "Books" / "DSM-5.md",
        "---\ntype: book\nauthor: APA\nyear: 2013\n---\n\n# DSM-5\n\n"
        "> *A map, not a verdict.*\n\nA manual — not a verdict.\n",
    )
    _note(
        vault / "Library" / "Python Libraries" / "requests.md",
        "---\ndownloads: 16M+/day\n---\n\n# requests\n\n"
        "> *HTTP for Humans — the origin.*\n\n"
        "## Creation Story\n\n"
        "It started as a wrapper, then became the library.\n\n"
        "Version v2.31.0 is not the point.\n\n"
        "16 million downloads a day is a stale figure.\n\n"
        "## Usage\n\n```python\nimport requests\n```\n",
    )
    data = tmp_path / "data"
    _note(
        data / "knowledge" / "psychology" / "the-self.md",
        "# The Self\n\nWholeness.\n",
    )
    _note(
        data / "knowledge" / "psychology" / "kept.md",
        "# Kept\n\nLeave this page alone.\n",
    )
    _note(
        data / "software" / "requests.md",
        "# Requests: HTTP for Humans\n\nThe product page.\n\n## Related\n\n- Docs.\n",
    )
    _note(data / "great-books.md", "# Great Books\n\n- [*DSM-5*](https://amzn.to/3X6cnOW) — a map.\n")
    return vault, data


def _overrides(tmp_path, vault):
    raw = (vault / "Knowledge" / "Psychology" / "Anxiety.md").read_bytes()
    k = tmp_path / "kover"
    lib = tmp_path / "lover"
    lib.mkdir(parents=True, exist_ok=True)
    _note(
        k / "Psychology" / "Anxiety.md",
        "---\ntype: concept\n---\n\n# Anxiety\n\n"
        "Fear without an object. The alarm with nothing in the room.\n\n"
        "See [[Missing Page]] and [[The Self]].\n",
    )
    (k / "manifest.json").write_text(
        json.dumps({"Psychology/Anxiety.md": hashlib.sha256(raw).hexdigest()}),
        encoding="utf-8",
    )
    (lib / "manifest.json").write_text("{}\n", encoding="utf-8")
    return k, lib


def _plan(vault, data, kover, lover, **kwargs):
    return vaultsync.plan_sync(
        vault,
        data_dir=data,
        allow_partial=True,
        knowledge_overrides=kover,
        library_overrides=lover,
        extra_terms=["Sarah"],
        warn_missing_terms=False,
        **kwargs,
    )


def test_override_replaces_raw_and_links(tmp_path):
    vault, data = _vault(tmp_path)
    kover, lover = _overrides(tmp_path, vault)
    result = _plan(vault, data, kover, lover)
    page = result.writes[data / "knowledge" / "psychology" / "anxiety.md"]
    assert "Sarah" not in page
    assert "alarm with nothing in the room" in page
    assert "[[Missing Page]]" not in page
    assert "Missing Page" in page
    assert "](/knowledge/psychology/the-self)" in page
    assert "plurality" not in page.lower()
    assert all("Plurality" not in rel for rel, _reason in result.withheld) or any(
        rel.endswith("Plurality.md") for rel, _reason in result.withheld
    )
    # The sibling page is not deleted on a partial sync.
    assert data / "knowledge" / "psychology" / "kept.md" not in result.deletes


def test_stale_override_warns_and_still_publishes(tmp_path, capsys):
    vault, data = _vault(tmp_path)
    kover, lover = _overrides(tmp_path, vault)
    manifest = json.loads((kover / "manifest.json").read_text())
    manifest["Psychology/Anxiety.md"] = "0" * 64
    (kover / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
    result = _plan(vault, data, kover, lover)
    assert any("stale" in message for message in result.warnings)
    assert "Psychology/Anxiety.md" in result.stale
    page = result.writes[data / "knowledge" / "psychology" / "anxiety.md"]
    assert "Sarah" not in page
    assert "alarm with nothing" in page


def test_guard_withholds_dirty_override(tmp_path):
    vault, data = _vault(tmp_path)
    kover, lover = _overrides(tmp_path, vault)
    _note(
        kover / "Psychology" / "Anxiety.md",
        "# Anxiety\n\nWrite me at secret@example.com.\n",
    )
    result = _plan(vault, data, kover, lover)
    assert (data / "knowledge" / "psychology" / "anxiety.md") not in result.writes
    assert ("Psychology/Anxiety.md", "privacy guard") in result.withheld


def test_missing_override_withholds_raw(tmp_path):
    vault, data = _vault(tmp_path)
    kover, lover = _overrides(tmp_path, vault)
    (kover / "Psychology" / "Anxiety.md").unlink()
    result = _plan(vault, data, kover, lover)
    assert (data / "knowledge" / "psychology" / "anxiety.md") not in result.writes
    assert ("Psychology/Anxiety.md", "scrub override missing") in result.withheld
    # The raw note's private term never becomes a page.
    blob = "\n".join(result.writes.values())
    assert "Sarah takes a pill" not in blob


def test_hard_exclude_never_publishes(tmp_path):
    vault, data = _vault(tmp_path)
    kover, lover = _overrides(tmp_path, vault)
    _note(
        kover / "Psychology" / "Plurality.md",
        "# Plurality\n\nA scrubbed version that must still not publish.\n",
    )
    # Plurality is hard-excluded under its real vault path. This fixture uses
    # a short path, so also drop a note at the hard-exclude path.
    _note(
        vault / "Knowledge" / "AI" / "Archetype Map.md",
        "# Archetype Map\n\nPrivate inventory.\n",
    )
    _note(
        kover / "AI" / "Archetype Map.md",
        "# Archetype Map\n\nShould not publish.\n",
    )
    result = _plan(vault, data, kover, lover)
    assert not any("archetype-map" in str(path) for path in result.writes)
    assert ("AI/Archetype Map.md", "excluded") in result.withheld


def test_history_block_is_idempotent_and_drops_stale_figures(tmp_path):
    vault, data = _vault(tmp_path)
    kover, lover = _overrides(tmp_path, vault)
    result = _plan(vault, data, kover, lover)
    page = result.writes[data / "software" / "requests.md"]
    assert page.count("<!-- vault:history start -->") == 1
    assert "v2.31.0" not in page
    assert "16 million" not in page
    assert "It started as a wrapper" in page
    assert "## Related" in page
    assert page.index("## History") < page.index("## Related")
    # Second plan against the updated page replaces the block in place.
    data.joinpath("software/requests.md").write_text(page, encoding="utf-8")
    again = _plan(vault, data, kover, lover)
    assert again.writes[data / "software" / "requests.md"] == page


def test_dry_run_writes_nothing(tmp_path):
    vault, data = _vault(tmp_path)
    kover, lover = _overrides(tmp_path, vault)
    before = {
        path: path.read_text(encoding="utf-8")
        for path in data.rglob("*.md")
    }
    result, code = vaultsync.sync_all(
        vault,
        dry_run=True,
        allow_partial=True,
        data_dir=data,
        knowledge_overrides=kover,
        library_overrides=lover,
        extra_terms=["Sarah"],
        warn_missing_terms=False,
    )
    assert code == 0
    after = {path: path.read_text(encoding="utf-8") for path in data.rglob("*.md")}
    assert before == after
    assert result.added
    assert "DSM-5" in (data / "great-books.md").read_text(encoding="utf-8")
    # The plan would have linked it, but dry-run did not touch disk.
    assert "/library/books/dsm-5" not in (data / "great-books.md").read_text(encoding="utf-8")


def test_em_dash_becomes_prose(tmp_path):
    vault, data = _vault(tmp_path)
    kover, lover = _overrides(tmp_path, vault)
    result = _plan(vault, data, kover, lover)
    book = result.writes[data / "library" / "books" / "dsm-5.md"]
    assert "—" not in book
    assert "A manual, not a verdict." in book


def test_partial_refuses_without_flag(tmp_path):
    vault, data = _vault(tmp_path)
    kover, lover = _overrides(tmp_path, vault)
    with pytest.raises(SystemExit):
        vaultsync.plan_sync(
            vault,
            data_dir=data,
            allow_partial=False,
            min_knowledge_notes=80,
            knowledge_overrides=kover,
            library_overrides=lover,
            warn_missing_terms=False,
        )


def test_check_fails_until_applied(tmp_path):
    vault, data = _vault(tmp_path)
    kover, lover = _overrides(tmp_path, vault)
    kwargs = dict(
        allow_partial=True,
        data_dir=data,
        knowledge_overrides=kover,
        library_overrides=lover,
        extra_terms=["Sarah"],
        warn_missing_terms=False,
    )
    _result, code = vaultsync.sync_all(vault, check=True, **kwargs)
    assert code == 1
    vaultsync.apply_result(vaultsync.plan_sync(vault, **kwargs))
    _result, code = vaultsync.sync_all(vault, check=True, **kwargs)
    assert code == 0
