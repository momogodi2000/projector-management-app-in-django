// Custom JavaScript for the manage users page

// Example: Confirm delete action
document.querySelectorAll('.btn-danger').forEach(function(button) {
    button.addEventListener('click', function(event) {
        if (!confirm('Are you sure you want to delete this user?')) {
            event.preventDefault();
        }
    });
});
