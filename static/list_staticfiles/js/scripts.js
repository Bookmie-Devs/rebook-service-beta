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
})



function loading(){
    return Load.style.display = "flex";   
}