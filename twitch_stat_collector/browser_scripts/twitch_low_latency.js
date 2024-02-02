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
            toggleLowLatencyMode();
        } else {
            console.log('PRIVATE_ERRRLOGAdvanced settings button not found.');
        }
    }, waitUnit);
}

// Function to toggle low latency mode
function toggleLowLatencyMode() {
    setTimeout(() => {
        const lowLatencyToggle = document.querySelector('input[type="checkbox"][data-a-target="tw-toggle"]');
        const advancedToggle = document.querySelector('div[data-a-target="player-settings-submenu-advanced-video-stats"] input[type="checkbox"]');
        if (lowLatencyToggle && !lowLatencyToggle.checked) {
            lowLatencyToggle.click();
            console.log('Low latency mode enabled.');
        } else if (lowLatencyToggle) {
            console.log('Low latency mode is already on.');
        } else {
            console.log('Low latency mode toggle not found.');
        }

        if (advancedToggle) {
            advancedToggle.click();
            getAllVideoStats();
        } else {
            console.log('PRIVATE_STATLOGAdvanced Video Stats toggle button not found.');
        }

        closeAdvancedMenu();
    }, waitUnit * 2);
}


// Function to get all values from the video stats table
function getAllVideoStats() {
    setTimeout(() => {

        const statsRows = document.querySelectorAll('tr[data-a-target="player-overlay-video-stats-row"]');
        let videoStats = {};
        
        // add an intial row for time stamp on videoStats
        videoStats['timeStamp'] = Date.now();

        statsRows.forEach(row => {
            const nameElement = row.querySelector('td:first-child p');
            const valueElement = row.querySelector('td:last-child p');
            if (nameElement && valueElement) {
                const name = nameElement.textContent.trim();
                const value = valueElement.textContent.trim();
                videoStats[name] = value;
            }
        });

        // Selector for the rebuffering wheel element
        const selector = '.ScLoadingSpinner-sc-bvzaq8-0.bAQAxX.tw-loading-spinner';

        // Check if the element exists in the DOM
        const isRebuffering = document.querySelector(selector) !== null;

        // add a row for isRebuffering
        videoStats['isRebuffering'] = isRebuffering;

        console.log('PRIVATE_DATALOG' + JSON.stringify(videoStats));

        // Close the advanced stats and then the settings menu
        closeAdvancedMenu();


        return videoStats;

    }, waitUnit * 3);
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