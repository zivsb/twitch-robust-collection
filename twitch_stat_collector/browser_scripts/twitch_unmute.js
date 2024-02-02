function checkAndUnmuteStream() {
    // Select the mute/unmute button based on its class
    var muteButton = document.querySelector('button[data-a-target="player-mute-unmute-button"]');

    // Check if the button is found
    if (!muteButton) {
        console.log("PRIVATE_STATLOGMute button not found.");
    }

    // Determine the mute status based on the aria-label attribute
    var isMuted = muteButton.getAttribute('aria-label') === "Unmute (m)";

    // Log the status and click the button to unmute if muted
    if (isMuted) {
        console.log("PRIVATE_STATLOGThe stream is muted. Unmuting now.");
        muteButton.click();
    } else {
        console.log("PRIVATE_STATLOGThe stream is unmuted.");
    }
}

// Call the function to check the mute status and unmute if necessary
checkAndUnmuteStream();
