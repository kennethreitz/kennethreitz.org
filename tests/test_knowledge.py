"""The Knowledge section and the concept crosslinker."""

import re
from pathlib import Path

import pytest

from tuftecms.core.knowledge import KnowledgeIndex


def _write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


@pytest.fixture()
def index(tmp_path):
    data = tmp_path / "data"
    _write(data / "knowledge" / "index.md", "# Knowledge\n")
    _write(data / "knowledge" / "psychology" / "index.md", "# Psychology\n")
    _write(
        data / "knowledge" / "psychology" / "collective-unconscious.md",
        "---\naliases:\n  - Objective Psyche\n---\n\n# Collective Unconscious\n\n"
        "See [Archetypes](/knowledge/psychology/archetypes).\n",
    )
    _write(data / "knowledge" / "psychology" / "archetypes.md", "# Archetypes\n\nPatterns.\n")
    _write(data / "knowledge" / "tarot" / "the-moon.md", "# The Moon\n\nCard.\n")
    _write(data / "knowledge" / "mythology" / "hermes.md", "# Hermes\n\nMessenger.\n")
    # Ordinary site prose: "the moon" is an everyday phrase here.
    _write(
        data / "essays" / "2026-01-01-on_dreams.md",
        "# On Dreams\n\nThe Collective Unconscious speaks. Hermes too.\n\n"
        "the moon rose. the moon set. the moon again.\n",
    )
    return KnowledgeIndex(data)


def test_concepts_include_titles_and_aliases(index):
    assert "Collective Unconscious" in index.concepts
    assert "Objective Psyche" in index.concepts
    assert index.concepts["Objective Psyche"].url == "/knowledge/psychology/collective-unconscious"


def test_generic_and_collection_terms_are_skipped(index):
    assert "The Moon" not in index.concepts  # everyday phrase on this site
    assert "Knowledge" not in index.concepts


def test_links_first_mention_only(index):
    html = "<p>Hermes arrives. Hermes leaves.</p>"
    out, linked = index.link_html(html)
    assert linked == ["/knowledge/mythology/hermes"]
    assert out.count('href="/knowledge/mythology/hermes"') == 1
    assert out.startswith('<p><a href="/knowledge/mythology/hermes" class="concept-link"')


@pytest.mark.parametrize(
    "html",
    [
        "<h2>Hermes</h2>",
        "<p><a href='/x'>Hermes</a></p>",
        "<p><code>Hermes</code></p>",
        "<pre><code>Hermes</code></pre>",
        '<p>x<label for="sn">1</label><span class="sidenote">Hermes</span></p>',
        '<p><span class="marginnote">On <em>Hermes</em></span></p>',
    ],
)
def test_never_links_inside_protected_markup(index, html):
    out, linked = index.link_html(html)
    assert linked == []
    assert out == html


def test_links_resume_after_sidenote_closes(index):
    html = '<p><span class="sidenote">Hermes <span>x</span> y</span> then Hermes.</p>'
    out, linked = index.link_html(html)
    assert linked == ["/knowledge/mythology/hermes"]
    assert out.endswith('then <a href="/knowledge/mythology/hermes" class="concept-link" '
                        'title="Knowledge: Hermes">Hermes</a>.</p>')


def test_word_boundaries(index):
    out, linked = index.link_html("<p>Hermeses and HermesX and /Hermes</p>")
    assert linked == []


def test_cap_per_page(index):
    html = "<p>Hermes, Archetypes, Collective Unconscious.</p>"
    _, linked = index.link_html(html, max_links=2)
    assert len(linked) == 2


def test_does_not_link_page_to_itself(index):
    _, linked = index.link_html("<p>Hermes</p>", page_url="/knowledge/mythology/hermes")
    assert linked == []


def test_mentions_and_related(index):
    mentions = index.mentions_for("/knowledge/psychology/collective-unconscious")
    assert [m["url"] for m in mentions] == ["/essays/2026-01-01-on_dreams"]
    related = index.related_for("/knowledge/psychology/archetypes")
    assert [r["url"] for r in related] == ["/knowledge/psychology/collective-unconscious"]
    assert index.concepts_for("/essays/2026-01-01-on_dreams")[0]["title"] == "Collective Unconscious"


# --- The live section ----------------------------------------------------


def test_knowledge_index_renders(client):
    r = client.get("/knowledge")
    assert r.status_code == 200
    assert "Tarot" in r.text and "/knowledge/tarot" in r.text


def test_nav_has_knowledge(client):
    r = client.get("/")
    assert 'href="/knowledge"' in r.text
    assert "knowledge-dropdown" in r.text


def test_nested_knowledge_note_renders_with_backlinks(client):
    r = client.get("/knowledge/tarot/major-arcana/death")
    assert r.status_code == 200
    assert "Related Knowledge" in r.text
    assert "[[" not in r.text


def test_knowledge_pages_have_no_wikilinks():
    for md in Path("data/knowledge").rglob("*.md"):
        text = md.read_text(encoding="utf-8")
        assert not re.search(r"(?<!`)\[\[[^\]]+\]\](?!`)", text), md


def test_legacy_slugs_unchanged_by_knowledge(client):
    # Bare slugs keep resolving to the pages they did before /knowledge existed.
    from engine import _legacy_files
    assert all(
        not url.startswith("/knowledge/")
        for slug, url in _legacy_files.items()
        if list(Path("data").rglob(f"{slug}.md"))[:1]
        and any(p.parts[1] != "knowledge" for p in Path("data").rglob(f"{slug}.md"))
    )


def test_personal_sections_never_crosslinked():
    from tuftecms.core.knowledge import links_allowed
    assert not links_allowed("/system-777/the-triad")
    assert not links_allowed("/knowledge/tarot")
    assert links_allowed("/essays/2026-01-01-anything")
