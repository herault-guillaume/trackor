<script>
  function createButtons() {
    const container = document.createElement('div');
    container.style.display = 'grid';
    container.style.gridTemplateColumns = '1fr';
    container.style.gap = '10px';
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

                // Create a container for the button and arrow/percentage
          const buttonContainer = document.createElement('div');
          buttonContainer.style.display = 'flex';
          buttonContainer.style.alignItems = 'center'

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

            buttonContainer.appendChild(button);

               // Arrow and Percentage
            const arrowPercentageContainer = document.createElement('div');
            arrowPercentageContainer.style.display = 'flex';
            arrowPercentageContainer.style.alignItems = 'flex-start'; // Align to the top
            arrowPercentageContainer.style.justifyContent = 'center';

            // Custom SVG Arrow (instead of the previous arrowSvg)
            const arrowSvg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
            arrowSvg.setAttribute("viewBox", "0 0 0.585029 1.4990282");
            arrowSvg.setAttribute('width', '16'); // Adjust width as needed
            arrowSvg.setAttribute('height', '16'); // Adjust height as needed
            arrowSvg.innerHTML = '<g transform="translate(-70.733191,-87.615908)"><g style="fill:#44ffff;fill-opacity:1;stroke:none;"><path style="fill:#ffffff;fill-opacity:1;stroke:none;" d="m 70.733191,87.615908 0.263454,0.683729 0.03066,-0.217931 c 0.200221,0.286655 0.172429,0.514203 0.09707,0.679997 -0.07857,0.172839 -0.212802,0.272604 -0.212802,0.272604 a 0.04473805,0.04473805 0 0 0 -0.0091,0.0628 0.04473805,0.04473805 0 0 0 0.06229,0.0091 c 0,0 0.152385,-0.111643 0.241501,-0.307692 0.08583,-0.18882 0.109502,-0.461306 -0.108171,-0.772014 l 0.220127,0.03078 z" /></g></g>';
            arrowSvg.style.marginLeft = '10px';
            // Percentage change (same as before)
            arrowPercentageContainer.appendChild(arrowSvg);

            // Button content - moved inside the loop
            const textSpan = document.createElement('span');
            textSpan.textContent = url.hostname;
            textSpan.style.color = '#fff';

            // Button content - moved inside the loop
            const changeSpan = document.createElement('span');
            changeSpan.textContent = ` ${Math.floor(Math.random() * 20) - 10}%`;
            changeSpan.style.color = '#fff';
            arrowPercentageContainer.appendChild(changeSpan);

            container.appendChild(arrowPercentageContainer);

          // Append arrow and percentage to the buttonContainer
          buttonContainer.appendChild(arrowSvg);
          buttonContainer.appendChild(changeSpan);
          container.appendChild(buttonContainer);
    })
  });

    document.body.appendChild(container);
  }

  createButtons();
</script>


