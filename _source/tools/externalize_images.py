#!/usr/bin/env python3
"""Move Base64 images out of a generated article into a shared asset directory.

For the pages that still have a spec, regenerate them with
`build_article.py --assets` instead. This script exists for `manual/`,
`updates/v34/`, and `updates/v33/`, whose specs were not kept.

Every `src="data:image/…;base64,…"` is written to the asset directory under a
content-addressed name, replaced with a relative URL, and marked
`loading="lazy"` unless the tag already states its own loading mode. Images
already present in the asset directory are reused, so a screenshot shared by
several pages is downloaded once by the reader.

    python3 _source/tools/externalize_images.py manual/index.html --assets assets
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import os
import re
from pathlib import Path

DATA_IMG_RE = re.compile(
    r'<img\b[^>]*?\bsrc\s*=\s*(["\'])(data:image/([a-z+]+);base64,([A-Za-z0-9+/=\s]+))\1[^>]*>',
    re.IGNORECASE,
)
LOADING_ATTR_RE = re.compile(r"\bloading\s*=", re.IGNORECASE)
EXTENSIONS = {"png": ".png", "jpeg": ".jpg", "jpg": ".jpg", "gif": ".gif", "webp": ".webp", "svg+xml": ".svg"}


def existing_digests(assets_dir: Path) -> dict[str, str]:
    found: dict[str, str] = {}
    for path in sorted(assets_dir.glob("*")):
        if path.is_file():
            found.setdefault(hashlib.sha256(path.read_bytes()).hexdigest(), path.name)
    return found


def externalize(page: Path, assets_dir: Path, prefix: str, stem: str) -> tuple[str, int, int]:
    html = page.read_text(encoding="utf-8")
    known = existing_digests(assets_dir) if assets_dir.is_dir() else {}
    written = 0
    counter = [0]

    def replace(match: re.Match[str]) -> str:
        tag, quote, subtype, payload = match.group(0), match.group(1), match.group(3).lower(), match.group(4)
        suffix = EXTENSIONS.get(subtype)
        if suffix is None:
            return tag
        data = base64.b64decode(re.sub(r"\s+", "", payload))
        digest = hashlib.sha256(data).hexdigest()
        name = known.get(digest)
        if name is None:
            counter[0] += 1
            name = f"{stem}-{counter[0]:02d}{suffix}"
            while (assets_dir / name).exists():
                counter[0] += 1
                name = f"{stem}-{counter[0]:02d}{suffix}"
            assets_dir.mkdir(parents=True, exist_ok=True)
            (assets_dir / name).write_bytes(data)
            known[digest] = name
            nonlocal written
            written += 1
        src_start = match.start(2) - match.start()
        src_end = match.end(2) - match.start()
        tag = tag[:src_start] + f"{prefix}/{name}" + tag[src_end:]
        if not LOADING_ATTR_RE.search(tag):
            tag = tag[:-1].rstrip().removesuffix("/") + ' loading="lazy">'
        return tag

    output, replaced = DATA_IMG_RE.subn(replace, html)
    return output, replaced, written


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("page", type=Path, help="Generated HTML page to rewrite in place")
    parser.add_argument("--assets", type=Path, required=True, help="Shared asset directory")
    parser.add_argument("--prefix", default=None, help="URL prefix (default: --assets relative to the page)")
    parser.add_argument("--stem", default=None, help="File name stem (default: the page's parent directory)")
    parser.add_argument("--dry-run", action="store_true", help="Report what would change and write nothing")
    args = parser.parse_args()

    page = args.page.expanduser().resolve()
    assets_dir = args.assets.expanduser().resolve()
    prefix = args.prefix or os.path.relpath(assets_dir, page.parent).replace(os.sep, "/")
    stem = args.stem or (page.parent.name if page.name == "index.html" else page.stem)

    if args.dry_run:
        count = len(DATA_IMG_RE.findall(page.read_text(encoding="utf-8")))
        print(f"{page}: {count} embedded image(s) would move to {assets_dir} as {prefix}/{stem}-NN.…")
        return

    before = page.stat().st_size
    output, replaced, written = externalize(page, assets_dir, prefix, stem)
    page.write_text(output, encoding="utf-8")
    after = page.stat().st_size
    print(
        f"{page}: {replaced} image reference(s) externalized, {written} new file(s), "
        f"{before / 1_048_576:.2f}MB → {after / 1_048_576:.2f}MB"
    )


if __name__ == "__main__":
    main()
