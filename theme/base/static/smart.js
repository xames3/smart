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
    const figures = document.querySelectorAll('#content figure.zoom:not([data-zoom-ready]) > img');
    for (const img of figures) {
        const figure = img.parentElement;
        if (!figure || figure.dataset.zoomReady === 'true') continue;
        if (img.classList.contains('no-zoom')) { figure.dataset.zoomReady = 'true'; continue; }
        const wrapper = document.createElement('div');
        wrapper.className = 'zoom-inner';
        wrapper.style.position = 'relative';
        wrapper.style.overflow = 'hidden';
        wrapper.style.borderRadius = 'var(--radius)';
        wrapper.style.lineHeight = '0';
        wrapper.style.display = 'block';
        img.style.borderRadius = '0';
        img.style.display = 'block';
        img.style.width = '100%';
        img.style.height = 'auto';
        img.style.transformOrigin = 'center';
        img.style.transition = 'transform var(--duration-slow) var(--ease-in-out)';
        figure.insertBefore(wrapper, img);
        wrapper.appendChild(img);
        wrapper.addEventListener('pointerenter', () => { img.style.transform = 'scale(1.05)'; }, { passive: true });
        wrapper.addEventListener('pointerleave', () => { img.style.transform = 'scale(1)'; }, { passive: true });
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
        img.style.transformOrigin = 'center';
        img.style.transition = 'transform var(--duration-slow) var(--ease-in-out)';
        const parent = img.parentElement;
        parent.insertBefore(wrapper, img);
        wrapper.appendChild(img);
        wrapper.addEventListener('pointerenter', () => { img.style.transform = 'scale(1.05)'; }, { passive: true });
        wrapper.addEventListener('pointerleave', () => { img.style.transform = 'scale(1)'; }, { passive: true });
        img.dataset.zoomReady = 'true';
    }
})();

// Sidebar hierarchical navigation toggles
(function () {
    const sidebar = document.getElementById('left-sidebar');
    if (!sidebar) return;
    const listItems = sidebar.querySelectorAll('li');
    let uid = 0;
    for (const li of listItems) {
        if (li.classList.contains('has-children')) continue; // already processed
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
        // Keyboard support on anchor for convenience (Left/Right arrows)
        anchor.addEventListener('keydown', (e) => {
            if (e.key === 'ArrowRight') {
                if (li.getAttribute('aria-expanded') === 'false') btn.click();
            } else if (e.key === 'ArrowLeft') {
                if (li.getAttribute('aria-expanded') === 'true') btn.click();
            }
        });
    }
})();
