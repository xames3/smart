window.addEventListener('load', () => {
    const wordsPerMinute = 550;
    const section = document.querySelector('section');
    if (!section) return;
    const paragraphs = section.querySelectorAll('p');
    const totalWordCount = Array.from(paragraphs).reduce((count, p) =>
        count + p.textContent.trim().split(/\s+/).length, 0);
    if (totalWordCount > 0) {
        const readingTime = Math.ceil(totalWordCount / wordsPerMinute);
        document.getElementById('readingTime').innerHTML = `<i class='fa-regular fa-timer' style='margin-right: 8px;'></i>${readingTime} min read`;
    }
});
document.addEventListener('DOMContentLoaded', function () {
    const links = document.querySelectorAll('a[href^="#"]');
    for (const link of links) {
        link.addEventListener('click', function (event) {
            event.preventDefault();
            const targetId = this.getAttribute('href').substring(1);
            const targetElement = document.getElementById(targetId);
            if (targetElement) {
                targetElement.scrollIntoView({ behavior: 'smooth' });
            }
        });
    }
});
$(window).scroll(function () {
    if ($(this).scrollTop() > 250) {
        $('header').addClass('border-b');
    }
    else {
        $('header').removeClass("border-b");
    }
});
