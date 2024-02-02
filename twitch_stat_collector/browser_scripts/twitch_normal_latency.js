if (typeof waitUnit === 'undefined') {
    waitUnit = 1;
}

// Function to toggle the main settings button
function toggleMainSettings() {
    const mainSettingsButton = document.querySelector('button[data-a-target="player-settings-button"]');
    if (mainSettingsButton) {
        mainSettingsButton.click();
        return true;
    }
    return false;
}

// Function to open the advanced settings menu
function openAdvancedSettingsMenu() {
    setTimeout(() => {
        const settingsButton = document.querySelector('button[data-a-target="player-settings-menu-item-advanced"]');
        if (settingsButton) {
            settingsButton.click();
            toggleNormalLatencyMode();
        } else {
            console.log('PRIVATE_ERRRLOGAdvanced settings button not found.');
        }
    }, waitUnit);
}

// Function to ensure low latency mode is off (normal latency)
function toggleNormalLatencyMode() {
    setTimeout(() => {
        const lowLatencyToggle = document.querySelector('input[type="checkbox"][data-a-target="tw-toggle"]');
        if (lowLatencyToggle && lowLatencyToggle.checked) {
            lowLatencyToggle.click();
            console.log('Low latency mode disabled. Normal latency mode enabled.');
        } else if (lowLatencyToggle) {
            console.log('Low latency mode is already off. Normal latency mode is active.');
        } else {
            console.log('Low latency mode toggle not found.');
        }

        closeAdvancedMenu();
    }, waitUnit * 2);
}

// Function to close the advanced menu and then the settings menu
function closeAdvancedMenu() {
    setTimeout(() => {
        const closeButton = document.querySelector('button[aria-label="Close video stats"]');
        if (closeButton) {
            closeButton.click();
            console.log('PRIVATE_STATLOGClosing advanced stats menu.');
            // Now re-toggle the main settings button to close it
            setTimeout(() => {
                console.log('PRIVATE_STATLOGClosing settings menu.');
                toggleMainSettings();
            }, waitUnit);
        } else {
            console.log('PRIVATE_STATLOGClose button for advanced stats not found.');
        }
    }, waitUnit * 4);
}

// Start the sequence
if (toggleMainSettings()) {
    openAdvancedSettingsMenu();
} else {
    console.log('PRIVATE_ERRRLOGMain settings button not found.');
}
