let timerDuration = 5 * 60; // 5 minutes in seconds (5 * 60 seconds)
let timerInterval;
let timerElement = document.getElementById('xteope');

// Function to update the timer
function updateTimer() {
    let minutes = Math.floor(timerDuration / 60);
    let seconds = timerDuration % 60;
    timerElement.innerText = `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}s`;
    if (timerDuration > 0) {
        timerDuration--;
    } else {
        clearInterval(timerInterval);
    }
}

// Start or reset the timer
function startTimer() {
    clearInterval(timerInterval);
    timerDuration = 5 * 60; // Reset to 5 minutes
    updateTimer(); // Update immediately before starting the timer
    timerInterval = setInterval(updateTimer, 1000); // Update every second
}
// Start the timer when the page loads
startTimer();
