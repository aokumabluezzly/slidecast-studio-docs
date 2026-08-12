# SlideCast Studio ドキュメント

[SlideCast Studio](https://note.com/bluezzly/n/nb4c85213c808) の紹介・マニュアル・補助ツールガイド・アップデート情報を公開しているドキュメントサイトのソースです。

公開URL: https://aokumabluezzly.github.io/slidecast-studio-docs/

## 構成

| パス | 内容 |
|---|---|
| `index.html` | トップページ（記事一覧） |
| `intro/` | SlideCast Studio とは（紹介ページ） |
| `manual/` | 公式マニュアル（v3.4 対応版） |
| `bundle-builder/` | SlideCast Bundle Builder 使い方ガイド |
| `mouthloop-v2/` | MouthLoop v2 アップデート・使い方ガイド |
| `updates/v34/` | v3.4「NUANCE」アップデート |
| `updates/v33/` | v3.3「SYNC」アップデート |
| `en/` | 英語版（現在はトップページと紹介ページ） |

画像は `assets/` に置き、各ページから相対パスで参照しています。CSSとJavaScriptは各HTMLに含め、外部CDN・トラッカー・フレームワークには依存していません。

## 日本語版と英語版

日本語ページはリポジトリ直下、英語ページは `en/` 配下に**同じ構造**で置きます。

| 日本語 | 英語 |
|---|---|
| `index.html` | `en/index.html` |
| `intro/index.html` | `en/intro/index.html` |

ヘッダーの 🌐 ボタンで切り替えます（`assets/site-lang.js`）。自動リダイレクトはしません。英語版がまだ無いページでは、ボタンは無効表示（English version coming soon）になります。

英語版があるかどうかは **`assets/site-nav.js` の `PAGES` に書いた `"en": true` が唯一の情報源**です。英語ページを増やしたら、そこに `"en": true` を足すと 🌐 が有効になります。手順の詳細は [`_source/README.md`](_source/README.md) の「英語版ページの作り方」を参照してください。

## このリポジトリに含まれないもの

アプリケーション本体のソースコードは含まれていません。**公開用のドキュメントのみ**を置くリポジトリです。

## 更新方法

記事の HTML を差し替えて push すると、GitHub Pages に自動反映されます（反映まで数十秒）。
