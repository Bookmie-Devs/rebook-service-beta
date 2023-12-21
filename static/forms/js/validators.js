document.addEventListener("DOMContentLoaded", () => {
    const passwordInput = document.getElementById("password");
    const passwordMessage = document.getElementById("password-message");

    const phoneInput =document.getElementById('phone');

    const signupButton = document.getElementById("signup-button");
    
    const passwordConfirmDiv = document.getElementById("password-confirm-div");

    const emailInput = document.getElementById("email");
    const emailMessage = document.getElementById("email-message");
  
    const passwordDiv = document.getElementById("password-div");


    passwordMessage.style.display = "none"
    emailMessage.style.display ="none"


  // EMAIL VALIDATORS
  //list of allowed domains
  const allowedDomains = ['gmail.com', 'outlook.com', 'yahoo.com','apple.com', 'icloud.com'];

  emailInput.addEventListener("input", validateEmail);

  function validateEmail() {
    const email = emailInput.value.trim();
    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    if (emailPattern.test(email)) {
        checkDomain(email);
    } else {
        showEmailMessage("Invalid email format");}
    }

  function checkDomain(email) {
    const domain = email.split('@')[1];

    if (allowedDomains.includes(domain)) {
      hideEmailMessage();
    } else {
      showEmailMessage(`Invalid domain: ${domain}`);
    }
  }

  function showEmailMessage(message) {
    emailMessage.style.display = "block"; // Show the message
    emailMessage.innerHTML = `<ul class="list-group"><li class="list-group-item list-group-item-danger">${message}</li></ul>`
    passwordDiv.style.display = "none"
    passwordConfirmDiv.style.display = "none"
  }

  function hideEmailMessage() {
    emailMessage.textContent = "";
    emailMessage.style.display = "none"; // Hide the message

    passwordDiv.style.display = "block"
    passwordConfirmDiv.style.display = "block"
  }
  
    
  
  // PASSWORD VALIDATORS

  passwordInput.addEventListener("input", validatePassword);

  function validatePassword() {
      const password = passwordInput.value;
    //   Dont show any message if field is empty
      if (password=="") {
        hidePasswordMessage()
      }else{
        const passwordMessages = checkPasswordStrength(password);

        if (passwordMessages.length === 0) {
          hidePasswordMessage();
        } else {
          showPasswordMessage(passwordMessages);
        }}
      }

    function checkPasswordStrength(password) {
      const messages = [];
        
      if (password.length < 8) {
        messages.push("At least 8 characters");
      }

      if (!/[a-z]/.test(password)) {
        messages.push("At least one lowercase letter");
      }

      if (!/[A-Z]/.test(password)) {
        messages.push("At least one uppercase letter");
      }

       // Check for special characters
    if (!/[!@#$%^&*(),.?":{}|<>]/.test(password)) {
      messages.push("At least one special character");
    }

      if (!/\d/.test(password)) {
        messages.push("At least one digit");
      }

      return messages;
    }

    function showPasswordMessage(messages) {
      // Format messages with list items
      const formattedMessages = messages.map(msg => `<li class="list-group-item list-group-item-danger">${msg}</li>`).join('');

      passwordMessage.innerHTML = `<ul class="list-group">${formattedMessages}</ul>`;
      passwordMessage.style.display = "block"; // Show the message
      passwordConfirmDiv.style.display = "none" // hide cofirm password input until passwrd is strong
      // signupButton.style.display = "none";
    }

    function hidePasswordMessage() {
      passwordMessage.textContent = "";
      passwordMessage.style.display = "none"; // Hide the message
      passwordConfirmDiv.style.display = "block" //show confirm password input
    }

  // Phone Validators
    phoneInput.addEventListener("input", validatePhone);

    function validatePhone() {
      const phone = phoneInput.value.trim();
  
      if (phone.length==10) {
          document.getElementById('msgDiv2').style.display = "none"
      } else {
        document.getElementById('msgDiv2').style.display = "block"
        document.getElementById('msgDiv2').innerHTML = `<ul class="list-group"><li class="list-group-item list-group-item-danger">Phone must be 10 values</li></ul>`;
      }}

  });