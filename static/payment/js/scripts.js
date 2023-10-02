
// scripts for paymnt

window.addEventListener('load', () => {
    // Page has finished loading, hide the loader
    const loaderWrapper = document.querySelector('.loader-wrapper');
    loaderWrapper.style.display = 'none';
});

// Simulate server-side process (remove this in your actual implementation)
setTimeout(() => {

    // Simulate the completion of a server-side process
    const loaderWrapper = document.querySelector('.loader-wrapper');
    loaderWrapper.style.display = 'none';
}, 505050); // Replace with the actual duration of your server-side process
