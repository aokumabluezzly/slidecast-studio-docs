#!/usr/bin/env python3
"""英語ページ（/en/…）に、サイト共通クロームを入れ直す。

build_article.py はサイト共通の飾り（ファビコン・OGP・シェアボタン・背景演出・
📚 ページ一覧・🌐 言語切替・共通フッター）を知らないので、生成しただけのページには
それらが入っていません。日本語ページは手作業で足す運用ですが、英語ページは
このスクリプトで自動化しています。**再生成したら必ず流してください。**

    python3 _source/tools/build_en.py            # 生成 → 仕上げ まで一括
    python3 _source/tools/finish_en_page.py en/intro/index.html

SNS アイコンの SVG はトップページ（index.html）から読み取ります。アイコンを
足したり差し替えたりするときは index.html だけ直せば、英語ページにも回ります。
"""

from __future__ import annotations

import pathlib
import re
import sys

REPO = pathlib.Path(__file__).resolve().parents[2]
BASE_URL = "https://aokumabluezzly.github.io/slidecast-studio-docs/"

# /en/ 配下のページごとの、ページ固有メタ情報
PAGE_META: dict[str, dict[str, str]] = {
    "en/intro/": {
        "og_title": "What is SlideCast Studio?",
        "og_description": (
            "A one-time-purchase, browser-only tool that turns your slides and AI voice "
            "into narrated, subtitled video. What it does, what it costs, and how to set it up."
        ),
    },
    "en/bundle-builder/": {
        "og_title": "SlideCast Bundle Builder — how to use it",
        "og_description": (
            "Prepare slides, script, AI voice and mic recordings in one pass, validate them, "
            "and export a Bundle ZIP that SlideCast Studio can import."
        ),
    },
    "en/mouthloop-v2/": {
        "og_title": "MouthLoop v2 — expressions and gestures",
        "og_description": (
            "A free Gemini Canvas app that turns a single image into lip-sync character assets "
            "with expressions and gestures, packed as a ZIP SlideCast Studio can import."
        ),
    },
    "en/gas-update/": {
        "og_title": "How to update SlideCast Studio",
        "og_description": (
            "Move the Apps Script edition to the latest version, keeping the same URL and the "
            "same data: swap two files, then redeploy as a new version."
        ),
    },
    "en/updates/v33/": {
        "og_title": "SlideCast Studio v3.3 “SYNC” update",
        "og_description": (
            "Character assets in three methods, ZIP and folder import, six-image lip sync "
            "and speech bubbles that follow the character."
        ),
    },
    "en/updates/v34/": {
        "og_title": "SlideCast Studio v3.4 “NUANCE”",
        "og_description": (
            "Expressions and posed gestures partway through a line, auto-acting, character "
            "pack ZIPs, breathing and speech motion, and blank slides."
        ),
    },
}

# ヘッダーの 📚 ページ一覧ボタン（site-nav.js が拾う data-site-nav が要る）
PAGENAV_BUTTON = (
    '<button class="header-link" type="button" data-site-nav aria-label="All pages">'
    '<span aria-hidden="true">📚</span><span class="nav-label">Pages</span></button>'
)


def social_links() -> str:
    """トップページの SNS アイコン行をそのまま借りる。"""
    home = (REPO / "index.html").read_text(encoding="utf-8")
    match = re.search(r'<nav class="social-links" aria-label="SNSリンク">(.*?)</nav>', home, re.S)
    if not match:
        raise SystemExit("index.html から SNS アイコン行が見つかりません")
    return match.group(1).replace('aria-label="X（旧Twitter）"', 'aria-label="X (formerly Twitter)"').strip()


def head_extras(rel: str, up: str, meta: dict[str, str]) -> str:
    ja_url = BASE_URL + rel[len("en/"):]
    en_url = BASE_URL + rel
    return "\n".join([
        f'<link rel="canonical" href="{en_url}">',
        f'<link rel="alternate" hreflang="ja" href="{ja_url}">',
        f'<link rel="alternate" hreflang="en" href="{en_url}">',
        f'<link rel="alternate" hreflang="x-default" href="{ja_url}">',
        f'<link rel="icon" type="image/png" sizes="32x32" href="{up}assets/brand/favicon-32.png">',
        f'<link rel="icon" type="image/png" sizes="16x16" href="{up}assets/brand/favicon-16.png">',
        f'<link rel="apple-touch-icon" sizes="180x180" href="{up}assets/brand/apple-touch-icon.png">',
        f'<link rel="manifest" href="{up}site.webmanifest">',
        '<meta name="theme-color" content="#1957ff">',
        '<meta property="og:type" content="article">',
        '<meta property="og:locale" content="en_US">',
        '<meta property="og:locale:alternate" content="ja_JP">',
        '<meta property="og:site_name" content="SlideCast Studio">',
        f'<meta property="og:title" content="{meta["og_title"]}">',
        f'<meta property="og:description" content="{meta["og_description"]}">',
        f'<meta property="og:url" content="{en_url}">',
        f'<meta property="og:image" content="{BASE_URL}assets/brand/og-image.png">',
        '<meta property="og:image:width" content="1200">',
        '<meta property="og:image:height" content="630">',
        '<meta property="og:image:alt" content="SlideCast Studio logo">',
        '<meta name="twitter:card" content="summary_large_image">',
        f'<meta name="twitter:title" content="{meta["og_title"]}">',
        f'<meta name="twitter:description" content="{meta["og_description"]}">',
        f'<meta name="twitter:image" content="{BASE_URL}assets/brand/og-image.png">',
    ])


def footer_html(up: str, en_up: str) -> str:
    """up はサイトのルートまで、en_up は /en/ のルートまでの相対パス。"""
    return (
        f'<a class="brand footer-brand" href="{en_up}" aria-label="SlideCast Studio home">'
        "SlideCast <b>Studio</b></a>"
        '<nav class="footer-links" aria-label="Footer navigation">'
        f'<a href="{en_up}intro/">What is SlideCast Studio?</a>'
        f'<a href="{up}manual/">Official manual (JA)</a>'
        f'<a href="{en_up}bundle-builder/">Bundle Builder</a>'
        f'<a href="{en_up}mouthloop-v2/">MouthLoop v2</a>'
        "</nav>"
    )


def finish(path: pathlib.Path) -> None:
    rel = path.relative_to(REPO).as_posix().removesuffix("index.html")
    if rel not in PAGE_META:
        raise SystemExit(f"PAGE_META に {rel} がありません。追記してください")
    up = "../" * (rel.count("/"))          # en/intro/ → ../../ （サイトのルートまで）
    en_up = "../" * (rel.count("/") - 1)   # en/intro/ → ../   （/en/ のルートまで）
    html = path.read_text(encoding="utf-8")

    # 生成テンプレートの注意書きは、公開ページには要らない
    html = re.sub(r"<!-- 自動生成:.*?-->\n?", "", html, count=1, flags=re.S)

    # 1. 動画ボタンの aria-label（build_article.py が日本語で書く唯一の箇所）
    html = re.sub(
        r'aria-label="([^"]*?) を再生（([a-z]+)）"',
        lambda m: f'aria-label="Play “{m.group(1)}” ({m.group(2).capitalize()})"',
        html,
    )

    # 2. <title> の直後にメタ情報一式
    if "rel=\"canonical\"" not in html:
        html = html.replace("</title>", "</title>\n" + head_extras(rel, up, PAGE_META[rel]), 1)

    # 3. </head> の前に共通CSS/JS。site-lang.js は site-nav.js より後ろに置く
    if "site-chrome.css" not in html:
        html = html.replace("</head>", "\n".join([
            f'<link rel="stylesheet" href="{up}assets/site-chrome.css">',
            f'<link rel="stylesheet" href="{up}assets/site-actions.css">',
            f'<script src="{up}assets/site-actions.js" defer></script>',
            f'<script src="{up}assets/site-nav.js" defer></script>',
            f'<script src="{up}assets/site-lang.js" defer></script>',
            "</head>",
        ]), 1)

    # 4. ヘッダー: 🏠 に aria-label、その直後に 📚 ボタン
    html = html.replace(
        f'<a class="header-link" href="{up[:-3] or "./"}"><span aria-hidden="true">🏠</span>',
        f'<a class="header-link" href="{up[:-3] or "./"}" aria-label="Home"><span aria-hidden="true">🏠</span>',
        1,
    )
    if "data-site-nav" not in html:
        html = html.replace(
            '<span class="nav-label">HOME</span></a>',
            '<span class="nav-label">HOME</span></a>' + PAGENAV_BUTTON,
            1,
        )

    # 5. ライトボックスの後ろに背景演出
    if "ambient-particles.js" not in html:
        marker = "</dialog>\n"
        last = html.rfind(marker)
        if last == -1:
            raise SystemExit("</dialog> が見つかりません")
        insert = last + len(marker)
        html = html[:insert] + f'<script src="{up}assets/ambient-particles.js"></script>\n' + html[insert:]

    # 6. フッターをサイト共通の形へ。最下段は SNS アイコンを並べた footer-bottom に包む
    html = re.sub(
        r'<div class="footer-top">.*?</div>\s*<p class="footer-meta">(.*?)</p>',
        lambda m: (
            f'<div class="footer-top">{footer_html(up, en_up)}</div>'
            '<div class="footer-bottom">'
            f'<p class="footer-meta">{m.group(1)}</p>'
            f'<nav class="social-links" aria-label="Social links">{social_links()}</nav>'
            "</div>"
        ),
        html,
        count=1,
        flags=re.S,
    )

    path.write_text(html, encoding="utf-8")
    print(f"仕上げました: {path.relative_to(REPO)}")


def main(argv: list[str]) -> int:
    if not argv:
        print(__doc__)
        return 1
    for arg in argv:
        finish(pathlib.Path(arg).resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
