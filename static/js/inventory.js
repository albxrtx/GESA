const form = document.querySelector(".add_new_product_form");
const btnAddNewProduct = document.getElementById("btn_add_new_product");
const btnCancel = document.getElementById("btn_cancel");
const btnAdd = document.getElementById("btn_add");

const inputId = document.getElementById("input_id");

btnAddNewProduct.addEventListener("click", () => {
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

btnAdd.addEventListener("click", () => {
  showToast();
});

function showToast() {
  const toast = document.getElementById("toast");

  toast.classList.add("show");

  setTimeout(() => {
    toast.classList.remove("show");
  }, 6000);
}

document.querySelectorAll(".btn-delete").forEach((button) => {
  button.addEventListener("click", (event) => {
    if (!confirm("¿Estás seguro de que deseas eliminar este elemento?")) {
      event.preventDefault();
    }
  });
});
