if (typeof waitUnit === 'undefined') {
    waitUnit = 1;
}

// Function to check if in an ad
function inAd() {
    const adElement = document.querySelector('span[data-a-target="video-ad-countdown"].CoreText-sc-1txzju1-0.ckwzla');
    return adElement !== null;
}

// Function to click the main settings button
function toggleMainSettings() {
    const mainSettingsButton = document.querySelector('button[data-a-target="player-settings-button"]');
    if (mainSettingsButton) {
        mainSettingsButton.click();
        return true;
    }
    return false;
}

// Function to open the settings menu
function openSettingsMenu() {
    setTimeout(() => {
        const settingsButton = document.querySelector('button[data-a-target="player-settings-menu-item-advanced"]');
        if (settingsButton) {
            settingsButton.click();
            toggleAdvancedVideoStats();
        } else {
            console.log('PRIVATE_STATLOGAdvanced settings button not found.');
        }
    }, waitUnit);
}

// Function to click the advanced stats toggle
function toggleAdvancedVideoStats() {
    setTimeout(() => {
        const toggleButton = document.querySelector('div[data-a-target="player-settings-submenu-advanced-video-stats"] input[type="checkbox"]');
        if (toggleButton) {
            toggleButton.click();
            getAllVideoStats();
        } else {
            console.log('PRIVATE_STATLOGAdvanced Video Stats toggle button not found.');
        }
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

        // Book
        const adElement = document.querySelector('span[data-a-target="video-ad-countdown"].CoreText-sc-1txzju1-0.ckwzla');
        inAd = adElement !== null;
        videoStats['inAd'] = inAd;

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
            // Now re-toggle the main settings button to close it
            setTimeout(() => {
                toggleMainSettings();
            }, waitUnit);
        } else {
            console.log('PRIVATE_STATLOGClose button for advanced stats not found.');
        }
    }, waitUnit * 4);
}


// Check if in an ad before proceeding
 if (toggleMainSettings()) { // Start the sequence by toggling the main settings
    openSettingsMenu();
} else {
    console.log('PRIVATE_STATLOGMain settings button not found.');
}