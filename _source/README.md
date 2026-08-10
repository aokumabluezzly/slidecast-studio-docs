# _source — 記事の設計データ

このフォルダは、公開している HTML を**生成するための元データ**です。サイトの表示には使われません。

文章や構成を直したいときは、ここの JSON を編集して再生成するのが確実です。

画像は HTML に埋め込まず、リポジトリ直下の `assets/` に実ファイルとして置き、各ページから相対パスで読み込んでいます（2026年8月に Base64 埋め込みから移行）。移行前は 1ページ 2〜4MB ありましたが、いまは HTML 本体が 60〜130KB です。

## 中身

| ファイル | 内容 |
|---|---|
| `retired/home.spec.json` | **旧**トップページの設計データ。現在のトップページは spec から生成していません（下記） |
| `intro.spec.json` | 紹介ページ（`/intro/index.html`）の設計データ |
| `bundle-builder.spec.json` | Bundle Builder ガイド（`/bundle-builder/index.html`）の設計データ |
| `mouthloop-v2/index.html` | note 添付HTMLを元に移行した MouthLoop v2 ガイド（specなし） |
| `img/` | 各 spec が参照する画像。生成時に `/assets/` へコピーされます |
| `tools/externalize_images.py` | 設計データが無いページから Base64 画像を抜き出して `/assets/` へ移す移行スクリプト |

テンプレートは `build-rich-html-article` スキル同梱の**標準テンプレートをそのまま使います**。以前このフォルダに置いていた専用テンプレートは、修正内容を標準側へ取り込んだため廃止しました。

## ⚠️ トップページ（`/index.html`）は spec から生成していません

2026年8月に、トップページだけ**記事テンプレートから外して手書きの専用ページ**に作り替えました。記事テンプレートは1本の記事を読ませる構造で、複数記事への入口を並べるハブには向かなかったためです（記事一覧が画面2つ分スクロールした先にありました）。

- トップページを直すときは `index.html` を**直接編集**します。`build_article.py` で再生成してはいけません（この専用ページが上書きされます）。
- 旧 spec は `_source/retired/home.spec.json` に退避してあります。参照用で、再生成には使いません。
- CSS 変数と `localStorage` のテーマキー（`article-theme`）は記事ページと共通なので、配色とダーク/ライトの選択はサイト全体で揃います。テーマ設計を変える場合は両方を直してください。
- 記事を追加したら、`index.html` の「記事一覧」カードと「更新履歴」に手で追記します。

## 再生成のしかた

リポジトリのルートで実行します。`--template` の指定は不要です。

**`--assets assets` を必ず付けます。** これを忘れると画像が Base64 で埋め込まれ、ページが数MBに戻ります。

```bash
python3 ~/.claude/skills/build-rich-html-article/scripts/build_article.py \
  _source/intro.spec.json intro/index.html --assets assets

python3 ~/.claude/skills/build-rich-html-article/scripts/build_article.py \
  _source/bundle-builder.spec.json bundle-builder/index.html --assets assets
```

リンクの接頭辞は、出力先から見た `assets` の相対パス（`assets/`、`../assets/`、`../../assets/`）が自動で入ります。同じ内容の画像は1つのファイルにまとめられ、ヒーロー以外には `loading="lazy"` が付きます。

`assets/` に増えたファイルはコミットに含めてください。差し替えで使われなくなったファイルは自動では消えないので、必要なら手で削除します。

## ヘッダーとフッターのリンク

ヘッダーは**サイト内の回遊専用**、note の記事リンクは**フッターとソースカードに残す**方針です（note 記事の評価につながるため）。以前は 🏠 リンクを生成後に手で挿入していましたが、いまは spec の `nav_links` から生成されます。

```json
"nav_links": [
  { "href": "../", "icon": "🏠", "label": "HOME" },
  { "href": "../manual/", "icon": "📘", "label": "公式マニュアル" }
],
"update_header": false
```

`href` は相対パスです。1階層（`intro/`）は `../`、2階層（`updates/v34/`）は `../../`。`update_header: false` を書かないと、note へのリンクがヘッダーにも出てしまいます。

`manual/`・`updates/v34/`・`updates/v33/` は spec が無いため、ヘッダーを直接編集してあります。

本文中の note 記事へのリンクは、サイト内に同等ページがあっても差し替えません。

## spec で使っている、見落としやすい指定

| 指定 | 意味 |
|---|---|
| `"lead": ""` | ヒーローの導入文を出さない。省略すると `description` が導入文として表示される |
| `"nowrap": true`（table ブロック） | 表の2列目以降を折り返さない。料金表で「約6 / 円」と分断されるのを防ぐため、intro の TTS 料金表だけに付けている |

長い文章が入る列を持つ表に `nowrap` を付けると横スクロールが過剰になるので、数値が並ぶ表にだけ使うこと。

## 動画の貼り方

YouTube / Vimeo は `video` ブロックで貼ります。**クリックされるまで YouTube にも Vimeo にも一切通信しません。**サムネイルは自前で用意し、クリック後の読み込み先は `youtube-nocookie.com`、Vimeo は `dnt=1` 付きです。

```json
{ "type": "video", "provider": "youtube", "id": "cB0MVpcMdKo",
  "title": "🎬 こうやって作ります！", "thumb": "./img/ui-easy.png",
  "caption": "制作の流れ（YouTube）。クリックすると、この場で再生されます" }
```

`thumb` は `img/` に置いたローカル画像です。YouTube の公式サムネイルを直接指定してはいけません（ページを開いただけで読者の訪問が YouTube に伝わります）。`thumb` を省略するとグラデーションの板が出ます。

現在 intro の2本は、専用のサムネイルがまだ無いため、既存のスクリーンショット（`v34.jpg` / `ui-easy.png`）で代用しています。

## 設計データが無い記事

`manual/`、`updates/v34/`、`updates/v33/` の3本は、この仕組みを整える前に作られたため、設計データが残っていません。`mouthloop-v2/` は、作者が note 記事内で配布している完成済みHTMLを元に、画像を外部ファイル化してサイトへ移行したページです。これらを大きく直す場合は、元の Markdown 原稿または元HTMLから spec を作り直す形になります。

画像の外部ファイル化だけは spec 無しで済ませてあります。同じことを別のページでやる場合は次のとおりです（ページを上書きするので、実行前に `--dry-run` で件数を確認してください）。

```bash
python3 _source/tools/externalize_images.py manual/index.html --assets assets --dry-run
python3 _source/tools/externalize_images.py manual/index.html --assets assets
```
