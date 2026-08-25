#!/usr/bin/env python3
"""日本語ページ（spec から生成したもの）に、サイト共通クロームを入れ直す。

build_article.py はサイト共通の飾り（ファビコン・OGP・📚 ページ一覧・🌐 言語切替・
背景演出・共通フッター）を知らないので、生成しただけのページにはそれらが入っていません。
英語ページ用の finish_en_page.py と同じことを、日本語ページに対して行います。
**spec から再生成したら必ず流してください。**

    python3 _source/tools/finish_ja_page.py ai-code-bgm-studio/index.html

対象ページを増やすときは、下の PAGE_META に1行足します。既に手で仕上げてある
ページ（manual・updates/v33・v34 など）にかける必要はありません。

SNS アイコンの SVG はトップページ（index.html）から読み取ります。
"""

from __future__ import annotations

import pathlib
import re
import sys

REPO = pathlib.Path(__file__).resolve().parents[2]
BASE_URL = "https://aokumabluezzly.github.io/slidecast-studio-docs/"

# ページごとの、ページ固有メタ情報。`en` は英語版があるかどうか（hreflang に効く）
PAGE_META: dict[str, dict[str, object]] = {
    "updates/v40/": {
        "og_title": "SlideCast Studio v4.0「DECAL」",
        "og_description": (
            "スライド内ステッカー、段階表示、登場・退場エフェクト、効果音、"
            "スナップ、ライブラリ、モザイク・ぼかしを追加したv4.0の更新内容。"
        ),
        "twitter_description": "ステッカーと段階表示で、1枚のスライドを見せる順番まで設計。",
        "en": True,
    },
    "ai-code-movie-studio/": {
        "og_title": "AI CODE MOVIE STUDIO で短尺動画を作る",
        "og_description": (
            "原稿やイメージから HTML Canvas と Web Audio API の映像コードを生成する無料の Gemini Canvas アプリ。"
            "設定・書き出し・SlideCast Studio の OP / ED での使い方を画像つきで解説します。"
        ),
        "twitter_description": "原稿から短尺動画を作って MP4 で書き出す使い方を画像つきで解説。",
        "en": True,
    },
    "ai-code-bgm-studio/": {
        "og_title": "AI CODE BGM STUDIO でBGMと効果音を作る",
        "og_description": (
            "言葉から Web Audio API のコードとしてBGM・効果音を生成する無料の Gemini Canvas アプリ。"
            "設定・書き出し・SlideCast Studio での使い方を画像つきで解説します。"
        ),
        "twitter_description": "言葉からBGM・効果音を作って MP3 で書き出す使い方を画像つきで解説。",
        "en": True,
    },
}

PAGENAV_BUTTON = (
    '<button class="header-link" type="button" data-site-nav aria-label="ページ一覧">'
    '<span aria-hidden="true">📚</span><span class="nav-label">ページ</span></button>'
)


def social_links() -> str:
    """トップページの SNS アイコン行をそのまま借りる。"""
    home = (REPO / "index.html").read_text(encoding="utf-8")
    match = re.search(r'<nav class="social-links" aria-label="SNSリンク">(.*?)</nav>', home, re.S)
    if not match:
        raise SystemExit("index.html から SNS アイコン行が見つかりません")
    return match.group(1).strip()


def head_extras(rel: str, up: str, meta: dict[str, object]) -> str:
    ja_url = BASE_URL + rel
    en_url = BASE_URL + "en/" + rel
    lines = [
        f'<link rel="canonical" href="{ja_url}">',
        f'<link rel="alternate" hreflang="ja" href="{ja_url}">',
    ]
    if meta.get("en"):
        lines.append(f'<link rel="alternate" hreflang="en" href="{en_url}">')
    lines += [
        f'<link rel="alternate" hreflang="x-default" href="{ja_url}">',
        f'<link rel="icon" type="image/png" sizes="32x32" href="{up}assets/brand/favicon-32.png">',
        f'<link rel="icon" type="image/png" sizes="16x16" href="{up}assets/brand/favicon-16.png">',
        f'<link rel="apple-touch-icon" sizes="180x180" href="{up}assets/brand/apple-touch-icon.png">',
        f'<link rel="manifest" href="{up}site.webmanifest">',
        '<meta name="theme-color" content="#1957ff">',
        '<meta property="og:type" content="article">',
        '<meta property="og:locale" content="ja_JP">',
        '<meta property="og:site_name" content="SlideCast Studio">',
        f'<meta property="og:title" content="{meta["og_title"]}">',
        f'<meta property="og:description" content="{meta["og_description"]}">',
        f'<meta property="og:url" content="{ja_url}">',
        f'<meta property="og:image" content="{BASE_URL}assets/brand/og-image.png">',
        '<meta property="og:image:width" content="1200">',
        '<meta property="og:image:height" content="630">',
        '<meta property="og:image:alt" content="SlideCast Studio ロゴ">',
        '<meta name="twitter:card" content="summary_large_image">',
        f'<meta name="twitter:title" content="{meta["og_title"]}">',
        f'<meta name="twitter:description" content="{meta.get("twitter_description", meta["og_description"])}">',
        f'<meta name="twitter:image" content="{BASE_URL}assets/brand/og-image.png">',
    ]
    return "\n".join(lines)


def footer_html(up: str) -> str:
    return (
        f'<a class="brand footer-brand" href="{up}" aria-label="SlideCast Studio トップページ">'
        "SlideCast <b>Studio</b></a>"
        '<nav class="footer-links" aria-label="フッターナビゲーション">'
        f'<a href="{up}intro/">SlideCast Studio とは</a>'
        f'<a href="{up}manual/">公式マニュアル</a>'
        f'<a href="{up}bundle-builder/">Bundle Builder</a>'
        f'<a href="{up}mouthloop-v2/">MouthLoop v2</a>'
        "</nav>"
    )


def finish(path: pathlib.Path) -> None:
    rel = path.relative_to(REPO).as_posix().removesuffix("index.html")
    if rel not in PAGE_META:
        raise SystemExit(f"PAGE_META に {rel} がありません。追記してください")
    meta = PAGE_META[rel]
    up = "../" * rel.count("/")            # ai-code-bgm-studio/ → ../ （サイトのルートまで）
    html = path.read_text(encoding="utf-8")

    # 生成テンプレートの注意書きは、公開ページには要らない
    html = re.sub(r"<!-- 自動生成:.*?-->\n?", "", html, count=1, flags=re.S)

    # 1. <title> の直後にメタ情報一式
    if 'rel="canonical"' not in html:
        html = html.replace("</title>", "</title>\n" + head_extras(rel, up, meta), 1)

    # 2. </head> の前に共通CSS/JS。site-lang.js は site-nav.js より後ろに置く
    if "site-chrome.css" not in html:
        html = html.replace("</head>", "\n".join([
            f'<link rel="stylesheet" href="{up}assets/site-chrome.css">',
            f'<link rel="stylesheet" href="{up}assets/site-actions.css">',
            f'<script src="{up}assets/site-actions.js" defer></script>',
            f'<script src="{up}assets/site-nav.js" defer></script>',
            f'<script src="{up}assets/site-lang.js" defer></script>',
            "</head>",
        ]), 1)

    # 3. ヘッダー: ブランドはサイトのトップへ、🏠 に aria-label、その直後に 📚 ボタン
    html = html.replace(
        '<a class="brand" href="#top">',
        f'<a class="brand" href="{up}" aria-label="SlideCast Studio トップページ">',
        1,
    )
    html = html.replace(
        '<button class="header-link" id="openToc" type="button">',
        '<button class="header-link" id="openToc" type="button" aria-label="目次">',
        1,
    )
    html = html.replace(
        f'<a class="header-link" href="{up}"><span aria-hidden="true">🏠</span>',
        f'<a class="header-link" href="{up}" aria-label="トップページ"><span aria-hidden="true">🏠</span>',
        1,
    )
    if "data-site-nav" not in html:
        html = html.replace(
            '<span class="nav-label">HOME</span></a>',
            '<span class="nav-label">HOME</span></a>' + PAGENAV_BUTTON,
            1,
        )

    # 4. ライトボックスの後ろに背景演出
    if "ambient-particles.js" not in html:
        marker = "</dialog>\n"
        last = html.rfind(marker)
        if last == -1:
            raise SystemExit("</dialog> が見つかりません")
        insert = last + len(marker)
        html = html[:insert] + f'<script src="{up}assets/ambient-particles.js"></script>\n' + html[insert:]

    # 5. フッターをサイト共通の形へ。最下段は SNS アイコンを並べた footer-bottom に包む
    html = re.sub(
        r'<div class="footer-top">.*?</div>\s*<p class="footer-meta">(.*?)</p>',
        lambda m: (
            f'<div class="footer-top">{footer_html(up)}</div>'
            '<div class="footer-bottom">'
            f'<p class="footer-meta">{m.group(1)}</p>'
            f'<nav class="social-links" aria-label="SNSリンク">{social_links()}</nav>'
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
