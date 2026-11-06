"""Knowledge notes on the cross-reference graph."""

from tuftecms.core.archive_graph import EXCLUDED, build_graph, to_archive_graph


def _write(root, rel, text):
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _corpus(root):
    _write(root, "knowledge/tarot/index.md", "# Tarot\n\nSee [The Magician](/knowledge/tarot/major-arcana/the-magician).\n")
    _write(root, "knowledge/tarot/major-arcana/the-magician.md", """# The Magician

## Correspondence

| Attribute | Value |
| --- | --- |
| **Hebrew letter** | Beth: the house. |
| **Planet** | Mercury, the messenger. |

See [Death](/knowledge/tarot/major-arcana/death).
""")
    _write(root, "knowledge/tarot/major-arcana/death.md", "# Death\n\nAn ending.\n")
    _write(root, "knowledge/hebrew-letters/index.md", "# Hebrew Letters\n")
    _write(root, "knowledge/hebrew-letters/bet.md", """# Bet

The letter.
""")
    _write(root, "knowledge/astrology/planets/mercury-astrology.md", "# Mercury\n\nThe messenger.\n")
    _write(root, "knowledge/table-of-correspondences.md", """# Table of Correspondences

| Trump | Hebrew Letter | Planet |
| --- | --- | --- |
| [The Magician](/knowledge/tarot/major-arcana/the-magician) | [Beth](/knowledge/hebrew-letters/bet) | [Mercury](/knowledge/astrology/planets/mercury-astrology) |
""")
    _write(root, "themes/index.md", "# Themes\n\n- [For Humans](/themes/for-humans-philosophy)\n")
    _write(root, "themes/for-humans-philosophy.md", "# For Humans\n\nA theme.\n")
    _write(root, "themes/mental-health.md", "# Mental Health Theme\n\nNot the personal page.\n")
    _write(root, "essays/index.md", "# Essays\n")
    _write(root, "essays/2026-01-01-for_humans.md", """---
themes:
  - for-humans-philosophy
tags:
  - requests
series: tools
---
# For Humans

See [Tarot](/knowledge/tarot) and [Worldview](/worldview).
""")
    _write(root, "essays/2026-02-01-another_tool.md", """---
series: tools
tags: requests
---
# Another Tool
""")
    _write(root, "worldview.md", "# Worldview\n\nA way of seeing.\n")
    _write(root, "values.md", "# Values\n\nSee [Worldview](/worldview).\n")
    _write(root, "family.md", "# Family\n\nPrivate.\n")
    _write(root, "mental-health.md", "# Mental Health\n")
    _write(root, "contact.md", "# Contact\n")
    _write(root, "system-777/violet.md", "# Violet\n\nSee [Worldview](/worldview).\n")


def _edge(graph, source, target):
    for edge in graph["edges"]:
        if edge["source"] == source and edge["target"] == target:
            return edge
    return None


def test_exclusion_list_is_config():
    assert isinstance(EXCLUDED, tuple)
    for name in ("system-777", "family", "mental-health", "contact"):
        assert name in EXCLUDED


def test_graph_reads_links_frontmatter_and_correspondences(tmp_path):
    _corpus(tmp_path)
    graph = build_graph(tmp_path)
    urls = {node["url"] for node in graph["nodes"]}

    assert "/worldview" in urls
    assert "/values" in urls
    assert "/themes/mental-health" in urls
    assert "/family" not in urls
    assert "/mental-health" not in urls
    assert "/contact" not in urls
    assert not any(url.startswith("/system-777") for url in urls)

    magician = "/knowledge/tarot/major-arcana/the-magician"
    bet = "/knowledge/hebrew-letters/bet"
    mercury = "/knowledge/astrology/planets/mercury-astrology"
    letter = _edge(graph, magician, bet)
    assert letter is not None
    assert "correspondence" in letter["kinds"]
    assert any("hebrew" in label.lower() for label in letter["labels"])
    planet = _edge(graph, magician, mercury)
    assert planet is not None and "correspondence" in planet["kinds"]

    death = _edge(graph, magician, "/knowledge/tarot/major-arcana/death")
    assert death is not None and "link" in death["kinds"]
    # A domain index pointing at its own card is containment, not a relationship.
    assert _edge(graph, "/knowledge/tarot", magician) is None

    essay = "/essays/2026-01-01-for_humans"
    theme = _edge(graph, essay, "/themes/for-humans-philosophy")
    assert theme is not None and "theme" in theme["kinds"]
    assert _edge(graph, essay, "/knowledge/tarot")["kinds"] == ["link"]
    series = _edge(graph, essay, "/essays/2026-02-01-another_tool")
    assert series is not None and "series" in series["kinds"]

    tagged = next(node for node in graph["nodes"] if node["url"] == essay)
    assert "requests" in tagged["tags"]
    # The tag does not name a page, so it stays on the node instead of inventing one.
    assert not any(node["title"].lower() == "requests" for node in graph["nodes"])

    tarot = next(node for node in graph["nodes"] if node["url"] == "/knowledge/tarot")
    assert tarot["kind"] == "domain" and tarot["overview"] is True
    assert next(node for node in graph["nodes"] if node["url"] == magician)["overview"] is False
    assert next(node for node in graph["nodes"] if node["url"] == "/essays")["kind"] == "section"
    assert "/worldview" in {node["url"] for node in graph["nodes"] if node["section"] == "pages"}


def test_new_page_appears_without_a_code_change(tmp_path):
    _corpus(tmp_path)
    before = {node["url"] for node in build_graph(tmp_path)["nodes"]}
    _write(tmp_path, "poetry/a-new-poem.md", "# A New Poem\n\nFresh.\n")
    after = {node["url"] for node in build_graph(tmp_path)["nodes"]}
    assert "/poetry/a-new-poem" not in before
    assert "/poetry/a-new-poem" in after


def test_exclusion_list_can_be_changed(tmp_path):
    _corpus(tmp_path)
    opened = build_graph(tmp_path, excluded=())
    assert any(node["url"] == "/family" for node in opened["nodes"])
    quiet = build_graph(tmp_path, excluded=("themes",))
    assert not any(node["section"] == "themes" for node in quiet["nodes"])
    assert quiet["excluded"] == ["themes"]


def test_archive_graph_includes_knowledge_pages(tmp_path):
    _corpus(tmp_path)
    archive = to_archive_graph(build_graph(tmp_path))
    by_id = {node["id"]: node for node in archive["nodes"]}
    assert by_id["knowledge/tarot/major-arcana/the-magician"]["category"] == "knowledge"
    assert by_id["knowledge/hebrew-letters/bet"]["url"] == "/knowledge/hebrew-letters/bet"
    pairs = {(edge["source"], edge["target"]) for edge in archive["edges"]}
    assert ("knowledge/tarot/major-arcana/the-magician", "knowledge/hebrew-letters/bet") in pairs
    assert ("essays/2026-01-01-for_humans", "worldview") in pairs
    assert "system-777/violet" not in by_id
    for edge in archive["edges"]:
        assert edge["source"] in by_id
        assert edge["target"] in by_id


def test_ontologies_route_is_gone(client):
    assert client.get("/ontologies").status_code == 404
    assert client.get("/ontologies/data").status_code == 404
    assert 'href="/ontologies"' not in client.get("/").text
    assert 'href="/ontologies"' not in client.get("/archive/graph").text


def test_archive_graph_now_contains_knowledge(client):
    payload = client.get("/archive/graph/data").json()
    nodes = {node["id"]: node for node in payload["nodes"]}
    assert nodes["knowledge/philosophy/materialism"]["category"] == "knowledge"
    assert nodes["knowledge/philosophy/materialism"]["url"] == "/knowledge/philosophy/materialism"
    pairs = {(edge["source"], edge["target"]) for edge in payload["edges"]}
    assert any(source.startswith("knowledge/") and target.startswith("knowledge/") for source, target in pairs)
    for edge in payload["edges"]:
        assert edge["source"] in nodes
        assert edge["target"] in nodes
        assert "link_text" in edge
