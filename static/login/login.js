(() => {
  const loginButton = document.getElementById('loginButton');
  const signinButton = document.getElementById('signinButton'); //added to make sure the slider buttons do not get an outline momentarially 
  const passwordToggleIconLogin = document.getElementsByClassName("passwordToggleIcon")[0];
  const passwordToggleIconSignin = document.getElementsByClassName("passwordToggleIcon")[1];

  [loginButton, signinButton].forEach(button => {
    button.addEventListener('mousedown', (e) => {
      e.preventDefault();
    }); button.addEventListener('click', () => {
      button.blur(); //to remove focus from the button and remove the outline
    });
  });
  loginButton.addEventListener("click", showLogin);
  signinButton.addEventListener("click", showSignup);
  passwordToggleIconLogin.addEventListener("click", togglePassword);
  passwordToggleIconSignin.addEventListener("click", togglePassword);

  //function to toggle the visibility of the password and to toggle the eye icon
  function togglePassword() {
    var password = document.getElementById("password_input");
    var new_password = document.getElementById("new_password");
    var toggleIcons = document.getElementsByClassName("passwordToggleIcon");
    
    var activePasswordInput = password.offsetParent !== null ? password : new_password;
    var activeToggleIcon = activePasswordInput === password ? toggleIcons[0] : toggleIcons[1];
    
    if(activePasswordInput.type === "password") {
      activePasswordInput.type = "text";
      activeToggleIcon.src = "/static/login/images/eye_open.svg";
      activeToggleIcon.classList.add('password-closed');
    } else {
      activePasswordInput.type = "password";
      activeToggleIcon.src = "/static/login/images/eye_closed.svg";
      activeToggleIcon.classList.remove('password-closed');
    }
  }

  function showLogin() {
    const loginButton = document.getElementById('loginButton');
    const signinButton = document.getElementById('signinButton');

    document.getElementById('ImLoggingIn').style.display = 'flex';
    document.getElementById('ImCreatingAnAccount').style.display = 'none';

    loginButton.className = 'sliderButtonActive';
    signinButton.className = 'sliderButtonInactive';
  }

  function showSignup() {
    document.getElementById('ImLoggingIn').style.display = 'none';
    document.getElementById('ImCreatingAnAccount').style.display = 'flex';

    const loginButton = document.getElementById('loginButton');
    const signinButton = document.getElementById('signinButton');

    loginButton.className = 'sliderButtonInactive';
    signinButton.className = 'sliderButtonActive';
  }
})();