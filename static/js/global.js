// Sidebar
const accountDetails = document.querySelector(".details_account");
const containerAccount = document.getElementById("container_account");
containerAccount.addEventListener("click", () => {
  if (accountDetails.style.visibility == "visible") {
    accountDetails.style.visibility = "hidden";
  } else {
    accountDetails.style.visibility = "visible";
  }
});

document.addEventListener("keydown", (event) => {
  if (event.key === "Escape") {
    accountDetails.style.visibility = "hidden";
  }
});
