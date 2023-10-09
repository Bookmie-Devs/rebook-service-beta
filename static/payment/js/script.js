// Variables

const payButton = document.getElementById('pay');
const Load = document.querySelector('.load');

// get the p-tag for the loader
const loadingOption = document.querySelector('#loading-option');





// Event Listener
payButton.addEventListener('click', () => {
    Load.style.display = "flex";

    // Simulate a delay (you can replace this with your actual form submission logic)
    setTimeout(function () {
    // Hide the loader after the delay
    Load.style.display = 'none';

    // After processing, you can redirect or show a success message as needed.
    }, 17000); // 17 seconds delay in this example
});


