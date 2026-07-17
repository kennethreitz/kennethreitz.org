"""Prebuild every responsive image variant for the production image."""

from engine import (
    DATA_DIR,
    _THUMB_TYPES,
    _THUMB_WIDTHS,
    _make_thumbnail,
    _thumbnail_cache_path,
)


def main():
    generated = 0
    existing = 0

    for source in sorted(DATA_DIR.rglob("*")):
        if not source.is_file() or source.suffix.lower() not in _THUMB_TYPES:
            continue

        path = source.relative_to(DATA_DIR).as_posix()
        for width in _THUMB_WIDTHS:
            _, cached = _thumbnail_cache_path(path, source, width)
            if cached.exists():
                existing += 1
                continue
            _make_thumbnail(source, cached, width)
            generated += 1

    print(
        f"Media cache ready: {generated} thumbnails generated, "
        f"{existing} already present."
    )


if __name__ == "__main__":
    main()
