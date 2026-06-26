document.addEventListener('DOMContentLoaded', function () {

    // ── Dark Mode ──────────────────────────────
    const toggle = document.getElementById('dark-mode-toggle');
    const body   = document.body;

    // Load saved preference
    if (localStorage.getItem('darkMode') === 'enabled') {
        body.classList.add('dark-mode');
        toggle.textContent = '☀️ Light';
    }

    // Toggle on click
    toggle.addEventListener('click', function () {
        body.classList.toggle('dark-mode');

        if (body.classList.contains('dark-mode')) {
            localStorage.setItem('darkMode', 'enabled');
            toggle.textContent = '☀️ Light';
        } else {
            localStorage.setItem('darkMode', 'disabled');
            toggle.textContent = '🌙 Dark';
        }
    });

    // ── Auto-hide flash messages ────────────────
    const messages = document.querySelectorAll('.messages li');
    messages.forEach(function (msg) {
        setTimeout(function () {
            msg.style.transition = 'opacity 0.5s';
            msg.style.opacity    = '0';
            setTimeout(() => msg.remove(), 500);
        }, 4000);
    });

});