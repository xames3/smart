window.addEventListener('load', () => {
    const wordsPerMinute = 550;
    const section = document.querySelector('section');
    if (!section) return;
    const paragraphs = section.querySelectorAll('p');
    const totalWordCount = Array.from(paragraphs).reduce((count, p) =>
        count + p.textContent.trim().split(/\s+/).length, 0);
    if (totalWordCount > 0) {
        const readingTime = Math.ceil(totalWordCount / wordsPerMinute);
        const rt = document.getElementById('readingTime');
        if (rt) rt.innerHTML = `<i class='fa-regular fa-timer' style='margin-right: 8px;'></i>${readingTime} min read`;
    }
});

document.addEventListener('DOMContentLoaded', function () {
    const links = document.querySelectorAll('a[href^="#"]');
    for (const link of links) {
        link.addEventListener('click', function (event) {
            if (this.getAttribute('href') === '#') return;
            event.preventDefault();
            const targetId = this.getAttribute('href').substring(1);
            const targetElement = document.getElementById(targetId);
            if (targetElement) targetElement.scrollIntoView({ behavior: 'smooth' });
        });
    }
});

$(window).scroll(function () {
    if ($(this).scrollTop() > 250) $('header').addClass('border-b');
    else $('header').removeClass('border-b');
});

(function () {
    const interactives = document.querySelectorAll('.sd-card, .admonition, a:not(.headerlink), button');
    for (const el of interactives) {
        el.addEventListener('pointerdown', () => el.classList.add('is-active'), { passive: true });
        el.addEventListener('pointerup', () => el.classList.remove('is-active'), { passive: true });
        el.addEventListener('pointerleave', () => el.classList.remove('is-active'), { passive: true });
        el.addEventListener('blur', () => el.classList.remove('is-active'), { passive: true });
    }
})();

(function () {
    const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (reduce) return;
    const figures = document.querySelectorAll('#content figure.zoom:not([data-zoom-ready]) > :is(img, .face-tag-wrap)');
    for (const el of figures) {
        const figure = el.parentElement;
        if (!figure || figure.dataset.zoomReady === 'true') continue;
        const isFaceWrap = el.classList && el.classList.contains('face-tag-wrap');
        const img = isFaceWrap ? el.querySelector('img') : el;
        if (!img) { figure.dataset.zoomReady = 'true'; continue; }
        if (img.classList.contains('no-zoom')) { figure.dataset.zoomReady = 'true'; continue; }
        const wrapper = document.createElement('div');
        wrapper.className = 'zoom-inner';
        wrapper.style.position = 'relative';
        wrapper.style.overflow = 'hidden';
        wrapper.style.borderRadius = 'var(--radius)';
        wrapper.style.lineHeight = '0';
        wrapper.style.display = 'block';
        if (isFaceWrap) {
            el.style.display = 'block';
            el.style.lineHeight = '0';
        } else if (img instanceof HTMLImageElement) {
            img.style.borderRadius = '0';
            img.style.display = 'block';
            img.style.width = '100%';
            img.style.height = 'auto';
        }
        const scale = document.createElement('div');
        scale.className = 'zoom-scale';
        scale.style.transformOrigin = 'center';
        scale.style.transition = 'transform var(--duration-slow) var(--ease-in-out)';
        scale.style.display = 'block';
        scale.style.lineHeight = '0';
        figure.insertBefore(wrapper, el);
        wrapper.appendChild(scale);
        scale.appendChild(el);
        wrapper.addEventListener('pointerenter', () => { scale.style.transform = 'scale(1.05)'; }, { passive: true });
        wrapper.addEventListener('pointerleave', () => { scale.style.transform = 'scale(1)'; }, { passive: true });
        figure.dataset.zoomReady = 'true';
    }
    const singles = document.querySelectorAll('#content img.zoom:not(figure img):not(.no-zoom):not([data-zoom-ready])');
    for (const img of singles) {
        if (img.dataset.zoomReady === 'true') continue;
        const wrapper = document.createElement('div');
        wrapper.className = 'zoom-inner';
        wrapper.style.position = 'relative';
        wrapper.style.overflow = 'hidden';
        wrapper.style.borderRadius = 'var(--radius)';
        wrapper.style.lineHeight = '0';
        wrapper.style.display = 'block';
        wrapper.style.margin = window.getComputedStyle(img).margin || '60px auto';
        img.style.margin = '0';
        img.style.borderRadius = '0';
        img.style.display = 'block';
        img.style.width = '100%';
        img.style.height = 'auto';
        const parent = img.parentElement;
        parent.insertBefore(wrapper, img);
        wrapper.appendChild(img);
        img.dataset.zoomReady = 'true';
    }
})();

(function () {
    const sidebar = document.getElementById('left-sidebar');
    if (!sidebar) return;
    const listItems = sidebar.querySelectorAll('li');
    let uid = 0;
    for (const li of listItems) {
        if (li.classList.contains('has-children')) continue;
        const childList = li.querySelector(':scope > ul');
        if (!childList) continue;
        const anchor = li.querySelector(':scope > a');
        if (!anchor) continue;
        li.classList.add('has-children');
        const controlId = childList.id || `nav-branch-${++uid}`;
        childList.id = controlId;
        const btn = document.createElement('button');
        btn.type = 'button';
        btn.className = 'nav-toggle';
        btn.setAttribute('aria-label', 'Toggle section');
        btn.setAttribute('aria-controls', controlId);
        const branchIsCurrent = li.classList.contains('current') || anchor.classList.contains('current') || !!li.querySelector(':scope > ul .current');
        if (branchIsCurrent) {
            li.setAttribute('aria-expanded', 'true');
        } else {
            li.setAttribute('aria-expanded', 'false');
            childList.hidden = true;
        }
        anchor.insertAdjacentElement('afterend', btn);
        btn.addEventListener('click', () => {
            const expanded = li.getAttribute('aria-expanded') === 'true';
            const nextState = !expanded;
            li.setAttribute('aria-expanded', String(nextState));
            btn.setAttribute('aria-expanded', String(nextState));
            if (expanded) {
                childList.hidden = true;
                childList.style.display = 'none';
            } else {
                childList.hidden = false;
                childList.style.display = '';
            }
        }, { passive: true });
        anchor.addEventListener('keydown', (e) => {
            if (e.key === 'ArrowRight') {
                if (li.getAttribute('aria-expanded') === 'false') btn.click();
            } else if (e.key === 'ArrowLeft') {
                if (li.getAttribute('aria-expanded') === 'true') btn.click();
            }
        });
    }
})();

(function () {
  if (document.body.dataset.sidebarInit === '1') return;
  document.body.dataset.sidebarInit = '1';

  function qsAll(sel, root = document) {
    return Array.from(root.querySelectorAll(sel));
  }

  function initMobileSidebar() {
    const sidebar = document.querySelector('#left-sidebar, #sidebar, .sidebar');
    if (!sidebar) return;

    let backdrop = document.querySelector('.sidebar-backdrop');
    if (!backdrop) {
      backdrop = document.createElement('div');
      backdrop.className = 'sidebar-backdrop';
      document.body.appendChild(backdrop);
    }

    const toggles = qsAll('[data-sidebar-toggle], .sidebar-toggle, #sidebar-toggle, [aria-controls="sidebar"]');
    function open() {
      document.body.classList.add('sidebar-open');
    }
    function close() {
      document.body.classList.remove('sidebar-open');
    }
    function toggle(e) {
      if (e) e.preventDefault();
      document.body.classList.toggle('sidebar-open');
    }

    toggles.forEach(btn => btn.addEventListener('click', toggle, { passive: false }));
    backdrop.addEventListener('click', close);

    document.addEventListener('keydown', e => {
      if (e.key === 'Escape') close();
    });

    sidebar.addEventListener('click', e => {
      const a = e.target.closest('a');
      if (!a) return;
      if (window.matchMedia('(max-width: 1024px)').matches) {
        close();
      }
    });

    let lastW = window.innerWidth;
    window.addEventListener('resize', () => {
      const w = window.innerWidth;
      if (lastW <= 1024 && w > 1024) {
        close();
      }
      lastW = w;
    }, { passive: true });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initMobileSidebar, { once: true });
  } else {
    initMobileSidebar();
  }
})();
