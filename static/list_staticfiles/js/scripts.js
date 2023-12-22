/*!
* Start Bootstrap - Shop Homepage v5.0.6 (https://startbootstrap.com/template/shop-homepage)
* Copyright 2013-2023 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-shop-homepage/blob/master/LICENSE)
*/
const load  = document.querySelector('.load' );
const loadingOption = document.getElementById('loading-option');


document.querySelectorAll('.booking-form').forEach((form) => {
    form.onsubmit = () => {
        
        load.style.display = "flex";
        // change p-tag of loader in campus hostel page during submission

        loadingOption.innerHTML = 'Booking . . .';    
        // Simulate a delay (you can replace this with your actual form submission logic)
        setTimeout(function () {
        // Hide the loader after the delay
        load.style.display = 'none';
        
        }, 2000); // 2 seconds delay 
    }
})





