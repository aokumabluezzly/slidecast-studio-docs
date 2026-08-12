#!/usr/bin/env python3
"""英語版の記事テンプレートを、標準テンプレートから作り直す。

記事ページの本文は spec（*.en.spec.json）から入るが、テンプレート側に直接
書かれている UI 文言（「本文へスキップ」「目次」「上へ」など）は日本語のまま
なので、ここで置き換えた英語版テンプレートを作り、build_article.py に
--template で渡す。

    python3 _source/tools/make_en_template.py

標準テンプレートが更新されたら、このスクリプトを流し直せば英語版も追従する。
置換前の文字列が1つでも見つからなければ、黙って通さずエラーで止まる
（テンプレート側の文言が変わったことに気づけるように）。
"""

from __future__ import annotations

import pathlib
import sys

SOURCE = pathlib.Path.home() / ".claude/skills/build-rich-html-article/assets/article-template.html"
OUTPUT = pathlib.Path(__file__).resolve().parents[1] / "article-template.en.html"

# 置換は「長い文字列が先」。'目次を閉じる' より前に '目次' を置くと壊れる
REPLACEMENTS: list[tuple[str, str]] = [
    ('<html lang="ja"', '<html lang="en"'),
    ("本文へスキップ", "Skip to content"),
    ('aria-label="記事内ナビゲーション"', 'aria-label="Article navigation"'),
    ('aria-label="表示テーマを切り替える"', 'aria-label="Switch colour theme"'),
    ('aria-label="記事の各章"', 'aria-label="Article chapters"'),
    ('aria-label="目次を閉じる"', 'aria-label="Close contents"'),
    ('aria-label="画像を閉じる"', 'aria-label="Close image"'),
    ('aria-label="目次"', 'aria-label="Contents"'),
    ('<span class="nav-label">目次</span>', '<span class="nav-label">Contents</span>'),
    ('<span class="float-label">閉じる</span>', '<span class="float-label">Close</span>'),
    ('<span class="float-label">目次</span>', '<span class="float-label">Contents</span>'),
    ('<span class="float-label">上へ</span>', '<span class="float-label">Top</span>'),
    ("<strong>目次</strong>", "<strong>Contents</strong>"),
    ('<span aria-hidden="true">🏠</span>概要', '<span aria-hidden="true">🏠</span>Overview'),
    ("動画';", "Video';"),
    ("コピーしました';", "Copied';"),
    ("コピーできません';", "Copy failed';"),
]


def main() -> int:
    if not SOURCE.exists():
        print(f"標準テンプレートが見つかりません: {SOURCE}", file=sys.stderr)
        return 1

    html = SOURCE.read_text(encoding="utf-8")
    missing = [old for old, _ in REPLACEMENTS if old not in html]
    if missing:
        print("標準テンプレート側の文言が変わっています。REPLACEMENTS を直してください:", file=sys.stderr)
        for old in missing:
            print(f"  - {old!r}", file=sys.stderr)
        return 1

    for old, new in REPLACEMENTS:
        html = html.replace(old, new)

    # DOCTYPE より前にコメントを置くと互換モードに落ちる恐れがあるため、直後に入れる
    banner = (
        "\n<!-- 自動生成: _source/tools/make_en_template.py が\n"
        "     build-rich-html-article の標準テンプレートから作っています。\n"
        "     このファイルを直接編集しないでください。 -->"
    )
    head, sep, rest = html.partition("\n")
    if not sep:
        print("テンプレートの1行目（DOCTYPE）が読めません", file=sys.stderr)
        return 1
    OUTPUT.write_text(head + banner + sep + rest, encoding="utf-8")
    print(f"書き出しました: {OUTPUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
