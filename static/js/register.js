const passwordInput = document.getElementById("password_input");
const confirmPasswordInput = document.getElementById("confirm_password_input");
const buttonSubmit = document.getElementById("button_submit");
const svgs = document.querySelectorAll("svg");

svgs.forEach((svg) => {
  svg.addEventListener("click", () => {
    if (passwordInput.type === "password") {
      passwordInput.type = "text";
      confirmPasswordInput.type = "text";
    } else {
      passwordInput.type = "password";
      confirmPasswordInput.type = "password";
    }
  });
});



passwordInput.addEventListener("input", () => {
  let check = document.querySelector(".check_password")
  
  if (passwordInput.value === confirmPasswordInput.value) {
    confirmPasswordInput.style.border = "1px solid gray";
    passwordInput.style.border = "1px solid gray";
    buttonSubmit.disabled = false;
  } else {
    confirmPasswordInput.style.border = "1px solid red";
    passwordInput.style.border = "1px solid red";
    buttonSubmit.disabled = true;
  }
  
  if ( passwordInput.value.length < 8) {
    check.textContent ="Carácteres mínimos: 8"
    check.style.display = "flex"
  }else{
    check.style.display = "none"
  }
});

confirmPasswordInput.addEventListener("input", (e) => {
  e.preventDefault()
  if (passwordInput.value === confirmPasswordInput.value) {
    confirmPasswordInput.style.border = "1px solid gray";
    passwordInput.style.border = "1px solid gray";
    buttonSubmit.disabled = false;
  } else {
    confirmPasswordInput.style.border = "1px solid red";
    passwordInput.style.border = "1px solid red";
    buttonSubmit.disabled = true;
  }
  
});


  