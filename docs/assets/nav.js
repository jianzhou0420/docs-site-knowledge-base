// docs-site — small client-side behaviors.
// Pure-vanilla, no deps. Loaded at end of <body> by every page.

(function () {
  // ----- theme toggle -----
  var html = document.documentElement;
  var toggle = document.querySelector('.theme-toggle');
  function applyIcon() {
    if (!toggle) return;
    toggle.textContent = html.getAttribute('data-theme') === 'dark' ? '☀️' : '🌙';
  }
  applyIcon();
  if (toggle) {
    toggle.addEventListener('click', function () {
      var cur = html.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
      html.setAttribute('data-theme', cur);
      localStorage.setItem('site-theme', cur);
      applyIcon();
    });
  }

  // ----- mobile nav drawer -----
  var navToggle = document.querySelector('.mobile-nav-toggle');
  if (navToggle) {
    navToggle.addEventListener('click', function () {
      document.body.classList.toggle('nav-open');
    });
    // close drawer when a sidebar link is clicked (mobile only)
    document.querySelectorAll('.sidebar-left a').forEach(function (a) {
      a.addEventListener('click', function () {
        document.body.classList.remove('nav-open');
      });
    });
  }

  // ----- nested sidebar: link inside <summary> should navigate, not toggle -----
  document.querySelectorAll('.sb-subsection > summary .sb-group-link').forEach(function (a) {
    a.addEventListener('click', function (e) { e.stopPropagation(); });
  });

  // ----- persist sidebar divider open/closed across navigation -----
  // The baked HTML only opens the branch containing the active page, so without
  // this, navigating to another page collapses every other divider. We remember
  // the user's expand/collapse choices (per browser session) and restore them on
  // load — never collapsing the branch that holds the active page.
  (function () {
    var STORE = 'sb-open';
    var state = {};
    try { state = JSON.parse(sessionStorage.getItem(STORE) || '{}'); } catch (_) {}
    function persist() {
      try { sessionStorage.setItem(STORE, JSON.stringify(state)); } catch (_) {}
    }
    document.querySelectorAll('.sidebar-left details[data-key]').forEach(function (d) {
      var key = d.getAttribute('data-key');
      var hasActive = !!d.querySelector('.active');
      if (key in state) {
        if (state[key]) d.open = true;
        else if (!hasActive) d.open = false; // never fold the active branch
      }
      d.addEventListener('toggle', function () { state[key] = d.open; persist(); });
    });
  })();

  // ----- right-TOC active-section highlighting via IntersectionObserver -----
  var tocLinks = document.querySelectorAll('.sidebar-right a[href^="#"]');
  if (tocLinks.length && 'IntersectionObserver' in window) {
    var linkMap = {};
    tocLinks.forEach(function (a) { linkMap[a.getAttribute('href').slice(1)] = a; });

    var lastActive = null;
    function activate(id) {
      if (lastActive) lastActive.classList.remove('toc-active');
      var a = linkMap[id];
      if (a) { a.classList.add('toc-active'); lastActive = a; }
    }

    var headings = Object.keys(linkMap)
      .map(function (id) { return document.getElementById(id); })
      .filter(Boolean);

    var observer = new IntersectionObserver(function (entries) {
      // Pick the topmost intersecting heading
      var visible = entries.filter(function (e) { return e.isIntersecting; });
      if (visible.length) {
        visible.sort(function (a, b) { return a.boundingClientRect.top - b.boundingClientRect.top; });
        activate(visible[0].target.id);
      }
    }, { rootMargin: '-80px 0px -70% 0px', threshold: 0 });

    headings.forEach(function (h) { observer.observe(h); });
  }

  // ----- client-side search -----
  // Zero-dependency: a flat index (assets/search-index.json) is baked by
  // _wrap_handwritten.py from every page's title + body text. We fetch it
  // lazily on first open and filter in the browser. Links are resolved
  // against data-asset-prefix on <body> so they work at any folder depth and
  // under any GitHub Pages base path.
  (function () {
    var btn = document.querySelector('.search-btn');
    if (!btn) return;
    var PREFIX = document.body.getAttribute('data-asset-prefix') || '';
    var index = null;            // lazily fetched array of {title,url,text}
    var overlay, input, list;    // built on first open
    var results = [];
    var sel = -1;

    function build() {
      overlay = document.createElement('div');
      overlay.className = 'search-overlay';
      overlay.innerHTML =
        '<div class="search-modal" role="dialog" aria-label="Search">' +
        '<input class="search-input" type="search" placeholder="Search…" aria-label="Search query" autocomplete="off" spellcheck="false">' +
        '<div class="search-results"></div>' +
        '<div class="search-hint">↑↓ navigate · ↵ open · esc close</div>' +
        '</div>';
      document.body.appendChild(overlay);
      input = overlay.querySelector('.search-input');
      list = overlay.querySelector('.search-results');
      overlay.addEventListener('click', function (e) { if (e.target === overlay) close(); });
      input.addEventListener('input', function () { render(input.value); });
      input.addEventListener('keydown', onKey);
    }

    function open() {
      if (!overlay) build();
      overlay.classList.add('open');
      document.body.classList.add('search-open');
      input.value = '';
      render('');
      input.focus();
      if (index === null) {
        fetch(PREFIX + 'assets/search-index.json')
          .then(function (r) { return r.json(); })
          .then(function (data) { index = data; render(input.value); })
          .catch(function () { index = []; render(input.value); });
      }
    }

    function close() {
      if (overlay) overlay.classList.remove('open');
      document.body.classList.remove('search-open');
    }

    function hint(msg) {
      var d = document.createElement('div');
      d.className = 'search-empty';
      d.textContent = msg;
      return d;
    }

    function render(q) {
      q = q.trim().toLowerCase();
      list.innerHTML = '';
      sel = -1;
      results = [];
      if (!q) {
        list.appendChild(hint(index === null ? 'Loading…'
          : 'Type to search ' + index.length + ' page' + (index.length === 1 ? '' : 's') + '.'));
        return;
      }
      if (!index) { list.appendChild(hint('Loading…')); return; }
      results = index.filter(function (e) {
        return e.title.toLowerCase().indexOf(q) !== -1 || e.text.toLowerCase().indexOf(q) !== -1;
      }).slice(0, 20);
      if (!results.length) { list.appendChild(hint('No matches.')); return; }
      results.forEach(function (e, i) { list.appendChild(row(e, q, i)); });
      select(0);
    }

    function row(e, q, i) {
      var a = document.createElement('a');
      a.className = 'search-result';
      a.href = PREFIX + e.url;
      var t = document.createElement('div');
      t.className = 'search-result-title';
      t.textContent = e.title;
      var s = document.createElement('div');
      s.className = 'search-result-snippet';
      s.appendChild(snippet(e.text, q));
      a.appendChild(t);
      a.appendChild(s);
      a.addEventListener('mouseenter', function () { select(i); });
      return a;
    }

    function snippet(text, q) {
      var frag = document.createDocumentFragment();
      var lo = text.toLowerCase().indexOf(q);
      if (lo === -1) {
        frag.appendChild(document.createTextNode(text.slice(0, 120) + (text.length > 120 ? '…' : '')));
        return frag;
      }
      var start = Math.max(0, lo - 40);
      frag.appendChild(document.createTextNode((start > 0 ? '…' : '') + text.slice(start, lo)));
      var mk = document.createElement('mark');
      mk.textContent = text.slice(lo, lo + q.length);
      frag.appendChild(mk);
      var end = lo + q.length;
      frag.appendChild(document.createTextNode(text.slice(end, end + 80) + (end + 80 < text.length ? '…' : '')));
      return frag;
    }

    function select(i) {
      var rows = list.querySelectorAll('.search-result');
      if (!rows.length) { sel = -1; return; }
      sel = (i + rows.length) % rows.length;
      rows.forEach(function (r, j) { r.classList.toggle('sel', j === sel); });
      rows[sel].scrollIntoView({ block: 'nearest' });
    }

    function onKey(e) {
      if (e.key === 'ArrowDown') { e.preventDefault(); select(sel + 1); }
      else if (e.key === 'ArrowUp') { e.preventDefault(); select(sel - 1); }
      else if (e.key === 'Enter') {
        var rows = list.querySelectorAll('.search-result');
        if (rows[sel]) { e.preventDefault(); window.location.href = rows[sel].href; }
      } else if (e.key === 'Escape') { close(); }
    }

    btn.addEventListener('click', open);
    document.addEventListener('keydown', function (e) {
      var open_ = document.body.classList.contains('search-open');
      var typing = /^(INPUT|TEXTAREA|SELECT)$/.test((document.activeElement || {}).tagName || '');
      if (e.key === '/' && !typing && !open_) { e.preventDefault(); open(); }
      else if (e.key === 'Escape' && open_) { close(); }
    });
  })();
})();
