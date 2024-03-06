// to get current year
function getYear() {
    var currentDate = new Date();
    var currentYear = currentDate.getFullYear();
    document.querySelector("#displayYear").innerHTML = currentYear;
}
getYear();

// nav menu 
function openNav() {
    document.getElementById("myNav").classList.toggle("menu_width")
    document.querySelector(".custom_menu-btn").classList.toggle("menu_btn-style")
}

//  Animation
const section1 = document.getElementById('1');
const section2 = document.getElementById('2');
const section3 = document.getElementById('3');
const section4 = document.getElementById('4');
const section5 = document.getElementById('5');
const section6 = document.getElementById('6');
const section7 = document.getElementById('7');
const section8 = document.getElementById('8');


const options = {
    rootMargin: '0px',
    threshold: 0.2,
}

function observeFunc(entries) {
    entries.forEach((entry) => {
        if (entry.isIntersecting) {
        const { target } = entry;
        console.log(entry)
            if (target.classList.contains('section')) {
                target.classList.add('fade-in')
            }
        }
    });
}

const observer = new IntersectionObserver(
    observeFunc,
    options
)

try {  
  observer.observe(section1);
  observer.observe(section2);
  observer.observe(section3);
  observer.observe(section4);
  observer.observe(section5);
  observer.observe(section6);
  observer.observe(section7);
  observer.observe(section8);
} catch (error) {
  
}



// // try {

// // quickSearch.onsubmit = () => {

// //     let campus = document.getElementById('campus').value
// //     let room_price_min = document.getElementById('room-price-min').value
// //     let room_price_max = document.getElementById('room-price-max').value
// //     let roomCapacity = document.getElementById('room-capacity').value
// //     let button = document.getElementById('quick-search-button')
    
// //     // if string is empty for campus means its not regitered
// //     if (campus == ""){
// //       button.innerHTML = "unavailable on this campus yet";
// //       return false;
// //     }
  
// // fetch(`/rooms/campus-rooms/${campus}?room_capacity=${roomCapacity}&room_price_min=${room_price_min}&room_price_max=${room_price_max}`, {
// //      method: "GET",
// //   }).then(function(response){
// //     console.log(response)
// //     button.innerHTML = "Searching...";
// //     // get url from the response object and redirect user to that
// //     window.location.href = response.url;
// //   })

// //   return false;
// // }

// // } catch (error) {
  
// // }

