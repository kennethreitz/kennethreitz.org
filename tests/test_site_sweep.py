"""Every URL the sitemap advertises must actually resolve.

This is the safety net for sweeping changes: if a refactor breaks any
page on the site, this test names it.
"""

import xml.etree.ElementTree as ET

SITE = "https://kennethreitz.org"


def test_every_sitemap_url_resolves(client):
    r = client.get("/sitemap.xml")
    assert r.status_code == 200
    ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    locs = [el.text for el in ET.fromstring(r.text).findall(".//sm:loc", ns)]
    paths = [loc.removeprefix(SITE) or "/" for loc in locs]
    assert len(paths) > 200

    failures = []
    for path in paths:
        resp = client.get(path)
        if resp.status_code != 200:
            failures.append(f"{path} -> {resp.status_code}")

    assert not failures, (
        f"{len(failures)}/{len(paths)} sitemap URLs broken:\n" + "\n".join(failures)
    )
