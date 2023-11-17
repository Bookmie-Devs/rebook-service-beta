
// form
const loginForm = document.querySelector('#login-form');
// loader
const Load = document.querySelector('.load');


// for changing sections of the signup page
try {
  
  function showSection(sectionNumber) {
    // Hide all sections
    document.querySelectorAll('.section').forEach((section) => {
      section.style.display = 'none';
    });
    // Show the selected section
    document.getElementById(`section${sectionNumber}`).style.display = 'block';
  }

} catch (error) {
  
}


// loader trigger for login form
try {
  
  loginForm.onsubmit =()=>{
      Load.style.display = "flex";
      setTimeout(function () {
      // Hide the loader after the delay
      Load.style.display = 'none';
      }, 6000);
  }
} catch (error) {
  
}








// check is passwor is strong
// function checkPasswordStrength(password) {
//     const errors = [];
  
//     if (password.length < 7) {
//       errors.push("Password must be at least 8 characters long.");
//     }
  
//     if (!/[A-Z]/.test(password)) {
//       errors.push("Password must contain at least one uppercase letter.");
//     }
  
//     if (!/[a-z]/.test(password)) {
//       errors.push("Password must contain at least one lowercase letter.");
//     }
  
//     if (!/\d/.test(password)) {
//       errors.push("Password must contain at least one digit.");
//     }
  
//     // if (!/[^A-Za-z0-9]/.test(password)) {
//     //   errors.push("Password must contain at least one special character.");
//     // }
//     return errors;
//   }



// try {
  
//   form.forEach(function(form) {

//     form.onsubmit = function(){
    
//         if (form.dataset.formtype === "login-form"){

//             Load.style.display = "flex";
//             setTimeout(function () {
//             // Hide the loader after the delay
//             Load.style.display = 'none';
//             }, 6000);
//         }

//         let heading = document.querySelector('#heading')
//         let input = document.querySelector('input')
//         let campus = document.querySelector('#campus').value
//         let password1 = document.getElementById('password').value
//         let confirmPassword = document.getElementById('confirm-password').value
//         let signupButton = document.getElementById('signup-button')
    
//         Load.style.display = "flex";
    
//         setTimeout(function () {

//         // Hide the loader after the delay
//         Load.style.display = 'none';
    
//         }, 6000);
        

//         document.onkeydown = () => {

//         signupButton.innerHTML = "Proceed";
//         }

//         if (password1 !== confirmPassword) {
            
//           Load.style.display = 'none';

//           heading.innerHTML = "Password not matching"
//           signupButton.innerHTML="Password not matching";
//           return false;
//         }
//           if (campus == ""){
//           Load.style.display = 'none';
//           heading.innerHTML = "Unavailable on this campus yet"
//           signupButton.innerHTML="Unavailable on this campus yet";

//           return false;
//         }
            
//         let errors = checkPasswordStrength(password1)

//         if (errors.length !== 0){

//             Load.style.display = 'none';
          
//             for (const error of errors) {
//               signupButton.innerHTML= error;
//             }
            
//             return false;}
                  
//           }})

// } catch (error) {
  
// }

    
// loader for reset password form
try {
  
  document.getElementById('reset-password').onsubmit = function(){

    Load.style.display = "flex";
    
    setTimeout(function () {

    // Hide the loader after the delay
    Load.style.display = 'none';

    }, 5000);

  }

} catch (error) {
  
}