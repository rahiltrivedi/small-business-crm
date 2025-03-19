document.addEventListener("DOMContentLoaded", function () {
    const toggleButton = document.getElementById('darkModeToggle');
    const body = document.body;

    // Check if dark mode is enabled in localStorage
    if (localStorage.getItem('darkMode') === 'enabled') {
        body.classList.add('dark-mode');
    }

    toggleButton.addEventListener('click', function () {
        body.classList.toggle('dark-mode');
        // Save the dark mode state to localStorage
        if (body.classList.contains('dark-mode')) {
            localStorage.setItem('darkMode', 'enabled');
        } else {
            localStorage.setItem('darkMode', 'disabled');
        }
    });

    // Function to apply dark mode styles to all charts
function applyDarkModeToCharts() {
    const isDarkMode = document.body.classList.contains('dark-mode');

    Chart.defaults.color = isDarkMode ? "#fff" : "#333"; // Change text color
    Chart.defaults.borderColor = isDarkMode ? "rgba(255, 255, 255, 0.2)" : "rgba(0, 0, 0, 0.1)"; // Grid lines

    // Update all existing charts dynamically
    Chart.helpers.each(Chart.instances, function (instance) {
        instance.options.scales.x.ticks.color = isDarkMode ? "#fff" : "#333";
        instance.options.scales.y.ticks.color = isDarkMode ? "#fff" : "#333";
        instance.options.scales.x.grid.color = isDarkMode ? "rgba(255, 255, 255, 0.2)" : "rgba(0, 0, 0, 0.1)";
        instance.options.scales.y.grid.color = isDarkMode ? "rgba(255, 255, 255, 0.2)" : "rgba(0, 0, 0, 0.1)";
        instance.options.plugins.tooltip.backgroundColor = isDarkMode ? "rgba(0, 0, 0, 0.7)" : "rgba(255, 255, 255, 0.9)";
        instance.update(); // Apply changes
    });
}

// Call function when dark mode is toggled
document.addEventListener("DOMContentLoaded", function () {
    applyDarkModeToCharts(); // Apply dark mode settings on page load

    // Listen for dark mode toggle event (assuming you have a toggle button)
    document.querySelector("#dark-mode-toggle")?.addEventListener("click", function () {
        setTimeout(applyDarkModeToCharts, 300); // Delay to wait for class change
    });
});

});
