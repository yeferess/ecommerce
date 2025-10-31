// Espera a que el DOM esté cargado
document.addEventListener("DOMContentLoaded", () => {
  const alerta = document.getElementById("alerta");
  const cerrar = document.getElementById("cerrar");

  if (alerta && cerrar) {
    cerrar.addEventListener("click", () => {
      // Agrega animación de desvanecimiento
      alerta.classList.add("opacity-0");

      // Espera 500ms y elimina el elemento
      setTimeout(() => {
        alerta.remove();
      }, 500);
    });
  }
});
