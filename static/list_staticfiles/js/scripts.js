/*!
* Start Bootstrap - Shop Homepage v5.0.6 (https://startbootstrap.com/template/shop-homepage)
* Copyright 2013-2023 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-shop-homepage/blob/master/LICENSE)
*/
// This file is intentionally blank
// Use this file to add JavaScript to your project

const bookingButton = document.getElementById("booking-button");
const Load  =document.querySelector('.load' );
const searchButton = document.getElementById('search-button')


// upon submit
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


document.addEventListener("DOMContentLoaded", function () {
      Load.style.display = "flex";
    
    // Hide the loader when all page assets (including images, scripts, etc.) are loaded
    window.addEventListener("load", function () {
        Load.style.display = "none";
    });
});



function loading(){
    return Load.style.display = "flex";   
}