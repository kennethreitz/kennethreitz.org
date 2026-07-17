"""Regression tests for bounded, disk-backed media generation."""

import io
from pathlib import Path

from PIL import Image

import engine


def test_thumbnail_is_generated_once_and_then_served_from_cache(
    client, monkeypatch, tmp_path
):
    data_dir = tmp_path / "data"
    cache_dir = tmp_path / "thumbs"
    source = data_dir / "gallery" / "large.jpg"
    source.parent.mkdir(parents=True)
    Image.new("RGB", (1600, 1000), "navy").save(source)

    monkeypatch.setattr(engine, "DATA_DIR", data_dir)
    monkeypatch.setattr(engine, "_THUMB_DIR", cache_dir)
    original = engine._make_thumbnail
    calls = []

    def tracked_make_thumbnail(*args):
        calls.append(args)
        return original(*args)

    monkeypatch.setattr(engine, "_make_thumbnail", tracked_make_thumbnail)

    first = client.get("/thumb/gallery/large.jpg?w=640")
    second = client.get("/thumb/gallery/large.jpg?w=640")

    assert first.status_code == 200
    assert first.headers["x-media-cache"] == "miss"
    assert second.status_code == 200
    assert second.headers["x-media-cache"] == "hit"
    assert len(calls) == 1
    with Image.open(io.BytesIO(second.content)) as thumbnail:
        assert thumbnail.width == 640


def test_thumbnail_cache_key_does_not_depend_on_source_mtime(tmp_path):
    source = tmp_path / "large.jpg"
    source.write_bytes(b"image")

    first = engine._thumbnail_cache_path("gallery/large.jpg", source, 640)
    source.touch()
    second = engine._thumbnail_cache_path("gallery/large.jpg", source, 640)

    assert first == second


def test_pdf_is_generated_once_and_then_served_from_cache(
    client, monkeypatch, tmp_path
):
    data_dir = tmp_path / "data"
    pdf_dir = tmp_path / "pdfs"
    source = data_dir / "article.md"
    source.parent.mkdir(parents=True)
    source.write_text("# Cached article\n\nA small test document.\n")

    monkeypatch.setattr(engine, "DATA_DIR", data_dir)
    monkeypatch.setattr(engine, "_PDF_DIR", pdf_dir)
    calls = []

    def fake_make_pdf(md_path, dest):
        calls.append(md_path)
        Path(dest).parent.mkdir(parents=True, exist_ok=True)
        Path(dest).write_bytes(b"%PDF-1.7\n%%EOF\n")

    monkeypatch.setattr(engine, "_make_pdf_cache", fake_make_pdf)

    first = client.get("/article.pdf")
    second = client.get("/article.pdf")

    assert first.status_code == 200
    assert first.headers["x-media-cache"] == "miss"
    assert second.status_code == 200
    assert second.headers["x-media-cache"] == "hit"
    assert first.content.startswith(b"%PDF")
    assert len(calls) == 1
