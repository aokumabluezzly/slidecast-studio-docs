#!/usr/bin/env python3
"""Apply reproducible MouthLoop v2 site extensions after standard generation."""

from __future__ import annotations

import argparse
from pathlib import Path

CSS_MARKER = "/* mouthloop-v2-extra:start */"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("page", type=Path)
    parser.add_argument("--css", type=Path, required=True)
    args = parser.parse_args()

    page = args.page.resolve()
    css = args.css.resolve().read_text(encoding="utf-8")
    html = page.read_text(encoding="utf-8")

    if CSS_MARKER in html:
        raise SystemExit("MouthLoop v2 extensions are already present")

    html = html.replace(
        "</style>",
        f"\n{CSS_MARKER}\n{css}\n/* mouthloop-v2-extra:end */\n</style>",
        1,
    )
    html = html.replace(
        '<div class="brand">MouthLoop v2</div>',
        '<a class="brand" href="../" aria-label="SlideCast Studio Docs ホームへ">MouthLoop v2</a>',
        1,
    )
    html = html.replace(
        '<span class="chapter-heading">',
        '<span class="chapter-heading" role="heading" aria-level="2">',
    )
    html = html.replace(
        '<div class="hero-media"><img ',
        '<div class="hero-media"><img width="1280" height="670" loading="eager" fetchpriority="high" ',
        1,
    )
    html = html.replace(
        '<div class="header-actions"><button class="nav-button" id="openToc"',
        '<div class="header-actions">'
        '<a class="nav-button site-nav" href="../"><span>🏠</span><span class="nav-label">HOME</span></a>'
        '<a class="nav-button site-nav" href="../manual/"><span>📘</span><span class="nav-label">公式マニュアル</span></a>'
        '<button class="nav-button" id="openToc"',
        1,
    )
    html = html.replace(
        '<footer class="footer">',
        '<footer class="footer"><a href="https://share.gemini.google/dkU0IVHfQ2gu" '
        'target="_blank" rel="noopener noreferrer">MouthLoopを開く ↗</a>',
        1,
    )
    html = html.replace('rel="noopener"', 'rel="noopener noreferrer"')
    html = html.replace(
        "</body>",
        '<script>(()=>{\'use strict\';const close=document.getElementById(\'closeChapter\'),'
        'chapters=[...document.querySelectorAll(\'.chapter\')];const sync=()=>close.classList.toggle('
        "'is-visible',chapters.some(ch=>ch.open));chapters.forEach(ch=>ch.addEventListener('toggle',sync));sync();})();</script>"
        "</body>",
        1,
    )
    page.write_text(html, encoding="utf-8")
    print(f"Enhanced {page}")


if __name__ == "__main__":
    main()
