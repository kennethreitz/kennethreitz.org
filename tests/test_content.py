"""Tests for markdown content rendering and legacy URL redirects."""

import pytest


@pytest.fixture(scope="module")
def recent_posts(client):
    r = client.get("/api/blog")
    assert r.status_code == 200
    items = r.json()["items"]
    assert items, "blog cache came back empty"
    return items[:5]


def test_recent_essays_render(client, recent_posts):
    for post in recent_posts:
        r = client.get(post["url"])
        assert r.status_code == 200, f"{post['url']} -> {r.status_code}"
        assert post["title"] in r.text


def test_raw_markdown_source_is_served(client, recent_posts):
    r = client.get(recent_posts[0]["url"] + ".md")
    assert r.status_code == 200
    assert "# " in r.text


def test_legacy_bare_slug_redirects(client, recent_posts):
    # Strip the date prefix off a real essay URL and expect a 301 back to it.
    url = recent_posts[0]["url"]
    slug = url.rsplit("/", 1)[-1].split("-", 3)[-1]
    r = client.get(f"/{slug}", follow_redirects=False)
    assert r.status_code == 301
    assert r.headers["location"] == url


def test_legacy_date_path_redirects(client, recent_posts):
    # Old-style /essays/YYYY/MM/DD/slug URLs resolve to the current scheme.
    url = recent_posts[0]["url"]
    stem = url.rsplit("/", 1)[-1]
    year, month, day, slug = stem.split("-", 3)
    r = client.get(f"/essays/{year}/{month}/{day}/{slug}", follow_redirects=False)
    assert r.status_code == 301
    assert r.headers["location"] == url


def test_essay_page_has_metadata(client, recent_posts):
    r = client.get(recent_posts[0]["url"])
    assert 'property="og:title"' in r.text
    assert 'rel="canonical"' in r.text


def test_essay_has_chronological_nav(client, recent_posts):
    # An essay in the middle of the timeline links both neighbors.
    r = client.get(recent_posts[1]["url"])
    assert r.status_code == 200
    assert 'class="post-nav"' in r.text
    assert "Older" in r.text
    assert "Newer" in r.text
