const direction = document.getElementById('direction');
const directionContainer = document.querySelector('.direction');
const closebtn = document.querySelector('.x');

direction.addEventListener('click', (e) => {
    e.preventDefault();
    directionContainer.style.display = 'block';
})

closebtn.addEventListener('click', () => {
    directionContainer.style.display = 'none';
})