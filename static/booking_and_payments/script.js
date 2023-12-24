const direction = document.getElementById('direction');
const directionContainer = document.querySelector('.direction');
const closebtn = document.querySelector('.close');

// loader
const Load = document.querySelector('.load');

// direction.addEventListener('click', (e) => {
//     e.preventDefault();
//     directionContainer.style.display = 'block';
// })

function openNav() {
    document.getElementById("menu-btn").classList.toggle("menu_btn-style")
}


direction.onclick =() => {

    Load.style.display = "flex";

    setTimeout(function () {

    // Hide the loader after the delay
    Load.style.display = 'none';

    }, 3000);
}

// NOT USING DIV FOR MAP

// closebtn.addEventListener('click', () => {
//     directionContainer.style.display = 'none';
// })