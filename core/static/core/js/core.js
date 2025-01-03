(() => {
  "use strict";

  // Fetch all the forms we want to apply custom Bootstrap validation styles to
  const forms = document.querySelectorAll(".needs-validation");

  // Loop over them and prevent submission
  Array.from(forms).forEach((form) => {
    form.addEventListener(
      "submit",
      (event) => {
        if (!form.checkValidity()) {
          event.preventDefault();
          event.stopPropagation();
        }

        form.classList.add("was-validated");
      },
      false
    );
  });
})();


function displaySelectedImage(event, imgId) {
  const [file] = event.target.files;
  if (file) {
      const img = document.getElementById(imgId);
      img.src = URL.createObjectURL(file);
  }
}


function toggleCollapseOnResize() {
  var collapseElements = document.querySelectorAll(".filter-content");

  collapseElements.forEach(function (element) {
    if (window.innerWidth >= 992) {
      var bsCollapse = new bootstrap.Collapse(element, {
        toggle: true,
      });
    } else {
      var bsCollapse = new bootstrap.Collapse(element, {
        toggle: false,
      });
    }
  });
}

window.addEventListener("resize", toggleCollapseOnResize);
window.addEventListener("load", toggleCollapseOnResize);

