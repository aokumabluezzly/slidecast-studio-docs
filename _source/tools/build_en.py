#!/usr/bin/env python3
"""英語ページを spec から作り直す（テンプレート生成 → ビルド → 共通クローム）。

    python3 _source/tools/build_en.py            # 英語ページ全部
    python3 _source/tools/build_en.py intro      # 1本だけ

英語ページを増やすときは、次の4か所を触ります。
  1. _source/＜名前＞.en.spec.json を作る（日本語 spec の翻訳）
  2. このファイルの PAGES に1行足す
  3. _source/tools/finish_en_page.py の PAGE_META に OGP 文言を足す
  4. assets/site-nav.js の該当ページに "en": true を足す（🌐 切替が有効になる）
"""

from __future__ import annotations

import pathlib
import subprocess
import sys

REPO = pathlib.Path(__file__).resolve().parents[2]
BUILDER = pathlib.Path.home() / ".claude/skills/build-rich-html-article/scripts/build_article.py"
TEMPLATE = REPO / "_source/article-template.en.html"

# 名前 -> (spec, 出力先)
PAGES: dict[str, tuple[str, str]] = {
    "intro": ("_source/intro.en.spec.json", "en/intro/index.html"),
    "bundle-builder": ("_source/bundle-builder.en.spec.json", "en/bundle-builder/index.html"),
    "gas-update": ("_source/gas-update.en.spec.json", "en/gas-update/index.html"),
}


def run(*args: str) -> None:
    result = subprocess.run(args, cwd=REPO)
    if result.returncode != 0:
        raise SystemExit(result.returncode)


def main(argv: list[str]) -> int:
    names = argv or list(PAGES)
    unknown = [n for n in names if n not in PAGES]
    if unknown:
        print(f"知らないページです: {', '.join(unknown)}", file=sys.stderr)
        print(f"使えるのは: {', '.join(PAGES)}", file=sys.stderr)
        return 1

    # 標準テンプレートの更新に追従させるため、毎回作り直す
    run(sys.executable, "_source/tools/make_en_template.py")

    for name in names:
        spec, out = PAGES[name]
        (REPO / out).parent.mkdir(parents=True, exist_ok=True)
        run(sys.executable, str(BUILDER), spec, out,
            "--assets", "assets", "--template", str(TEMPLATE.relative_to(REPO)))
        run(sys.executable, "_source/tools/finish_en_page.py", out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
