/* ヘッダーの言語切替（🌐 JA / EN）。
   日本語ページはリポジトリ直下、英語ページは /en/ 配下に同じ構造で置く。
     ja: intro/index.html   ⇔   en: en/intro/index.html

   どのページに英語版があるかは assets/site-nav.js の PAGES（"en": true）が持っています。
   このファイルは台帳を引くだけなので、ページを増やしてもここは触りません。
   **site-nav.js より後ろに読み込んでください**（どちらも defer なので記述順で決まります）。

   自動リダイレクトはしません。意図しない転送を避けるため、切替は常にユーザー操作です。 */
(() => {
  'use strict';

  const script = document.currentScript;
  const site = window.SlideCastPages;
  const root = site ? site.root : new URL('../', script.src);
  const normalize = site ? site.normalize
    : (path => path.replace(/index\.html$/, '').replace(/\/+$/, '/') || '/');

  const rootPath = site ? site.rootPath : normalize(root.pathname);
  const here = site ? site.here : normalize(location.pathname);
  const relative = site ? site.relative : (here.startsWith(rootPath) ? here.slice(rootPath.length) : '');
  const isEnglish = site ? site.lang === 'en' : (relative === 'en/' || relative.startsWith('en/'));

  /* 日本語側から見たパスに揃えて台帳と突き合わせる（トップは空文字） */
  const jaPath = isEnglish ? relative.slice(3) : relative;
  const entry = site
    ? site.pages.flatMap(section => section.items).find(item => item.href === jaPath)
    : null;
  /* 英語ページに居るなら、対の日本語ページは必ずある */
  const paired = isEnglish || (entry ? entry.en === true : false);

  const nav = document.querySelector('.site-header .header-nav');
  if (!nav) return;

  const targetPath = isEnglish ? jaPath : `en/${jaPath}`;
  const label = isEnglish ? 'JA' : 'EN';

  /* 対になるページが無いときは、切替できないことが伝わる無効ボタンを出す。
     ボタンごと消すと、英語版が「無い」のか「そもそも多言語でない」のか分からなくなる */
  const element = document.createElement(paired ? 'a' : 'button');
  element.className = 'header-link lang-switch' + (paired ? '' : ' is-disabled');

  if (paired) {
    element.href = new URL(targetPath, root).pathname;
    element.hreflang = isEnglish ? 'ja' : 'en';
    element.lang = isEnglish ? 'ja' : 'en';
    element.setAttribute('aria-label', isEnglish ? '日本語版に切り替える' : 'Switch to English');
    element.title = isEnglish ? '日本語版' : 'English version';
  } else {
    element.type = 'button';
    element.disabled = true;
    element.setAttribute('aria-disabled', 'true');
    element.setAttribute('aria-label', 'English version of this page is coming soon');
    element.title = 'English version coming soon';
  }

  element.innerHTML = '<span aria-hidden="true">🌐</span><span class="nav-label">' + label + '</span>';

  /* テーマ切替ボタンの手前に入れる（☰目次 の隣） */
  const theme = nav.querySelector('#themeToggle');
  if (theme) nav.insertBefore(element, theme);
  else nav.append(element);
})();
