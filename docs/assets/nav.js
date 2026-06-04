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

  // ----- search button placeholder -----
  var searchBtn = document.querySelector('.search-btn');
  if (searchBtn) {
    searchBtn.addEventListener('click', function () {
      alert('Search coming soon. For now, use the sidebar or browser Ctrl+F.');
    });
  }
})();
