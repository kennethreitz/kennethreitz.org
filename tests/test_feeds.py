"""Tests for RSS, sitemap, and robots.txt."""

import xml.etree.ElementTree as ET


def test_feed_xml(client):
    r = client.get("/feed.xml")
    assert r.status_code == 200
    root = ET.fromstring(r.text)
    items = root.findall(".//item")
    assert len(items) >= 10
    first = items[0]
    assert first.findtext("title")
    assert first.findtext("link", "").startswith("https://kennethreitz.org/")


def test_sitemap_xml(client):
    r = client.get("/sitemap.xml")
    assert r.status_code == 200
    root = ET.fromstring(r.text)
    ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    locs = [el.text for el in root.findall(".//sm:loc", ns)]
    assert len(locs) > 200
    assert all(loc.startswith("https://kennethreitz.org") for loc in locs)


def test_robots_txt(client):
    r = client.get("/robots.txt")
    assert r.status_code == 200
    assert "Sitemap: https://kennethreitz.org/sitemap.xml" in r.text
