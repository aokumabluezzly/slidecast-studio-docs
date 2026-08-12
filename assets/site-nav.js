/* ヘッダーの「ページ」メニュー。
   ページを1本足したら、ここの PAGES に1行足すだけで全ページのメニューに載ります。
   href はリポジトリのルートからの相対パス。各ページの階層は script.src から自動で解決します。 */
(() => {
  'use strict';

  const script = document.currentScript;
  const root = new URL('../', script.src);

  const PAGES = [
    {
      group: 'はじめに',
      items: [
        { href: '', icon: '🏠', label: 'HOME', desc: 'ドキュメントの入口' },
        { href: 'intro/', icon: '💡', label: 'SlideCast Studio とは', desc: 'できること・料金の概要' },
        { href: 'manual/', icon: '📘', label: '公式マニュアル', desc: '全機能の使い方リファレンス' }
      ]
    },
    {
      group: 'ガイド',
      items: [
        { href: 'bundle-builder/', icon: '🧩', label: 'SlideCast Bundle Builder', desc: '資料・台本・AI音声をまとめて準備' },
        { href: 'mouthloop-v2/', icon: '😀', label: 'MouthLoop v2', desc: '画像1枚から口パクキャラ素材を作る' },
        { href: 'gas-update/', icon: '🔄', label: 'アップデート方法（GAS版）', desc: 'データを引き継いだまま最新版へ' }
      ]
    },
    {
      group: '更新履歴',
      items: [
        { href: 'updates/v34/', icon: '🆕', label: 'v3.4「NUANCE」', desc: '表情・ポーズ仕草・おまかせ演技' },
        { href: 'updates/v33/', icon: '📌', label: 'v3.3「SYNC」', desc: 'キャラ設定まわりの作り直し' }
      ]
    }
  ];

  const trigger = document.querySelector('[data-site-nav]');
  const header = document.querySelector('.site-header');
  if (!trigger || !header) return;

  /* 末尾の index.html と重複スラッシュを落として比べる */
  const normalize = path => path.replace(/index\.html$/, '').replace(/\/+$/, '/') || '/';
  const here = normalize(location.pathname);

  const escape = text => text.replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));

  const groupsHtml = PAGES.map(section => {
    const links = section.items.map(item => {
      const url = new URL(item.href, root);
      const current = normalize(url.pathname) === here;
      return `<li><a class="pagenav-item${current ? ' is-current' : ''}" href="${url.pathname}"${current ? ' aria-current="page"' : ''}>` +
        `<span class="pagenav-icon" aria-hidden="true">${item.icon}</span>` +
        `<span class="pagenav-text"><b>${escape(item.label)}</b><small>${escape(item.desc)}</small></span>` +
        `</a></li>`;
    }).join('');
    return `<section class="pagenav-group"><h2 class="pagenav-group-title">${escape(section.group)}</h2><ul>${links}</ul></section>`;
  }).join('');

  const wrapper = document.createElement('div');
  wrapper.className = 'pagenav';
  wrapper.hidden = true;
  wrapper.innerHTML =
    `<div class="pagenav-backdrop" data-pagenav-close></div>` +
    `<div class="pagenav-panel" role="dialog" aria-label="ページ一覧" aria-modal="false">` +
      `<div class="pagenav-head"><strong>ページ一覧</strong>` +
      `<button class="pagenav-close" type="button" aria-label="ページ一覧を閉じる" data-pagenav-close>×</button></div>` +
      `<div class="pagenav-body">${groupsHtml}</div>` +
    `</div>`;
  document.body.append(wrapper);

  const panel = wrapper.querySelector('.pagenav-panel');
  const desktop = () => window.matchMedia('(min-width: 641px)').matches;
  let open = false;
  let pinned = false;
  let hoverTimer = 0;

  /* デスクトップのドロップダウンは、ヘッダーの内側の右端に合わせる。
     .site-header は backdrop-filter を持つため position:fixed の基準になれない。
     そのぶんパネルは body 直下に置き、位置を測って CSS 変数で渡している。 */
  const place = () => {
    if (!desktop()) {
      panel.style.removeProperty('--pagenav-top');
      panel.style.removeProperty('--pagenav-right');
      return;
    }
    const inner = header.querySelector('.wrap, .header-inner') || header;
    const rect = inner.getBoundingClientRect();
    panel.style.setProperty('--pagenav-top', `${Math.max(header.getBoundingClientRect().bottom, 0) + 8}px`);
    panel.style.setProperty('--pagenav-right', `${Math.max(document.documentElement.clientWidth - rect.right, 8)}px`);
  };

  const setOpen = next => {
    if (open === next) return;
    open = next;
    trigger.setAttribute('aria-expanded', String(next));
    if (next) {
      wrapper.hidden = false;
      place();
      requestAnimationFrame(() => wrapper.classList.add('is-open'));
      if (!desktop()) document.body.classList.add('pagenav-locked');
    } else {
      pinned = false;
      wrapper.classList.remove('is-open');
      document.body.classList.remove('pagenav-locked');
      const hide = () => { if (!open) wrapper.hidden = true; };
      window.setTimeout(hide, 200);
    }
  };

  trigger.setAttribute('aria-expanded', 'false');
  trigger.setAttribute('aria-haspopup', 'true');

  /* ホバーで開いた直後のクリックは「閉じる」ではなく「固定」。
     マウスを動かした時点で開いているので、ここで toggle すると押した瞬間に閉じてしまう */
  trigger.addEventListener('click', event => {
    event.preventDefault();
    if (open && !pinned) {
      pinned = true;
      window.clearTimeout(hoverTimer);
      return;
    }
    pinned = !open;
    setOpen(!open);
  });

  wrapper.addEventListener('click', event => {
    if (event.target.closest('[data-pagenav-close]')) setOpen(false);
  });

  document.addEventListener('click', event => {
    if (!open) return;
    if (trigger.contains(event.target) || panel.contains(event.target)) return;
    setOpen(false);
  });

  document.addEventListener('keydown', event => {
    if (event.key !== 'Escape' || !open) return;
    setOpen(false);
    trigger.focus();
  });

  window.addEventListener('resize', () => { if (open) place(); });
  window.addEventListener('scroll', () => { if (open && desktop()) place(); }, { passive: true });

  /* ホバーで開くのはマウス環境だけ。タッチでは1回目のタップが吸われるため付けない */
  if (window.matchMedia('(hover: hover) and (pointer: fine)').matches) {
    const enter = () => {
      window.clearTimeout(hoverTimer);
      if (desktop()) setOpen(true);
    };
    const leave = () => {
      window.clearTimeout(hoverTimer);
      hoverTimer = window.setTimeout(() => { if (!pinned) setOpen(false); }, 220);
    };
    [trigger, panel].forEach(element => {
      element.addEventListener('pointerenter', enter);
      element.addEventListener('pointerleave', leave);
    });
  }
})();
