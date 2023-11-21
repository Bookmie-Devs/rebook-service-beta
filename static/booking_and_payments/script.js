const direction = document.getElementById('direction');
const directionContainer = document.querySelector('.direction');
const closebtn = document.querySelector('.close');

// loader
const Load = document.querySelector('.load');

// direction.addEventListener('click', (e) => {
//     e.preventDefault();
//     directionContainer.style.display = 'block';
// })


direction.onclick =() => {

    Load.style.display = "flex";

    setTimeout(function () {

    // Hide the loader after the delay
    Load.style.display = 'none';

    }, 6000);
}

closebtn.addEventListener('click', () => {
    directionContainer.style.display = 'none';
})