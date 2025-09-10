window.addEventListener('load', () => {
    const wordsPerMinute = 225;
    const section = document.querySelector('section');
    if (!section) return;
    const paragraphs = section.querySelectorAll('p');
    const totalWordCount = Array.from(paragraphs).reduce((count, p) =>
        count + p.textContent.trim().split(/\s+/).length, 0);
    if (totalWordCount > 0) {
        const readingTime = Math.ceil(totalWordCount / wordsPerMinute);
        const rt = document.getElementById('readingTime');
        if (rt) rt.innerHTML = `<i class='fa-regular fa-stopwatch' style='margin-right: 8px;'></i>${readingTime} min read`;
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

(function () {
    function onScroll() {
        const sc = window.scrollY || document.documentElement.scrollTop;
        const header = document.querySelector('header');
        if (!header) return;
        if (sc > 250) header.classList.add('border-b');
        else header.classList.remove('border-b');
    }
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
})();

// Read CSS duration variables in ms
(function () {
    if (window.smartGetDurationMs) return;
    window.smartGetDurationMs = function (cssVar = '--duration-normal', fallback = 500) {
        try {
            const cs = getComputedStyle(document.documentElement);
            const raw = (cs.getPropertyValue(cssVar) || '').toString().trim();
            if (!raw) return fallback;
            if (raw.endsWith('ms')) return Math.max(0, parseFloat(raw));
            if (raw.endsWith('s')) return Math.max(0, parseFloat(raw) * 1000);
            const n = Number(raw);
            return isNaN(n) ? fallback : n;
        } catch { return fallback; }
    };
})();

// Theme transition helper to ensure color changes fade smoothly
(function () {
    if (window.smartApplyTheme) return;
    window.smartApplyTheme = function (mode, maxWait) {
        const root = document.documentElement;
        const dur = (window.smartGetDurationMs ? smartGetDurationMs('--duration-normal', 500) : 500);
        const debounce = Math.max(60, Math.round(dur * 0.25));
        const fallback = maxWait ?? Math.max(dur * 3, dur + 500);
        root.classList.add('theme-transition');
        requestAnimationFrame(() => {
            root.setAttribute('data-theme', mode);
            let doneTimer;
            function cleanup() {
                root.classList.remove('theme-transition');
                root.removeEventListener('transitionend', onEnd, true);
                if (doneTimer) clearTimeout(doneTimer);
            }
            function onEnd(e) {
                if (!e || !e.propertyName) return;
                if (e.propertyName === 'color' || e.propertyName === 'background-color' || e.propertyName === 'border-color' || e.propertyName === 'fill' || e.propertyName === 'stroke' || e.propertyName === 'box-shadow' || e.propertyName === 'text-decoration-color') {
                    if (doneTimer) clearTimeout(doneTimer);
                    doneTimer = setTimeout(cleanup, debounce);
                }
            }
            root.addEventListener('transitionend', onEnd, true);
            doneTimer = setTimeout(cleanup, fallback);
        });
    };
})();

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
        wrapper.addEventListener('pointerenter', () => { scale.style.transform = 'scale(1.02)'; }, { passive: true });
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

        const scale = document.createElement('div');
        scale.className = 'zoom-scale';
        scale.style.transformOrigin = 'center';
        scale.style.transition = 'transform var(--duration-slow) var(--ease-in-out)';
        scale.style.display = 'block';
        scale.style.lineHeight = '0';

        const parent = img.parentElement;
        parent.insertBefore(wrapper, img);
        wrapper.appendChild(scale);
        scale.appendChild(img);

        wrapper.addEventListener('pointerenter', () => { scale.style.transform = 'scale(1.02)'; }, { passive: true });
        wrapper.addEventListener('pointerleave', () => { scale.style.transform = 'scale(1)'; }, { passive: true });

        img.dataset.zoomReady = 'true';
    }
})();

function initLeftSidebarAccordion() {
    const sidebars = document.querySelectorAll('#left-sidebar, #sidebar, .sidebar');
    if (!sidebars.length) return;
    sidebars.forEach((sidebar) => {
        let uid = 0;
        function setExpanded(li, expanded) {
            li.setAttribute('aria-expanded', expanded ? 'true' : 'false');
        }
        function collapseOthers(except) {
            const open = sidebar.querySelectorAll('li.has-children[aria-expanded="true"]');
            for (const o of open) {
                if (o !== except) setExpanded(o, false);
            }
        }
        function toggle(li) {
            const isOpen = li.getAttribute('aria-expanded') === 'true';
            if (isOpen) setExpanded(li, false); else { collapseOthers(li); setExpanded(li, true); }
        }
        const listItems = sidebar.querySelectorAll('li');
        for (const li of listItems) {
            const childList = li.querySelector(':scope > ul');
            const anchor = li.querySelector(':scope > a, :scope > p > a');
            if (!childList || !anchor) continue;
            childList.removeAttribute('hidden');
            childList.style.removeProperty('display');
            li.classList.add('has-children');
            const controlId = childList.id || `nav-branch-${++uid}`;
            childList.id = controlId;
            const btn = li.querySelector(':scope > button.nav-toggle, :scope > a > button.nav-toggle');
            if (btn) btn.setAttribute('aria-controls', controlId);
            const branchIsCurrent = li.classList.contains('current') || anchor.classList.contains('current') || !!li.querySelector(':scope > ul .current');
            if (branchIsCurrent) {
                setExpanded(li, false);
                requestAnimationFrame(() => setExpanded(li, true));
            } else {
                setExpanded(li, false);
            }
            // Allow link to navigate; only the chevron button toggles
            if (btn) btn.addEventListener('click', (e) => { e.preventDefault(); e.stopPropagation(); toggle(li); }, { passive: false });
            anchor.addEventListener('click', (e) => {
                const href = anchor.getAttribute('href') || '';
                if (href && !href.startsWith('#')) {
                    e.preventDefault();
                    e.stopPropagation();
                    collapseOthers(li);
                    setExpanded(li, true);
                    const d = (window.smartGetDurationMs ? smartGetDurationMs('--duration-normal', 500) : 500);
                    setTimeout(() => { window.location.href = href; }, d);
                } else {
                    e.preventDefault();
                    e.stopPropagation();
                    toggle(li);
                }
            }, { passive: false });
            anchor.addEventListener('keydown', (e) => {
                if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); e.stopPropagation(); toggle(li); }
                if (e.key === 'ArrowRight') { e.preventDefault(); e.stopPropagation(); collapseOthers(li); setExpanded(li, true); }
                if (e.key === 'ArrowLeft') { e.preventDefault(); e.stopPropagation(); setExpanded(li, false); }
            });
        }
        sidebar.addEventListener('click', (e) => {
            const toggleBtn = e.target.closest('button.nav-toggle');
            if (toggleBtn && sidebar.contains(toggleBtn)) {
                const li = toggleBtn.closest('li');
                if (li && li.classList.contains('has-children')) {
                    e.preventDefault();
                    e.stopPropagation();
                    toggle(li);
                    return;
                }
            }
        }, { passive: false });
        // Keyboard activation uses the button's native behavior (Enter/Space)
        const expanded = sidebar.querySelectorAll('li.has-children[aria-expanded="true"]');
        if (expanded.length > 1) {
            let keep = Array.from(expanded).find(li => li.querySelector(':scope .current')) || expanded[0];
            collapseOthers(keep);
        }
    });
}

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initLeftSidebarAccordion);
} else {
    initLeftSidebarAccordion();
}

(function () {
    try {
        document.querySelectorAll('[x-cloak]').forEach(el => { el.removeAttribute('x-cloak'); el.style.removeProperty('display'); });
    } catch { }
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
        const closers = qsAll('[data-sidebar-close]');
        function open() {
            document.body.classList.add('sidebar-open');
        }
        function close() {
            document.body.classList.remove('sidebar-open');
        }
        function toggle(e) {
            if (e) e.preventDefault();
            if (document.body.classList.contains('sidebar-open')) close();
            else open();
        }
        toggles.forEach(btn => btn.addEventListener('click', toggle, { passive: false }));
        backdrop.addEventListener('click', close);
        closers.forEach(btn => btn.addEventListener('click', (e) => { e.preventDefault(); close(); }));
        document.addEventListener('keydown', e => { if (e.key === 'Escape') close(); });
        sidebar.addEventListener('click', e => { if (e.target.closest('a')) close(); });
        let lastW = window.innerWidth;
        window.addEventListener('resize', () => {
            const w = window.innerWidth;
            if (w !== lastW) {
                if (w >= 1024) close();
                lastW = w;
            }
        }, { passive: true });
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initMobileSidebar, { once: true });
    } else {
        initMobileSidebar();
    }
})();

(function () {
    function initTOCScrollSpy() {
        const tocSidebar = document.getElementById('right-sidebar');
        if (!tocSidebar) return;
        const tocLinks = tocSidebar.querySelectorAll('a[href^="#"]');
        const headings = [];
        tocLinks.forEach(link => {
            const href = link.getAttribute('href');
            if (href && href.startsWith('#')) {
                const targetId = href.substring(1);
                const heading = document.getElementById(targetId);
                if (heading) {
                    headings.push({
                        id: targetId,
                        element: heading,
                        link: link,
                        offsetTop: heading.offsetTop
                    });
                }
            }
        });
        if (headings.length === 0) return;
        headings.sort((a, b) => a.offsetTop - b.offsetTop);
        function updateActiveTOC() {
            const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
            const windowHeight = window.innerHeight;
            const documentHeight = document.documentElement.scrollHeight;
            const headerOffset = 250;
            let currentHeading = null;
            const isNearBottom = scrollTop + windowHeight >= documentHeight - 250;
            if (isNearBottom && headings.length > 0) {
                currentHeading = headings[headings.length - 1];
            } else {
                for (let i = headings.length - 1; i >= 0; i--) {
                    const heading = headings[i];
                    if (scrollTop + headerOffset >= heading.offsetTop - 500) {
                        currentHeading = heading;
                        break;
                    }
                }
            }
            if (scrollTop < 100) {
                currentHeading = null;
            }
            tocLinks.forEach(link => {
                link.classList.remove('toc-active');
                link.style.color = '';
            });
            if (currentHeading) {
                currentHeading.link.classList.add('toc-active');
                currentHeading.link.style.color = 'hsl(var(--foreground))';
            }
        }
        let ticking = false;
        function onScroll() {
            if (!ticking) {
                requestAnimationFrame(() => {
                    updateActiveTOC();
                    ticking = false;
                });
                ticking = true;
            }
        }
        window.addEventListener('scroll', onScroll, { passive: true });
        window.addEventListener('resize', () => {
            headings.forEach(heading => {
                heading.offsetTop = heading.element.offsetTop;
            });
            updateActiveTOC();
        });
        updateActiveTOC();
    }
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initTOCScrollSpy);
    } else {
        initTOCScrollSpy();
    }
})();

(function () {
    function initPlaceholderAnimation() {
        const input = document.querySelector(".DocSearch-Button-Placeholder");
        if (!input) {
            setTimeout(initPlaceholderAnimation, 100);
            return;
        }
        function generatePlaceholders() {
            const navLinks = document.querySelectorAll('#left-sidebar a, nav a, .toctree a');
            const pageNames = new Set();
            navLinks.forEach(link => {
                const href = link.getAttribute('href');
                if (href && !href.startsWith('#') && !href.startsWith('http')) {
                    const text = link.textContent.trim();
                    if (text && text.length > 2 &&
                        !text.match(/^(home|index|back|next|previous|toc|contents)$/i)) {
                        pageNames.add(text);
                    }
                }
            });
            if (pageNames.size < 3) {
                const headings = document.querySelectorAll('h1, h2, .document-title, .page-title');
                headings.forEach(heading => {
                    const text = heading.textContent.trim();
                    if (text && text.length > 2) {
                        pageNames.add(text);
                    }
                });
            }
            const titles = Array.from(pageNames).slice(0, 6);
            const prefixes = ['Search for', 'Read more about', 'Explore', 'Discover', 'Learn about'];
            const placeholders = [];
            titles.forEach((title, index) => {
                const prefix = prefixes[index % prefixes.length];
                placeholders.push(`${prefix} ${title}`);
            });
            if (placeholders.length === 0) {
                return [
                    "Search for content",
                    "Find documentation",
                    "Explore projects",
                    "Discover guides"
                ];
            }
            return placeholders;
        }
        const placeholders = generatePlaceholders();
        let currentText = '';
        let placeholderIndex = 0;
        let charIndex = 0;
        let typing = true;
        function typePlaceholder() {
            const fullText = placeholders[placeholderIndex];
            if (typing) {
                currentText = fullText.slice(0, charIndex++);
                input.textContent = currentText;
                if (charIndex > fullText.length) {
                    typing = false;
                    setTimeout(typePlaceholder, 5500);
                    return;
                }
            } else {
                currentText = fullText.slice(0, --charIndex);
                input.textContent = currentText;
                if (charIndex === 0) {
                    typing = true;
                    placeholderIndex = (placeholderIndex + 1) % placeholders.length;
                }
            }
            const delay = typing ? 100 : 50;
            setTimeout(typePlaceholder, delay);
        }
        typePlaceholder();
    }
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initPlaceholderAnimation);
    }
})();

document.addEventListener('DOMContentLoaded', function () {
    const h1Elements = document.querySelectorAll('h1');
    h1Elements.forEach(h1 => {
        const originalText = h1.textContent;
        const trimmedText = originalText.replace(/^\s+/, '');
        if (originalText !== trimmedText) {
            h1.textContent = trimmedText;
        }
    });
});

(function () {
    function intersectOnce(nodes, onEnter) {
        const list = Array.from(nodes);
        if (!list.length) return;
        if (!('IntersectionObserver' in window)) {
            list.forEach(onEnter);
            return;
        }
        const io = new IntersectionObserver((entries) => {
            for (const e of entries) {
                if (e.isIntersecting) {
                    io.unobserve(e.target);
                    onEnter(e.target);
                }
            }
        }, { rootMargin: '200px' });
        list.forEach(n => io.observe(n));
    }

    function withTimeout(promise, ms) {
        const ctrl = new AbortController();
        const t = setTimeout(() => ctrl.abort(), ms);
        return Promise.race([
            fetch(promise, { signal: ctrl.signal }),
            new Promise((_, rej) => setTimeout(() => rej(new Error('timeout')), ms + 10))
        ]).finally(() => clearTimeout(t));
    }

    async function enrichYouTubeCard(card) {
        if (card.dataset.youtubeEnriched === '1') return;
        const vid = card.getAttribute('data-youtube-id');
        if (!vid) { card.dataset.youtubeEnriched = '1'; return; }
        const titleEl = card.querySelector('.youtube-title');
        const channelEl = card.querySelector('.youtube-channel');
        const url = 'https://www.youtube.com/oembed?url=' + encodeURIComponent('https://www.youtube.com/watch?v=' + vid) + '&format=json';
        try {
            const res = await withTimeout(url, 8000);
            if (!res.ok) throw new Error(String(res.status));
            const data = await res.json();
            if (titleEl) titleEl.textContent = data.title;
            if (channelEl) channelEl.textContent = data.author_name;
        } catch (_) {
        } finally {
            card.dataset.youtubeEnriched = '1';
        }
    }

    function bootYouTubeOEmbed() {
        const cards = document.querySelectorAll('.youtube-card-container[data-youtube-id]');
        intersectOnce(cards, enrichYouTubeCard);
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', bootYouTubeOEmbed);
    } else {
        bootYouTubeOEmbed();
    }
})();
