document.addEventListener("DOMContentLoaded", () => {
  const accountDetails = document.querySelector(".details_account");
  const containerAccount = document.getElementById("container_account");

  if (containerAccount && accountDetails) {
    containerAccount.addEventListener("click", () => {
      accountDetails.style.visibility =
        accountDetails.style.visibility === "visible" ? "hidden" : "visible";
    });

    document.addEventListener("keydown", (event) => {
      if (event.key === "Escape") {
        accountDetails.style.visibility = "hidden";
      }
    });
  }

  const btnAdd = document.getElementById("btn_add_header");
  const btnCancel = document.getElementById("btn_cancel");
  const form = document.querySelector(".container_form");

  if (btnAdd && btnCancel && form) {
    btnAdd.addEventListener("click", () => {
      console.log("Botón 'Añadir venta' presionado");
      form.style.visibility = "visible";
    });

    btnCancel.addEventListener("click", () => {
      form.style.visibility = "hidden";
    });
  } else {
    console.error("Uno o más elementos no existen en el DOM.");
  }

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
});

function showDeleteForm(button) {
  const form = button.closest("div").querySelector(".delete_form");

  if (form.style.visibility === "hidden" || form.style.visibility === "") {
    form.style.visibility = "visible";
  } else {
    form.style.visibility = "hidden";
  }
}
