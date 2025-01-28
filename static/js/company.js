function imprimir() {
  const color = document.getElementById("color-picker").value;
  console.log(color);
}
function actualizarImg() {
  const imgPicker = document.getElementById("img-picker").value;
  const img = document.querySelector("img");
  img.src = imgPicker;
}
document.querySelectorAll(".btn-delete").forEach((button) => {
  button.addEventListener("click", (event) => {
    if (!confirm("¿Estás seguro de que deseas eliminar este elemento?")) {
      event.preventDefault();
    }
  });
});
