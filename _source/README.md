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
| `mouthloop-v2.spec.json` | MouthLoop v2 ガイド（`/mouthloop-v2/index.html`）の設計データ |
| `gas-update.spec.json` | アップデート方法ガイド（`/gas-update/index.html`）の設計データ |
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

MouthLoop v2 も同じ現行標準テンプレートとブロックライブラリから生成します。

```bash
python3 ~/.claude/skills/build-rich-html-article/scripts/build_article.py \
  _source/mouthloop-v2.spec.json mouthloop-v2/index.html --assets assets
```

```bash
python3 ~/.claude/skills/build-rich-html-article/scripts/build_article.py \
  _source/gas-update.spec.json gas-update/index.html --assets assets
```

リンクの接頭辞は、出力先から見た `assets` の相対パス（`assets/`、`../assets/`、`../../assets/`）が自動で入ります。同じ内容の画像は1つのファイルにまとめられ、ヒーロー以外には `loading="lazy"` が付きます。

`assets/` に増えたファイルはコミットに含めてください。差し替えで使われなくなったファイルは自動では消えないので、必要なら手で削除します。

## ⚠️ 生成後に手で足している「共通クローム」

`build_article.py` はサイト共通の飾りを知らないため、**生成しただけのページには次が入っていません**。再生成したら毎回入れ直してください。入れ忘れると、そのページだけファビコンとシェアボタンと背景演出が消えます。

`<title>` の直後（`../` は1階層のページの場合。2階層なら `../../`）:

```html
<link rel="canonical" href="https://aokumabluezzly.github.io/slidecast-studio-docs/＜ページ＞/">
<link rel="icon" type="image/png" sizes="32x32" href="../assets/brand/favicon-32.png">
<link rel="icon" type="image/png" sizes="16x16" href="../assets/brand/favicon-16.png">
<link rel="apple-touch-icon" sizes="180x180" href="../assets/brand/apple-touch-icon.png">
<link rel="manifest" href="../site.webmanifest">
<meta name="theme-color" content="#1957ff">
<!-- og:type / og:locale / og:site_name / og:title / og:description / og:url /
     og:image（+width・height・alt）/ twitter:card / twitter:title /
     twitter:description / twitter:image -->
```

`</style>` と `</head>` の間:

```html
<link rel="stylesheet" href="../assets/site-chrome.css">
<link rel="stylesheet" href="../assets/site-actions.css">
<script src="../assets/site-actions.js" defer></script>
```

`</dialog>`（ライトボックス）の直後、ページ末尾のインライン `<script>` の前:

```html
<script src="../assets/ambient-particles.js"></script>
```

フッターも生成物のままではサイトの他ページと揃いません。`<footer class="site-footer">` の中身を、他ページと同じ次の形に置き換えます。

```html
<a class="brand footer-brand" href="../" aria-label="SlideCast Studio トップページ">SlideCast <b>Studio</b></a>
<nav class="footer-links" aria-label="フッターナビゲーション"><a href="../intro/">SlideCast Studio とは</a><a href="../manual/">公式マニュアル</a><a href="../bundle-builder/">Bundle Builder</a><a href="../mouthloop-v2/">MouthLoop v2</a></nav>
```

フッターナビは**サイト内リンクだけ**です。note へのリンクは、以前ここに並べていましたが、SNS アイコン行へ移しました。

フッター最下段も生成物には入りません。`<p class="footer-meta">` を `footer-bottom` で包み、SNS アイコン（note / X / YouTube / Substack）の `<nav class="social-links">` を隣に足します。**他ページから丸ごとコピーするのが確実です**（インライン SVG のパスが長いため）。

```html
<div class="footer-bottom">
  <p class="footer-meta">SlideCast Studio ドキュメント · aokuma</p>
  <nav class="social-links" aria-label="SNSリンク"><!-- note / X / YouTube / Substack のアイコンリンク --></nav>
</div>
```

`.footer-bottom` と `.social-link` の見た目は `assets/site-chrome.css` にあるので、CSS 側の追記は不要です。SNS リンクはトップページの CTA 直下（`.cta-social`）にも置いてあります。

`footer-meta` は全ページ共通で `SlideCast Studio ドキュメント · aokuma` です。spec 側の `footer_meta` にも同じ文字列を書いておくと、再生成してもこの行だけは戻りません。note の元記事へのリンクは、フッターナビではなく記事末尾のソースカード（spec の `source_url`）が担当します（フッターの note は SNS アイコン行にあるトップページへのリンクです）。

`site-actions.js` はシェアボタンを組み立てるとき `link[rel=canonical]` と `meta[property="og:title"]` を読みます。canonical と og:title を入れ忘れると、シェアされるURLとタイトルが崩れます。

## ヘッダーとフッターのリンク

ヘッダーは**サイト内の回遊専用**、note へのリンクは**フッターの SNS アイコン行とソースカードに残す**方針です（note 記事の評価につながるため）。以前は 🏠 リンクを生成後に手で挿入していましたが、いまは spec の `nav_links` から生成されます。

```json
"nav_links": [
  { "href": "../", "icon": "🏠", "label": "HOME" },
  { "href": "../manual/", "icon": "📘", "label": "公式マニュアル" }
],
"update_header": false
```

`href` は相対パスです。1階層（`intro/`）は `../`、2階層（`updates/v34/`）は `../../`。`update_header: false` を書かないと、note へのリンクがヘッダーにも出てしまいます。

ヘッダーは全8ページで同じ4項目に揃えています。**🏠 ホーム / 💡 概要 / 📘 マニュアル / ☰ 目次**（目次はテンプレートが自動で付けます）。「紹介」ではなく「概要」です。

spec の `nav_links` から出るのはリンクとラベルだけで、`aria-label`（`ホーム` / `SlideCast Studio とは` / `公式マニュアル`）は生成後に手で足しています。再生成したら入れ直してください。

`manual/`・`updates/v34/`・`updates/v33/` は spec が無いため、ヘッダーを直接編集してあります。

本文中の note 記事へのリンクは、原則としてサイト内に同等ページがあっても差し替えません。ただし**アップデート手順だけは例外**で、`/gas-update/` への内部リンクに統一しています（`intro/`・`manual/`・`updates/v33`・`updates/v34`・トップページ）。元記事へのリンクは `/gas-update/` 末尾のソースカードが担います。

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

`manual/`、`updates/v34/`、`updates/v33/` の3本は、この仕組みを整える前に作られたため、設計データが残っていません。これらを大きく直す場合は、元の Markdown 原稿から spec を作り直す形になります。

画像の外部ファイル化だけは spec 無しで済ませてあります。同じことを別のページでやる場合は次のとおりです（ページを上書きするので、実行前に `--dry-run` で件数を確認してください）。

```bash
python3 _source/tools/externalize_images.py manual/index.html --assets assets --dry-run
python3 _source/tools/externalize_images.py manual/index.html --assets assets
```
