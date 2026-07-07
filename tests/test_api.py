"""Tests for the JSON API endpoints."""


def test_api_blog(client):
    r = client.get("/api/blog")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] > 100
    post = data["items"][0]
    for field in ("title", "url", "date", "category"):
        assert post[field]


def test_api_blog_is_sorted_newest_first(client):
    items = client.get("/api/blog").json()["items"]
    dates = [p["date"] for p in items]
    assert dates == sorted(dates, reverse=True)


def test_api_search(client):
    r = client.get("/api/search", params={"q": "requests"})
    assert r.status_code == 200
    data = r.json()
    assert data["query"] == "requests"
    assert data["total"] > 0
    assert data["results"][0]["url"]


def test_api_search_autocomplete(client):
    r = client.get("/api/search/autocomplete", params={"q": "req"})
    assert r.status_code == 200


def test_api_themes(client):
    r = client.get("/api/themes")
    assert r.status_code == 200


def test_api_icon(client):
    post = client.get("/api/blog").json()["items"][0]
    r = client.get(f"/api/icon{post['url']}")
    assert r.status_code == 200
    data = r.json()
    assert data["success"] is True
    assert data["icon"].startswith("data:image/svg+xml;base64,")


def test_api_fortune(client):
    r = client.get("/api/fortune")
    assert r.status_code == 200


def test_api_directory_tree(client):
    r = client.get("/api/directory-tree")
    assert r.status_code == 200
