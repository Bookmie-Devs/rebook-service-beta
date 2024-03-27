const load  = document.querySelector('.load' );
const loadingOption = document.getElementById('loading-option');


document.querySelectorAll('.booking-form').forEach((form) => {
    form.onsubmit = () => {
        
        load.style.display = "flex";

        loadingOption.innerHTML = 'Booking . . .';    
        setTimeout(function () {
        load.style.display = 'none';
        
        }, 2000);
    }
})

function openNav() {
    document.getElementById("menu-btn").classList.toggle("menu_btn-style")
}

window.addEventListener("scroll", bodyScroll)

let scrollTimer = -1;

function bodyScroll() {
    document.querySelector(".map-link").classList.add('hide')
    
    if (scrollTimer != -1)
    clearTimeout(scrollTimer);

scrollTimer = window.setTimeout(scrollFinished, 200);
}

function scrollFinished() {
    document.querySelector(".map-link").classList.remove('hide')
}