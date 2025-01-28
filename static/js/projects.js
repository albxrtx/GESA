const form = document.querySelector(".add_new_project_form");
const btnAdd = document.getElementById("btn_add_new_project");
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
const deleteBtn = document.getElementById("btn_delete");
deleteBtn.addEventListener("click", (event) => {
  if (!confirm("¿Estás seguro de que deseas eliminar este elemento?")) {
    event.preventDefault();
  }
});
function showDeleteForm(button) {
  const form = button.closest("details").querySelector(".delete_form");

  if (form.style.visibility === "hidden" || form.style.visibility === "") {
    form.style.visibility = "visible";
  } else {
    form.style.visibility = "hidden";
  }
}
