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

画像は `assets/` に置き、各ページから相対パスで参照しています。CSSとJavaScriptは各HTMLに含め、外部CDN・トラッカー・フレームワークには依存していません。

## このリポジトリに含まれないもの

アプリケーション本体のソースコードは含まれていません。**公開用のドキュメントのみ**を置くリポジトリです。

## 更新方法

記事の HTML を差し替えて push すると、GitHub Pages に自動反映されます（反映まで数十秒）。
