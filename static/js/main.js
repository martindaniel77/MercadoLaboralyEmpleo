/* Interacciones del menú — navbar responsive y submenús */
(function () {
    'use strict';

    var toggle = document.getElementById('navToggle');
    var menu = document.getElementById('navMenu');

    if (toggle && menu) {
        toggle.addEventListener('click', function () {
            var open = toggle.getAttribute('aria-expanded') === 'true';
            toggle.setAttribute('aria-expanded', String(!open));
            menu.classList.toggle('is-open');
        });
    }

    // Submenús (dropdown) en dispositivos táctiles
    var items = document.querySelectorAll('.nav-item--dropdown > .nav-link--dropdown');

    Array.prototype.forEach.call(items, function (trigger) {
        trigger.addEventListener('click', function (e) {
            var item = trigger.parentElement;
            var dropdown = item.querySelector('.dropdown');
            var isMobile = window.getComputedStyle(menu).display === 'none';

            if (dropdown && isMobile) {
                e.preventDefault();
                dropdown.classList.toggle('is-open');
            }
        });
    });
})();
