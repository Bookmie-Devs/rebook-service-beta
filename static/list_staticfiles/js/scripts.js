/*!
* Start Bootstrap - Shop Homepage v5.0.6 (https://startbootstrap.com/template/shop-homepage)
* Copyright 2013-2023 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-shop-homepage/blob/master/LICENSE)
*/
// This file is intentionally blank
// Use this file to add JavaScript to your project

let bookingButton = document.getElementById("booking-button")

// document.addEventListener('click', () => {
//     bookingButton.innerHTML="HDHD"

//     console.log("{{ room.room_price }}")
// })

bookingButton.onclick = () => {
    
    bookingButton.innerText = "Payment";
}