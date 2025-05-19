// Detect system theme and apply corresponding class to body
document.addEventListener('DOMContentLoaded', function() {
    // Function to apply theme
    function applyTheme() {
        if (window.matchMedia('(prefers-color-scheme: dark)').matches) {
            document.body.classList.remove('light-mode');
            document.body.classList.add('dark-mode');
        } else {
            document.body.classList.remove('dark-mode');
            document.body.classList.add('light-mode');
        }
    }

    // Apply theme on page load
    applyTheme();

    // Listen for system theme changes
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', applyTheme);
});