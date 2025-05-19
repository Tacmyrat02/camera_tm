function displayAshgabatTime() {
    const ashgabatTimeElement = document.getElementById("ashgabat-datetime");

    function updateTime() {
        // Create a Date object for current time
        const now = new Date();

        // Define Ashgabat time zone (GMT+5)
        const ashgabatOffset = 5 * 60; // in minutes
        const localOffset = now.getTimezoneOffset();
        const ashgabatTime = new Date(now.getTime() + (ashgabatOffset + localOffset) * 60 * 1000);

        // Format the date and time as "Day - Mon DD, YYYY HH:MM:SS"
        const days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
        const months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];

        const dayName = days[ashgabatTime.getDay()];
        const monthName = months[ashgabatTime.getMonth()];
        const day = ashgabatTime.getDate();
        const year = ashgabatTime.getFullYear();
        const hours = ashgabatTime.getHours();
        const minutes = ashgabatTime.getMinutes();
        const seconds = ashgabatTime.getSeconds();

        // Add leading zeros to minutes and seconds if needed
        const formattedMinutes = minutes < 10 ? "0" + minutes : minutes;
        const formattedSeconds = seconds < 10 ? "0" + seconds : seconds;

        const formattedDateTimeString = `${dayName} - ${monthName} ${day}, ${year} ${hours}:${formattedMinutes}:${formattedSeconds}`;
        ashgabatTimeElement.textContent = formattedDateTimeString;
    }
    updateTime();
    setInterval(updateTime, 1000); // Update every second
}

// Call the function when the page loads
document.addEventListener("DOMContentLoaded", displayAshgabatTime);