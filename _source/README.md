# _source — 記事の設計データ

このフォルダは、公開している HTML を**生成するための元データ**です。サイトの表示には使われません。

HTML は 1ファイル 2〜4MB あり、その大半が Base64 画像なので、人力で直接編集するのは大変です。文章や構成を直したいときは、ここの JSON を編集して再生成するのが確実です。

## 中身

| ファイル | 内容 |
|---|---|
| `home.spec.json` | トップページ（`/index.html`）の設計データ |
| `intro.spec.json` | 紹介ページ（`/intro/index.html`）の設計データ |
| `img/` | 上記が参照する画像。生成時に Base64 で HTML へ埋め込まれます |

テンプレートは `build-rich-html-article` スキル同梱の**標準テンプレートをそのまま使います**。以前このフォルダに置いていた専用テンプレートは、修正内容を標準側へ取り込んだため廃止しました。

## 再生成のしかた

リポジトリのルートで実行します。`--template` の指定は不要です。

```bash
python3 ~/.claude/skills/build-rich-html-article/scripts/build_article.py \
  _source/home.spec.json index.html
```

```bash
python3 ~/.claude/skills/build-rich-html-article/scripts/build_article.py \
  _source/intro.spec.json intro/index.html
```

## ⚠️ 再生成したら必ずやること

生成直後の HTML には、ヘッダーの「🏠 ドキュメント」リンクが**入っていません**。生成スクリプトの管轄外で、後から差し込んでいるためです。忘れるとトップページへ戻れなくなります。

`<nav class="header-nav" aria-label="記事内ナビゲーション">` の直後に、以下を挿入してください。

ルート直下の記事（`intro/` など、1階層）:

```html
<a class="header-link" href="../"><span aria-hidden="true">🏠</span><span class="nav-label">ドキュメント</span></a>
```

2階層の記事（`updates/v34/` など）は `href="../../"` にします。

## spec で使っている、見落としやすい指定

| 指定 | 意味 |
|---|---|
| `"lead": ""` | ヒーローの導入文を出さない。省略すると `description` が導入文として表示される |
| `"nowrap": true`（table ブロック） | 表の2列目以降を折り返さない。料金表で「約6 / 円」と分断されるのを防ぐため、intro の TTS 料金表だけに付けている |

長い文章が入る列を持つ表に `nowrap` を付けると横スクロールが過剰になるので、数値が並ぶ表にだけ使うこと。

## 設計データが無い記事

`manual/`、`updates/v34/`、`updates/v33/` の3本は、この仕組みを整える前に作られたため、設計データが残っていません。これらを大きく直す場合は、元の Markdown 原稿から spec を作り直す形になります。
