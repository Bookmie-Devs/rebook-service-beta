// Variables

const payButton = document.getElementById('pay');
const Load = document.querySelector('.load');

// get the p-tag for the loader
const loadingOption = document.querySelector('#loading-option');





// Event Listener
payButton.addEventListener('click', () => {
    Load.style.display = "flex";
});



