<script>
  function createButtons() {
    const container = document.createElement('div');
    container.style.display = 'grid';
    container.style.gridTemplateColumns = '1fr';
    container.style.gap = '20px';
    container.style.padding = '20px';

  fetch('https://storage.googleapis.com/prixlouisdor/site_data.json')
    .then(response => {
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return response.json();
    })
    .then(data => {

      data = data.slice(0, 7);

      data.forEach((item, index) => {
            const button = document.createElement('a');
            const url = new URL(item.source);
            button.href = url;  // Use the 'source' from JSON
            button.target = "_blank";  // Use the 'source' from JSON
            button.rel = "noopener noreferrer";  // Use the 'source' from JSON
            button.textContent = `${url.hostname}`;

            // Styles du bouton
            button.style.padding = '10px 30px';
            button.style.fontFamily = 'Lora';  // Choose your desired font family
            button.style.fontWeight = 'bold';               // Make the text bold (optional)
            button.style.fontSize = '1.1rem';
            button.style.textAlign = 'center'
            button.style.cursor = 'pointer';
            button.style.border = '0px';
            button.style.background = 'transparent';
            button.style.position = 'relative';
            button.style.transition = 'all .2s';
            button.style.overflow = 'hidden';
            button.style.color = '#fff';
            button.style.borderRadius = '30px';
            button.style.boxShadow = '0px -0px 0px 0px rgba(143, 64, 248, .5), 0px 0px 0px 0px rgba(39, 200, 255, .5)';

            // Carré arc-en-ciel
            const rainbowSquare = document.createElement('div');
            rainbowSquare.style.content = "''";
            rainbowSquare.style.width = '800px';
            rainbowSquare.style.height = '800px';
            rainbowSquare.style.position = 'absolute';
            rainbowSquare.style.top = '-100px';
            rainbowSquare.style.left = '-200px';
            rainbowSquare.style.backgroundImage = 'linear-gradient(225deg, #debc71ff 0%, #b69543ff 50%, #9c6e2aff 100%)';

//            rainbowSquare.style.backgroundImage = 'linear-gradient(225deg, #27d86c 0%, #26caf8 50%, #c625d0 100%)';
            rainbowSquare.style.zIndex = '-1';
            rainbowSquare.style.transition = 'all .5s';

            // Effets au survol
            button.addEventListener('mouseover', () => {
            rainbowSquare.style.transform = 'rotate(180deg)';
            button.style.transform = 'translate(0,-6px)';
            });

            button.addEventListener('mouseout', () => {
            rainbowSquare.style.transform = 'none'; // Réinitialise la rotation
            button.style.transform = 'none'; // Réinitialise la translation
            button.style.boxShadow = '0px -0px 0px 0px rgba(143, 64, 248, .5), 0px 0px 0px 0px rgba(39, 200, 255, .5)'; // Réinitialise l'ombre
            });

            button.appendChild(rainbowSquare); // Ajoute le carré arc-en-ciel au bouton
            container.appendChild(button);
    })
  });

    document.body.appendChild(container);
  }

  createButtons();
</script>


