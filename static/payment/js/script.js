// Variables

const Pay = document.getElementById('pay');
const Load  =document.querySelector('.load');

// Event Listener

Pay.addEventListener('click', function(){
    Load.style.display = "flex";
});

// Pay.onclick = () => {
//     Load.style.display = "flex";
// }