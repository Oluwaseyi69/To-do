document.addEventListener("DOMContentLoaded", function() {
    var alertElements = document.querySelectorAll('.alert');

    alertElements.forEach(function(alertElement) {
        setTimeout(function() {
            alertElement.style.display = 'none';
        }, 5000);
    });
});