document.addEventListener("DOMContentLoaded", function() {
    // Toggle sidebar
    document.querySelector(".menu-toggle").addEventListener("click", function() {
        document.querySelector(".dashboard-nav").classList.toggle("active");
    });

    // Notification panel
    document.querySelector(".notification-icon").addEventListener("mouseover", function() {
        document.querySelector(".notification-panel").style.display = "block";
    });

    document.querySelector(".notification-icon").addEventListener("mouseout", function() {
        document.querySelector(".notification-panel").style.display = "none";
    });
});
