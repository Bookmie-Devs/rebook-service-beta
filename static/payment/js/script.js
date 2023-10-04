// Variables

const Pay = document.getElementById('pay');
const Load = document.querySelector('.load');


// Event Listener
Pay.addEventListener('click', () => {
    Load.style.display = "flex";

    // Simulate a delay (you can replace this with your actual form submission logic)
    setTimeout(function () {
    // Hide the loader after the delay
    Load.style.display = 'none';

    // Now you can proceed with your form submission logic
    // For example, you can submit the form data using AJAX or perform any other action.
    
    // After processing, you can redirect or show a success message as needed.
    }, 5000); // 5 seconds delay in this example
});

// Pay.onclick = () => {
//     Load.style.display = "flex";
// }

