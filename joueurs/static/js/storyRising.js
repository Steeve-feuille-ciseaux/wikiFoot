document.addEventListener("DOMContentLoaded", () => {
  const items = Array.from(document.querySelectorAll(".timeline-item"));
  const nextBtn = document.getElementById("next-btn");
  const endMessage = document.getElementById("end-message");
  const celebrationBtn = document.getElementById("celebration-btn");
  const congratsMsg = document.getElementById("congrats-msg");
  const closeCongrats = document.getElementById("close-congrats");
  const closePopup = document.getElementById("close-popup");

  let current = 0;

  // Affiche le premier élément
  if (items.length > 0) {
    items[current].classList.remove("hidden");
  }

  // Bouton "Match suivant"
  nextBtn.addEventListener("click", () => {
    current++;
    if (current < items.length) {
      items[current].classList.remove("hidden");
    }

    if (current === items.length - 1) {
      nextBtn.innerText = "Voir la victoire finale";
    }

    if (current >= items.length) {
      endMessage.classList.remove("hidden");
      nextBtn.style.display = "none";

      // Afficher le bouton célébration après 1 seconde
      setTimeout(() => {
        celebrationBtn.classList.remove("hidden");
      }, 1000);
    }
  });

  // Bouton "Célébration"
  celebrationBtn.addEventListener("click", () => {
    congratsMsg.classList.add("show");
  });

  // Bouton fermer le popup (croix)
  closePopup.addEventListener("click", () => {
    congratsMsg.classList.remove("show");
  });

  // Bouton fermer le popup (bouton de célébration)
  if (closeCongrats) {
    closeCongrats.addEventListener("click", () => {
      congratsMsg.classList.remove("show");
    });
  }
});