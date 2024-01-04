
// form
const loginForm = document.querySelector('#login-form');
// loader
const Load = document.querySelector('.load');


// for changing sections of the signup page
try {
  
  function showSection2(sectionNumber) {
    // Hide all sections
    document.querySelectorAll('.section').forEach((section) => {
      section.style.display = 'none';
    });
    // Show the selected section on a condition
    let msgDiv = document.getElementById('msgDiv');
    let section1a = document.querySelector('.section1a').value;
    let section1b = document.querySelector('.section1b').value;
    let sectionInputs = [section1a, section1b];
    let emptyInput = sectionInputs.some( input => input === '');
    
    if(emptyInput){
      document.getElementById('section1').style.display = 'block';
      msgDiv.innerHTML = `<ul class="list-group"><li class="list-group-item list-group-item-danger">Inputs are required</li></ul>`
       setTimeout(function () {
         msgDiv.innerHTML = ''
      }, 4000);
    } else{
    document.getElementById(`section${sectionNumber}`).style.display = 'block';
    }
  }

} catch (error) {
  
}
try {
  
  function showSection3(sectionNumber) {
    // Hide all sections
    document.querySelectorAll('.section').forEach((section) => {
      section.style.display = 'none';
    });
    // Show the selected section on a condition
    let msgDiv2 = document.getElementById('msgDiv2');
    let section2a = document.querySelector('.section2a').value;
    let section2b = document.querySelector('.section2b').value;
    let section2c = document.querySelector('.section2c').value;
    let sectionInputs = [section2a, section2b, section2c];
    let emptyInput = sectionInputs.some( input => input.trim() === '');
    
    if(emptyInput){
      document.getElementById('section2').style.display = 'block';
      msgDiv2.innerHTML = `<ul class="list-group"><li class="list-group-item list-group-item-danger">Inputs are required</li></ul>`;
      
    } else{
    document.getElementById(`section${sectionNumber}`).style.display = 'block';
    }
  }

} catch (error) {
  
}

try {
  
  function back(sectionNumber) {
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

// Password toogle
try {
  const passwordInput = document.getElementById('password');
    const togglePasswordButton = document.getElementById('togglePassword');

    togglePasswordButton.addEventListener('click', function () {
        const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
        passwordInput.setAttribute('type', type);

        // Change the eye icon based on the password visibility
        togglePasswordButton.innerHTML = type === 'password' ?
            `<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="gray" class="bi bi-eye" viewBox="0 0 16 16">
  <path d="M16 8s-3-5.5-8-5.5S0 8 0 8s3 5.5 8 5.5S16 8 16 8M1.173 8a13.133 13.133 0 0 1 1.66-2.043C4.12 4.668 5.88 3.5 8 3.5c2.12 0 3.879 1.168 5.168 2.457A13.133 13.133 0 0 1 14.828 8c-.058.087-.122.183-.195.288-.335.48-.83 1.12-1.465 1.755C11.879 11.332 10.119 12.5 8 12.5c-2.12 0-3.879-1.168-5.168-2.457A13.134 13.134 0 0 1 1.172 8z"/>
  <path d="M8 5.5a2.5 2.5 0 1 0 0 5 2.5 2.5 0 0 0 0-5M4.5 8a3.5 3.5 0 1 1 7 0 3.5 3.5 0 0 1-7 0"/>
</svg>` :
            `<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="gray" class="bi bi-eye-slash" viewBox="0 0 16 16">
  <path d="M13.359 11.238C15.06 9.72 16 8 16 8s-3-5.5-8-5.5a7.028 7.028 0 0 0-2.79.588l.77.771A5.944 5.944 0 0 1 8 3.5c2.12 0 3.879 1.168 5.168 2.457A13.134 13.134 0 0 1 14.828 8c-.058.087-.122.183-.195.288-.335.48-.83 1.12-1.465 1.755-.165.165-.337.328-.517.486z"/>
  <path d="M11.297 9.176a3.5 3.5 0 0 0-4.474-4.474l.823.823a2.5 2.5 0 0 1 2.829 2.829zm-2.943 1.299.822.822a3.5 3.5 0 0 1-4.474-4.474l.823.823a2.5 2.5 0 0 0 2.829 2.829"/>
  <path d="M3.35 5.47c-.18.16-.353.322-.518.487A13.134 13.134 0 0 0 1.172 8l.195.288c.335.48.83 1.12 1.465 1.755C4.121 11.332 5.881 12.5 8 12.5c.716 0 1.39-.133 2.02-.36l.77.772A7.029 7.029 0 0 1 8 13.5C3 13.5 0 8 0 8s.939-1.721 2.641-3.238l.708.709zm10.296 8.884-12-12 .708-.708 12 12-.708.708"/>
</svg>`;
    });
} catch (error) {
  
}
try {
  const passwordInput2 = document.getElementById('confirm-password');
    const togglePasswordButton2 = document.getElementById('togglePassword2');

    togglePasswordButton2.addEventListener('click', function () {
        const type2 = passwordInput2.getAttribute('type') === 'password' ? 'text' : 'password';
        passwordInput2.setAttribute('type', type2);

        // Change the eye icon based on the password visibility
        togglePasswordButton2.innerHTML = type2 === 'password' ?
            `<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="gray" class="bi bi-eye" viewBox="0 0 16 16">
  <path d="M16 8s-3-5.5-8-5.5S0 8 0 8s3 5.5 8 5.5S16 8 16 8M1.173 8a13.133 13.133 0 0 1 1.66-2.043C4.12 4.668 5.88 3.5 8 3.5c2.12 0 3.879 1.168 5.168 2.457A13.133 13.133 0 0 1 14.828 8c-.058.087-.122.183-.195.288-.335.48-.83 1.12-1.465 1.755C11.879 11.332 10.119 12.5 8 12.5c-2.12 0-3.879-1.168-5.168-2.457A13.134 13.134 0 0 1 1.172 8z"/>
  <path d="M8 5.5a2.5 2.5 0 1 0 0 5 2.5 2.5 0 0 0 0-5M4.5 8a3.5 3.5 0 1 1 7 0 3.5 3.5 0 0 1-7 0"/>
</svg>` :
            `<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="gray" class="bi bi-eye-slash" viewBox="0 0 16 16">
  <path d="M13.359 11.238C15.06 9.72 16 8 16 8s-3-5.5-8-5.5a7.028 7.028 0 0 0-2.79.588l.77.771A5.944 5.944 0 0 1 8 3.5c2.12 0 3.879 1.168 5.168 2.457A13.134 13.134 0 0 1 14.828 8c-.058.087-.122.183-.195.288-.335.48-.83 1.12-1.465 1.755-.165.165-.337.328-.517.486z"/>
  <path d="M11.297 9.176a3.5 3.5 0 0 0-4.474-4.474l.823.823a2.5 2.5 0 0 1 2.829 2.829zm-2.943 1.299.822.822a3.5 3.5 0 0 1-4.474-4.474l.823.823a2.5 2.5 0 0 0 2.829 2.829"/>
  <path d="M3.35 5.47c-.18.16-.353.322-.518.487A13.134 13.134 0 0 0 1.172 8l.195.288c.335.48.83 1.12 1.465 1.755C4.121 11.332 5.881 12.5 8 12.5c.716 0 1.39-.133 2.02-.36l.77.772A7.029 7.029 0 0 1 8 13.5C3 13.5 0 8 0 8s.939-1.721 2.641-3.238l.708.709zm10.296 8.884-12-12 .708-.708 12 12-.708.708"/>
</svg>`;
    });
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

