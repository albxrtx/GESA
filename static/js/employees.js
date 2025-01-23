const form = document.querySelector(".add_new_employer_form");
const btnAdd = document.getElementById("btn_add_new_employer");
const btnCancel = document.getElementById("btn_cancel");

btnAdd.addEventListener("click", () => {
  form.style.visibility = "visible";
});
btnCancel.addEventListener("click", () => {
  form.style.visibility = "hidden";
});
document.addEventListener("keydown", (event) => {
  if (event.key === "Escape") {
    form.style.visibility = "hidden";
  }
});
document.querySelectorAll(".btn-delete").forEach((button) => {
  button.addEventListener("click", (event) => {
    if (!confirm("¿Estás seguro de que deseas eliminar este elemento?")) {
      event.preventDefault();
    }
  });
});
