// contact
const contactForm = document.getElementById('contact-form')
const contactButton = document.getElementById('contact-button')
// feedback
const feedbackForm = document.getElementById('feedback-form')
const feedbackButton = document.getElementById('feedback-button')

// quickSearch
const quickSearch = document.getElementById('quick-search')

// newsLetter
const newsLetter = document.getElementById('news-letter')

// subcribeButton
let subscribeButton = document.getElementById('subscribe-button')


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

/*USE TRY AND CATCH BLOCKS TO PREVENT
THE OTHER ONSUBMIT EVENT LISTERNERS FROM CRASHING */


// catch error is element is not found
try {
  // FEEDBACK/ISSUES FORM
feedbackForm.onsubmit = () => {
  
  let username = document.getElementById('username').value
  let useremail = document.getElementById('useremail').value
  let userphone = document.getElementById('userphone').value
  let message = document.getElementById('message').value
  
  feedbackButton.innerHTML = "Sending..."

  fetch("/reviews/feedback-and-issues/", {
   method: "POST",
   body: JSON.stringify({
  "name": username,
  "email": useremail,
  "phone": userphone,
  "message":message,
}),
  headers: {
    "Content-type": "application/json; charset=UTF-8"
  }
})
.then((response) => response.json())
  .then((json) =>feedbackButton.innerHTML=json.message);

  document.getElementById('username').value = ''
  document.getElementById('useremail').value = ''
  document.getElementById('userphone').value = ''
  document.getElementById('message').value = ''

  return false
}
} catch (error) {
  
}


// CUSTOMER CARE FORM(CONTACT US)
try {

contactForm.onsubmit = () => {
  let username = document.getElementById('username').value
  let useremail = document.getElementById('useremail').value
  let userphone = document.getElementById('userphone').value
  let message = document.getElementById('message').value

  contactButton.innerHTML = "Sending..."

  fetch("/reviews/customer-care/", {
   method: "POST",
   body: JSON.stringify({
  "name": username,
  "email": useremail,
  "phone": userphone,
  "message":message,
}),
  headers: {
    "Content-type": "application/json; charset=UTF-8"
  }
})
.then((response) => response.json())
    .then((json) => contactButton.innerHTML = json.message);

  document.getElementById('username').value = ''
  document.getElementById('useremail').value = ''
  document.getElementById('userphone').value = ''
  document.getElementById('message').value = ''

  return false}
} catch (error) {
  
}


try {

quickSearch.onsubmit = () => {

    let campus = document.getElementById('campus').value
    let room_price_min = document.getElementById('room-price-min').value
    let room_price_max = document.getElementById('room-price-max').value
    let roomCapacity = document.getElementById('room-capacity').value
    let button = document.getElementById('quick-search-button')
    
    // if string is empty for campus means its not regitered
    if (campus == ""){
      button.innerHTML = "unavailable on this campus yet";
      return false;
    }
  
fetch(`/rooms/campus-rooms/${campus}?room_capacity=${roomCapacity}&room_price_min=${room_price_min}&room_price_max=${room_price_max}`, {
     method: "GET",
  }).then(function(response){
    console.log(response)
    button.innerHTML = "Searching...";
    // get url from the response object and redirect user to that
    window.location.href = response.url;
  })

  return false;
}

} catch (error) {
  
}

try {
  
newsLetter.onsubmit = () =>{

  let newsEmail = document.getElementById('news-email').value

  subscribeButton.innerHTML = "Sending..."

  fetch("/news-letter/", {
   method: "POST",
   body: JSON.stringify({
  "email": newsEmail,
}),
  headers: {
    "Content-type": "application/json; charset=UTF-8"
  }
})
.then((response) => response.json())
    .then((json) => subscribeButton.innerHTML = json.message);

  document.getElementById('news-email').value = ''


  return false
}
} catch (error) {
  
}