function checkRebuffering() {
    // Selector for the rebuffering wheel element
    const selector = '.ScLoadingSpinner-sc-bvzaq8-0.bAQAxX.tw-loading-spinner';

    // Check if the element exists in the DOM
    const isRebuffering = document.querySelector(selector) !== null;

    if (isRebuffering) {
        console.log('The stream is currently rebuffering.');
    } else {
        console.log('The stream is running smoothly.');
    }
}

// Call the function
checkRebuffering();