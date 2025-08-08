document.addEventListener('DOMContentLoaded', function() {
    // Éléments du DOM
    const modal = document.getElementById("modal");
    const modalContent = document.querySelector(".modal-content");
    const modalTexte = document.getElementById("modalTexte");
    const images = document.querySelectorAll(".modal-image");
    const precedentBtn = document.getElementById("precedentBtn");
    const suivantBtn = document.getElementById("suivantBtn");
    const closeBtn = document.getElementById("closeBtn");
    const progression = document.getElementById("progression");
    const lireSuiteBtn = document.getElementById("lireSuiteBtn");

    // Récupération des paragraphes depuis le DOM
    const paragrapheDivs = document.querySelectorAll('.paragraphe');
    const paragraphes = Array.from(paragrapheDivs).map(div => div.textContent.trim());
    const totalPages = paragraphes.length;

    let index = 0;

    function afficherPage(i) {
        index = i;

        // Arrêter toutes les transitions GIF actives
        if (window.GifTransit) {
            window.GifTransit.stopAllTransitions();
        }

        // Animation de sortie du texte
        modalTexte.classList.remove("visible");
        
        setTimeout(() => {
            // Affiche le nouveau texte
            modalTexte.textContent = paragraphes[i];
            
            // Masque toutes les images
            images.forEach(img => img.classList.remove("active"));
            
            // Affiche l'image correspondante selon l'attribut data-index
            const imageCorrespondante = document.querySelector(`img.modal-image[data-index="${i}"]`);
            if (imageCorrespondante) {
                imageCorrespondante.classList.add("active");
                
                // Démarrer la transition GIF si c'est un GIF
                if (window.GifTransit) {
                    window.GifTransit.start(imageCorrespondante);
                }
            }

            // Animation d'entrée du texte
            setTimeout(() => {
                modalTexte.classList.add("visible");
            }, 100);

            // Gestion des boutons
            precedentBtn.classList.toggle("hidden", i === 0);
            suivantBtn.classList.toggle("hidden", i === totalPages - 1);

            // Mise à jour de la progression
            progression.textContent = `Page ${i + 1}/${totalPages}`;
        }, 250);
    }

    function ouvrirModal() {
        modal.style.display = "flex";
        setTimeout(() => {
            modal.classList.add("visible");
            modalContent.classList.add("animate-in");
        }, 10);
        afficherPage(0);
    }

    function fermerModal() {
        // Arrêter toutes les transitions GIF
        if (window.GifTransit) {
            window.GifTransit.reset();
        }
        
        modal.classList.remove("visible");
        setTimeout(() => {
            modal.style.display = "none";
            modalContent.classList.remove("animate-in");
        }, 300);
    }

    // Événements des boutons
    precedentBtn.addEventListener('click', () => {
        if (index > 0) afficherPage(index - 1);
    });

    suivantBtn.addEventListener('click', () => {
        if (index < totalPages - 1) afficherPage(index + 1);
    });

    closeBtn.addEventListener('click', fermerModal);
    lireSuiteBtn.addEventListener('click', ouvrirModal);

    // Fermer modale si clic en dehors
    modal.addEventListener('click', (e) => {
        if (e.target === modal) fermerModal();
    });

    // Navigation au clavier
    document.addEventListener('keydown', (e) => {
        if (modal.style.display === 'flex') {
            if (e.key === 'ArrowLeft' && index > 0) {
                afficherPage(index - 1);
            } else if (e.key === 'ArrowRight' && index < totalPages - 1) {
                afficherPage(index + 1);
            } else if (e.key === 'Escape') {
                fermerModal();
            }
        }
    });

    // Initialisation de la progression avec le nombre total de pages
    if (progression && totalPages > 0) {
        progression.textContent = `Page 1/${totalPages}`;
    }
});