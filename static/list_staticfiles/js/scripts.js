/*!
* Start Bootstrap - Shop Homepage v5.0.6 (https://startbootstrap.com/template/shop-homepage)
* Copyright 2013-2023 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-shop-homepage/blob/master/LICENSE)
*/

const load  = document.querySelector('.load' );
const loadingOption = document.getElementById('loading-option');


// upon submit
document.addEventListener('submit', () => {
    load.style.display = "flex";

    // change p-tag of loader in campus hostel page during submission
    loadingOption.innerHTML = "Searching..."

    // Simulate a delay (you can replace this with your actual form submission logic)
    setTimeout(function () {
    // Hide the loader after the delay
    load.style.display = 'none';
    
    }, 7000); // 7 seconds delay 
})





