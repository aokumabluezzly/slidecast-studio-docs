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
| `intro.en.spec.json` | 英語版の紹介ページ（`/en/intro/index.html`）の設計データ |
| `bundle-builder.en.spec.json` | 英語版の Bundle Builder ガイド（`/en/bundle-builder/index.html`）の設計データ |
| `mouthloop-v2.en.spec.json` | 英語版の MouthLoop v2 ガイド（`/en/mouthloop-v2/index.html`）の設計データ |
| `gas-update.en.spec.json` | 英語版のアップデート方法ガイド（`/en/gas-update/index.html`）の設計データ |
| `img/` | 各 spec が参照する画像。生成時に `/assets/` へコピーされます |
| `article-template.en.html` | **自動生成**。英語ページ用テンプレート（直接編集しない） |
| `tools/build_en.py` | 英語ページを spec から作り直す入口。生成 → 仕上げまで一括 |
| `tools/make_en_template.py` | 標準テンプレートの UI 文言を英語化して `article-template.en.html` を作る |
| `tools/finish_en_page.py` | 生成した英語ページに共通クロームを入れ直す（下記の手作業を自動化したもの） |
| `tools/externalize_images.py` | 設計データが無いページから Base64 画像を抜き出して `/assets/` へ移す移行スクリプト |

テンプレートは `build-rich-html-article` スキル同梱の**標準テンプレートをそのまま使います**。以前このフォルダに置いていた専用テンプレートは、修正内容を標準側へ取り込んだため廃止しました。英語ページだけは、テンプレート側に直接書かれた UI 文言（「本文へスキップ」「目次」など）が日本語のままなので、`make_en_template.py` が標準テンプレートから英語版を作り直しています。

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
  { "href": "../", "icon": "🏠", "label": "HOME" }
],
"update_header": false
```

`href` は相対パスです。1階層（`intro/`）は `../`、2階層（`updates/v34/`）は `../../`。`update_header: false` を書かないと、note へのリンクがヘッダーにも出てしまいます。

ヘッダーは全8ページで同じ4項目に揃えています。**🏠 HOME / 📚 ページ / ☰ 目次 / ☀️テーマ**（目次はテンプレートが自動で付けます）。以前ここに並べていた「概要」「マニュアル」は、📚 ページ一覧メニューの中へ移しました。

spec の `nav_links` から出るのはリンクとラベルだけなので、生成後に次の2つを手で足します。再生成したら入れ直してください。

- 🏠 リンクの `aria-label="トップページ"`
- 🏠 の直後の📚ボタン（下記）

```html
<button class="header-link" type="button" data-site-nav aria-label="ページ一覧"><span aria-hidden="true">📚</span><span class="nav-label">ページ</span></button>
```

`manual/`・`updates/v34/`・`updates/v33/` は spec が無いため、ヘッダーを直接編集してあります。

### 📚 ページ一覧メニュー

トップページに戻らなくても全ページへ移動できるように、ヘッダーの📚ボタンでページ一覧を開けます。PCはヘッダー直下のドロップダウン（クリックで開く。マウス環境ではホバーでも開き、クリックすると開いたまま固定）、スマホは下から出るボトムシートです。Esc・背景タップ・×ボタンで閉じます。

- 一覧の中身は **`assets/site-nav.js` の `PAGES` 配列に1箇所だけ**書いてあります。**ページを増やしたらここに1行足すだけ**で、全8ページのメニューに反映されます（各ページのHTMLを触る必要はありません）。
- `href` はリポジトリのルートからの相対パス（`intro/`、`updates/v34/`、トップは空文字）。ページ側の階層は `script.src` から自動で解決するので、`../` を数える必要はありません。
- 見た目は `assets/site-chrome.css` の「ページ一覧メニュー」ブロック。640px 以下でボトムシートに切り替わります。
- 各ページに必要なのは、ヘッダーの📚ボタン（`data-site-nav`）と `<script src="＜相対パス＞assets/site-nav.js" defer></script>` の2つだけです。
- 520px 以下では `assets/site-actions.css` がヘッダーの3番目（☰目次）を隠します。記事ページには右下のフローティング☰があるためです。**HOME と ページ は隠しません。**

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

## 英語版ページの作り方

英語ページは `/en/` 配下に、日本語と**同じ構造**で置きます（`intro/` → `en/intro/`）。日本語ページの URL は変わりません。

再生成は次の1行だけです。テンプレートの英語化・ビルド・共通クロームの差し込みまで通しでやります。

```bash
python3 _source/tools/build_en.py
```

1本だけ作り直すときは `python3 _source/tools/build_en.py intro` のように名前を渡します。

**日本語ページのように手でクロームを足す必要はありません。** `finish_en_page.py` が canonical・hreflang・ファビコン・OGP・共通CSS/JS・📚ボタン・背景演出・共通フッター（SNSアイコン込み）を毎回入れ直します。SNS アイコンの SVG はトップページ `index.html` から読み取るので、アイコンを変えるときは `index.html` だけ直せば英語ページにも回ります。

### 英語ページを1本増やすときに触る4か所

1. `_source/＜名前＞.en.spec.json` を作る（日本語 spec の翻訳）
2. `_source/tools/build_en.py` の `PAGES` に1行足す
3. `_source/tools/finish_en_page.py` の `PAGE_META` に OGP 用の英語タイトル・説明を足す
4. `assets/site-nav.js` の該当ページに `"en": true` を足す ← これで 🌐 切替が有効になる

日本語ページ側にも `hreflang` を足してください（`index.html` と `intro/index.html` に入っている3行が見本です）。

### 英語 spec で気をつけること

- **内部リンクの階層が1つ深くなります。** `en/intro/` から見たサイト内リンクは `../../bundle-builder/` です（日本語版は `../bundle-builder/`）。`nav_links` の `href: "../"` は英語版でも `../`（= `/en/`）のままで正しいので、そこだけ変えません。
- 英語版が無いページへのリンクには `(Japanese)` を添えます。読者が日本語のページに落ちる前に分かるようにするためです。
- 価格は日本円のまま書きます（note で円建て販売のため）。API 料金の表だけは、為替レートを挟まずに済むよう**日本語版の円表記ではなく米ドルで直接計算**してあります。

### 🌐 言語切替の仕組み

`assets/site-lang.js` がヘッダーに 🌐 ボタンを差し込みます。**自動リダイレクトはしません**（意図しない転送を避けるため、切替は常にユーザー操作）。

- 現在位置が `en/` 配下かどうかで JA / EN を判定します。
- 対になるページの有無は `assets/site-nav.js` の `PAGES`（`window.SlideCastPages`）から引きます。英語版の有無を2か所に書かなくて済むようにするためです。
- そのため **`site-lang.js` は `site-nav.js` より後ろに読み込みます**（どちらも `defer` なので記述順で決まります）。
- 対になるページが無いときは、ボタンを消さずに無効表示にします。英語版が「無い」のか「そもそも多言語対応していない」のかが読者に分かるようにするためです。
- 📚 ページ一覧も英語ページでは英語で出て、英語版が無い項目には `(Japanese)` が付きます。

## 設計データが無い記事

`manual/`、`updates/v34/`、`updates/v33/` の3本は、この仕組みを整える前に作られたため、設計データが残っていません。これらを大きく直す場合は、元の Markdown 原稿から spec を作り直す形になります。

画像の外部ファイル化だけは spec 無しで済ませてあります。同じことを別のページでやる場合は次のとおりです（ページを上書きするので、実行前に `--dry-run` で件数を確認してください）。

```bash
python3 _source/tools/externalize_images.py manual/index.html --assets assets --dry-run
python3 _source/tools/externalize_images.py manual/index.html --assets assets
```
