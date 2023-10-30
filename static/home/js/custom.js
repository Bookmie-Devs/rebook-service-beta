// contact
const contactForm = document.getElementById('contact-form')
const contactButton = document.getElementById('contact-button')
// feedback
const feedbackForm = document.getElementById('feedback-form')
const feedbackButton = document.getElementById('feedback-button')

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
