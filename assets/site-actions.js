(() => {
  'use strict';

  const script = document.currentScript;
  const markUrl = new URL('brand/header-mark-compact.png', script.src).href;
  const canonical = document.querySelector('link[rel="canonical"]')?.href || location.href.split('#')[0];
  const shareTitle = document.querySelector('meta[property="og:title"]')?.content || document.title;
  let installPrompt = null;
  let toastTimer = 0;

  const icons = {
    share: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 16V3m0 0L7.5 7.5M12 3l4.5 4.5"/><path d="M5 11v8h14v-8"/></svg>',
    link: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M9.5 14.5l5-5"/><path d="M7.2 17.8l-1 1a3.5 3.5 0 01-5-5l4-4a3.5 3.5 0 015 0"/><path d="M16.8 6.2l1-1a3.5 3.5 0 015 5l-4 4a3.5 3.5 0 01-5 0"/></svg>',
    home: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 10.5L12 4l8 6.5V20H4z"/><path d="M9 20v-6h6v6"/><path d="M18 3v5"/><path d="M15.5 5.5h5"/></svg>',
    substack: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 5h16M4 9h16M6 13h12v7l-6-3.5L6 20z"/></svg>'
  };

  const showToast = message => {
    let toast = document.querySelector('.share-toast');
    if (!toast) {
      toast = document.createElement('div');
      toast.className = 'share-toast';
      toast.setAttribute('role', 'status');
      toast.setAttribute('aria-live', 'polite');
      document.body.append(toast);
    }
    toast.textContent = message;
    toast.classList.add('is-visible');
    clearTimeout(toastTimer);
    toastTimer = window.setTimeout(() => toast.classList.remove('is-visible'), 2600);
  };

  const copyLink = async () => {
    try {
      await navigator.clipboard.writeText(canonical);
      return true;
    } catch {
      const input = document.createElement('textarea');
      input.value = canonical;
      input.style.position = 'fixed';
      input.style.opacity = '0';
      document.body.append(input);
      input.select();
      const copied = document.execCommand('copy');
      input.remove();
      return copied;
    }
  };

  const describeAction = (element, label) => {
    element.setAttribute('aria-label', label);
    element.dataset.tooltip = label;
    element.title = label;
    return element;
  };

  const makeButton = (className, label, icon, action) => {
    const button = document.createElement('button');
    button.type = 'button';
    button.className = `share-action ${className}`;
    button.innerHTML = icon;
    describeAction(button, label);
    button.addEventListener('click', action);
    return button;
  };

  const showInstallHelp = () => {
    let dialog = document.querySelector('.install-help');
    if (!dialog) {
      dialog = document.createElement('dialog');
      dialog.className = 'install-help';
      const isiOS = /iphone|ipad|ipod/i.test(navigator.userAgent);
      const guide = isiOS
        ? 'Safari下部の共有ボタンを押し、「ホーム画面に追加」を選んでください。'
        : 'ブラウザのメニューを開き、「アプリをインストール」または「ホーム画面に追加」を選んでください。';
      dialog.innerHTML = `<div class="install-help__body"><h2>ホーム画面に追加</h2><p>${guide}</p><button class="install-help__close" type="button">閉じる</button></div>`;
      dialog.querySelector('.install-help__close').addEventListener('click', () => dialog.close());
      dialog.addEventListener('click', event => { if (event.target === dialog) dialog.close(); });
      document.body.append(dialog);
    }
    if (typeof dialog.showModal === 'function') dialog.showModal();
    else showToast('ブラウザのメニューから「ホーム画面に追加」を選んでください');
  };

  const installApp = async () => {
    if (matchMedia('(display-mode: standalone)').matches || navigator.standalone) {
      showToast('このサイトはホーム画面から開かれています');
      return;
    }
    if (!installPrompt) {
      showInstallHelp();
      return;
    }
    installPrompt.prompt();
    await installPrompt.userChoice;
    installPrompt = null;
  };

  window.addEventListener('beforeinstallprompt', event => {
    event.preventDefault();
    installPrompt = event;
  });

  const brand = document.querySelector('.site-header .brand');
  if (brand && !brand.querySelector('.brand-mark')) {
    const mark = document.createElement('img');
    mark.className = 'brand-mark';
    mark.src = markUrl;
    mark.alt = '';
    mark.width = 24;
    mark.height = 34;
    mark.decoding = 'async';
    brand.prepend(mark);
  }

  const hero = document.querySelector('main .hero');
  if (!hero || document.querySelector('.site-share')) return;
  const anchor = hero.nextElementSibling?.classList.contains('stat-strip') ? hero.nextElementSibling : hero;
  const panel = document.createElement('section');
  panel.className = 'site-share';
  panel.setAttribute('aria-label', 'このページの共有メニュー');
  panel.innerHTML = '<div class="site-share__actions"></div>';
  const actions = panel.querySelector('.site-share__actions');

  const xLink = document.createElement('a');
  xLink.className = 'share-action share-action--x';
  xLink.href = `https://twitter.com/intent/tweet?text=${encodeURIComponent(shareTitle)}&url=${encodeURIComponent(canonical)}`;
  xLink.target = '_blank';
  xLink.rel = 'noopener noreferrer';
  describeAction(xLink, 'Xでシェア');
  xLink.innerHTML = '<span class="share-action__x" aria-hidden="true">𝕏</span>';
  actions.append(xLink);

  const lineLink = document.createElement('a');
  lineLink.className = 'share-action share-action--line';
  lineLink.href = `https://social-plugins.line.me/lineit/share?url=${encodeURIComponent(canonical)}&text=${encodeURIComponent(shareTitle)}`;
  lineLink.target = '_blank';
  lineLink.rel = 'noopener noreferrer';
  describeAction(lineLink, 'LINEで送る');
  lineLink.innerHTML = '<span class="share-action__line" aria-hidden="true">LINE</span>';
  actions.append(lineLink);

  actions.append(makeButton('share-action--substack', 'Substackで共有', icons.substack, async () => {
    window.open('https://substack.com/home', '_blank', 'noopener,noreferrer');
    const copied = await copyLink();
    showToast(copied ? 'リンクをコピーしました。SubstackのNoteに貼り付けられます' : 'Substackを開きました。ページURLを貼り付けてください');
  }));

  actions.append(makeButton('share-action--native', '共有メニューを開く', icons.share, async () => {
    if (navigator.share) {
      try { await navigator.share({ title: shareTitle, url: canonical }); }
      catch (error) { if (error.name !== 'AbortError') showToast('共有メニューを開けませんでした'); }
    } else {
      const copied = await copyLink();
      showToast(copied ? 'リンクをコピーしました' : 'リンクをコピーできませんでした');
    }
  }));

  actions.append(makeButton('share-action--copy', 'リンクをコピー', icons.link, async () => {
    const copied = await copyLink();
    showToast(copied ? 'リンクをコピーしました' : 'リンクをコピーできませんでした');
  }));

  actions.append(makeButton('share-action--install', 'ホーム画面に追加', icons.home, installApp));
  anchor.insertAdjacentElement('afterend', panel);
})();
