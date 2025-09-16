// Toggle mobile menu
document.addEventListener("DOMContentLoaded", () =>{


    const menuToggle = document.getElementById("menu-toggle");
    const navLinks = document.querySelector(".nav-links");

    const navLinkObject = document.querySelectorAll(".nav-links a");

    const UpgradeToggle = document.getElementById("upgrade-account");
    const formLinks = document.querySelector(".user-upgrade");

    UpgradeToggle.addEventListener("click", (e) => {
      e.preventDefault();
      formLinks.classList.toggle("show");
    });

    menuToggle.addEventListener("click", () => {
      navLinks.classList.toggle("active");
    });

    navLinkObject.forEach(link => {
        link.addEventListener("click", () => {
          navLinks.classList.remove("active");
    });
    });



    document.getElementById('errorLink').addEventListener('click', function(event) {
      event.preventDefault();
      showError("You don't have active downlines to request a withdrawal");
    });

    function showError(errorMessage) {
      var errorContainer = document.createElement('div');
      errorContainer.classList.add('error-container');

      var errorIcon = document.createElement('div');
      errorIcon.classList.add('error-icon');
      errorContainer.appendChild(errorIcon);

      var errorText = document.createElement('p');
      errorText.textContent = errorMessage;
      errorContainer.appendChild(errorText);

      document.body.appendChild(errorContainer);

      setTimeout(function() {
        errorContainer.remove();
      }, 3000); // Remove the error container after 3 seconds
    }

    /* document.addEventListener("DOMContentLoaded", function(){
      let names = document.querySelectorAll(".names");
      let index = 0;

      names[index].classList.add("active");

      function SwitchImgs(){
        names[index].classList.remove("active");

        index = (index + 1)

        names[index].classList.add("active")
      }
      setInterval(SwitchImgs, 500)
    }); */

});