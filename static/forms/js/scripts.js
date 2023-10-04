
// get sign-up button
const signUpButton = document.getElementById("signup-button");


// get login button
const loginButton = document.getElementById("login-button")


// loader
const Load = document.querySelector('.load');


document.addEventListener('submit', () => {
    Load.style.display = "flex";

    // Simulate a delay (you can replace this with your actual form submission logic)
    setTimeout(function () {
    // Hide the loader after the delay
    Load.style.display = 'none';

    // Now you can proceed with your form submission logic
    // For example, you can submit the form data using AJAX or perform any other action.
    
    // After processing, you can redirect or show a success message as needed.
    }, 7000); // 7 seconds delay in this example
})

