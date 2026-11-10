"""Smoke tests for the site's page routes."""

import pytest

KEY_PAGES = [
    "/",
    "/archive",
    "/archive/by-length",
    "/archive/sidenotes",
    "/archive/outlines",
    "/archive/quotes",
    "/archive/connections",
    "/archive/terms",
    "/archive/themes",
    "/archive/graph",
    "/search",
    "/directory",
    "/themes",
    "/essays",
    "/software",
    "/music",
    "/photography",
    "/values",
    "/contact",
    "/mental-health",
]

ARCHIVE_ALIASES = ["sidenotes", "outlines", "quotes", "connections", "terms", "graph"]


@pytest.mark.parametrize("path", KEY_PAGES)
def test_key_page_renders(client, path):
    r = client.get(path)
    assert r.status_code == 200
    assert "<html" in r.text.lower()


def test_homepage_content(client):
    r = client.get("/")
    assert r.status_code == 200
    assert "Kenneth Reitz" in r.text
    # Homepage-specific meta description, not the site-wide default.
    assert 'name="description" content="Kenneth Reitz — creator of Requests' in r.text


def test_homepage_recent_posts_have_dates(client):
    r = client.get("/")
    assert r.text.count('class="recent-post"') == 5
    assert r.text.count('class="recent-post-date"') == 5


@pytest.mark.parametrize("page", ARCHIVE_ALIASES)
def test_bare_archive_alias_redirects(client, page):
    r = client.get(f"/{page}", follow_redirects=False)
    assert r.status_code == 308
    assert r.headers["location"] == f"/archive/{page}"


def test_random_redirects_to_a_post(client):
    r = client.get("/random", follow_redirects=False)
    assert r.status_code == 307
    assert r.headers["location"].startswith("/essays/")


def test_trailing_slash_redirects(client):
    r = client.get("/archive/", follow_redirects=False)
    assert r.status_code == 307
    assert r.headers["location"] == "/archive"


def test_unknown_page_is_404(client):
    r = client.get("/definitely-not-a-real-page-xyz")
    assert r.status_code == 404
    assert "Page not found" in r.text


def test_social_url_matches_the_page(client):
    home = client.get("/")
    assert 'property="og:url" content="https://kennethreitz.org"' in home.text
    contact = client.get("/contact")
    assert 'property="og:url" content="https://kennethreitz.org/contact"' in contact.text
    assert 'rel="canonical" href="https://kennethreitz.org/contact"' in contact.text


def test_favicon_is_the_k_mark(client):
    home = client.get("/")
    assert 'href="/static/images/favicon-32.png"' in home.text
    assert 'href="data:,"' not in home.text
    icon = client.get("/favicon.ico")
    assert icon.status_code == 200
    assert icon.content[:8] == b"\x89PNG\r\n\x1a\n"


def test_analytics_snippet_stays(client):
    r = client.get("/")
    assert "analytics.kennethreitz.org/script.js" in r.text
    assert "41b1fd15-82b1-4211-aeff-b3caa2d50ea3" in r.text
