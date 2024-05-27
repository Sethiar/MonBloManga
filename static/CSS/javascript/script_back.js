// Code JavaScript pour l'apparition d'une fenêtre de dialogue afin d'affirmer la suppression.
document.addEventListener("DOMContentLoaded", () => {
  const inputImage = document.querySelector("#image");
  const previewImage = document.querySelector("#preview");

  inputImage.addEventListener("change", () => {
    const file = inputImage.files[0];
    const reader = new FileReader();

    reader.addEventListener("load", () => {
      previewImage.setAttribute("src", reader.result);
    });

    if (file) {
      reader.readAsDataURL(file);
    }
  });
});

// Code JavaScript pour confirmation de la suppression
document.addEventListener("DOMContentLoaded", () => {
  const deleteForms = document.querySelectorAll(".btn_suppression");
  deleteForms.forEach(form => {
    form.addEventListener("submit", (event) => {
      const confirmation = confirm("Êtes-vous sûr de vouloir supprimer cet article ?");
      if (!confirmation) {
        event.preventDefault();
      }
    });
  });
});

