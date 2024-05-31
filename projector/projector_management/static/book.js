document.addEventListener('DOMContentLoaded', function () {
    var menuToggle = document.querySelector('.menu-toggle');
    var dashboardNav = document.querySelector('.dashboard-nav');

    menuToggle.addEventListener('click', function () {
        dashboardNav.classList.toggle('open');
    });
});
