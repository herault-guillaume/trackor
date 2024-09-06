<script>
        const urls = [
            { url: "https://storage.googleapis.com/prixlouisdor/10_dol_usa.json", name: '10 Dollars USA' },
            { url: "https://storage.googleapis.com/prixlouisdor/10_fr_france.json", name: '10 Francs FR' },
            { url: "https://storage.googleapis.com/prixlouisdor/1_2_souv_ru.json", name: '1/2 Souv. UK' },
            { url: "https://storage.googleapis.com/prixlouisdor/1_oz_krugerrand.json", name: '1 Oz Kruggerand' },
            { url:"https://storage.googleapis.com/prixlouisdor/1_souv_ru.json", name: '1 Souv. UK' },
            { url:"https://storage.googleapis.com/prixlouisdor/20_dol_usa.json", name: '20 Dollars USA' },
            { url:"https://storage.googleapis.com/prixlouisdor/20_fr_belgique.json", name: '20 Francs BEL' },
            { url: "https://storage.googleapis.com/prixlouisdor/20_fr_france.json", name: '10 Francs FR' },
            { url: "https://storage.googleapis.com/prixlouisdor/20_fr_suisse.json", name: '20 Francs SUI' },
            { url: "https://storage.googleapis.com/prixlouisdor/20_lires_italie.json", name: '20 Lires ITA' },
            { url: "https://storage.googleapis.com/prixlouisdor/20_mark_all.json", name: '20 Mark DE' },
            { url: "https://storage.googleapis.com/prixlouisdor/50_pesos_mex.json", name: '50 Pesos MEX' },
            { url: "https://storage.googleapis.com/prixlouisdor/5_dol_usa.json", name: '5 Dollars USA' },
            //{ url: "https://storage.googleapis.com/prixlouisdor/best_deals.json", name: 'Bests deals' },
        ];

        const container = document.createElement('container-coins-name');
        container.style.display = 'grid';
        container.style.gap = '20px';
        container.style.padding = '20px';

        function createButtons(url) {
               // Supprime l'ancien conteneur s'il existe
              while (container.firstChild) {
                container.removeChild(container.firstChild);
              }

            fetch(url,  {
            cache: 'no-store',
            })
                .then(response => {
                    if (!response.ok) {
                        throw new Error(`HTTP error! status: ${response.status}`);
                    }
                    return response.json();
                })
                .then(data => {
                    if (!data || data.length === 0) {
                        console.error('No data received from site_data.json');
                        return;
                    }

                    // Extract last update time from data (assuming it's in a field called 'last_update')
                    const lastUpdateTime = data[0].last_updated; // Adjust if the field name is different

                    const numButtons = data.length;
                    const midIndex = Math.floor(numButtons / 2);

                    data.slice(0, numButtons).forEach((item,index) => {
                        // Button
                        const button = document.createElement('a');
                        const url = new URL(item.source);
                        button.href = url;
                        button.target = "_blank";
                        button.rel = "noopener noreferrer";

                        const textSpan = document.createElement('span');
                        textSpan.textContent = url.hostname.replace(/(?:www\.|\.fr|\.be|\.com)/gi, '');
                        textSpan.style.color = '#fff';
                        button.appendChild(textSpan);

                        // Button styling
                        button.style.padding = '10px 30px'; // Adjusted padding to accommodate the overlapping container
                        button.style.fontFamily = 'Lora';
                        button.style.fontWeight = 'bold';
                        button.style.fontSize = '1.1rem';
                        button.style.textAlign = 'center';
                        button.style.cursor = 'pointer';
                        button.style.border = 'none';
                        button.style.background = 'transparent';
                        button.style.position = 'relative';
                        button.style.transition = 'all 0.2s';
                        button.style.overflow = 'hidden'; // Keep overflow hidden
                        button.style.color = '#fff';
                        button.style.borderRadius = '30px';
                        button.style.boxShadow = '0px -0px 0px 0px rgba(143, 64, 248, .5), 0px 0px 0px 0px rgba(39, 200, 255, .5)';


                        // Rainbow Square Effect (Optional)
                        const rainbowSquare = document.createElement('div');
                        rainbowSquare.style.content = "''";
                        rainbowSquare.style.width = '800px';
                        rainbowSquare.style.height = '800px';
                        rainbowSquare.style.position = 'absolute';
                        rainbowSquare.style.top = '-100px';
                        rainbowSquare.style.left = '-200px';
                        rainbowSquare.style.backgroundImage = 'linear-gradient(225deg, #debc71ff 0%, #b69543ff 50%, #9c6e2aff 100%)';
                        rainbowSquare.style.zIndex = '-1';
                        rainbowSquare.style.transition = 'all .5s';

                        button.addEventListener('mouseover', () => {
                            rainbowSquare.style.transform = 'rotate(180deg)';
                            button.style.transform = 'translate(0,-6px)';
                        });

                        button.addEventListener('mouseout', () => {
                            rainbowSquare.style.transform = 'none';
                            button.style.transform = 'none';
                            button.style.boxShadow = '0px -0px 0px 0px rgba(143, 64, 248, .5), 0px 0px 0px 0px rgba(39, 200, 255, .5)';
                        });

                        button.appendChild(rainbowSquare);

                        // Overlapping Container for Arrow and Percentage
                        const overlappingContainer = document.createElement('div');
                        overlappingContainer.style.position = 'absolute';
                        overlappingContainer.style.bottom = '50%';
                        overlappingContainer.style.right = '10%';
                        overlappingContainer.style.transform = 'translate(50%, 50%)';
                        overlappingContainer.style.display = 'flex';
                        overlappingContainer.style.alignItems = 'center';
                        overlappingContainer.style.color = '#fff';
                        overlappingContainer.style.zIndex = '1';

                        const changeSpan = document.createElement('span');
                        changeSpan.textContent = item.diff;
                        changeSpan.style.fontSize = '1.0rem';
                                       // Add class to changeSpan
                                // Apply oval styles directly to changeSpan
                        changeSpan.style.backgroundColor = 'rgba(0, 0, 0, 0.5)';
                        changeSpan.style.padding = '5px 10px';
                        changeSpan.style.borderRadius = '20px';
                        changeSpan.style.fontSize = '1.0rem';

                       // Calculate gradient color based on button index relative to the median
                        let r, g, b;
                        if (index === midIndex) {
                            // White for the median button
                            r = 255;
                            g = 255;
                            b = 255;
                        } else if (index < midIndex) {
                            // Green gradient for buttons before the median
                            const greenIntensity = Math.round(255 * (midIndex - index) / midIndex);
                            r = 255 - greenIntensity;;
                            g = 255;
                            b = 255 - greenIntensity;;
                        } else {
                            // Red gradient for buttons after the median
                            const redIntensity = Math.round(255 * (index - midIndex) / (numButtons - midIndex - 1));
                            r = 255;
                            g = 255 - redIntensity;
                            b = 255 - redIntensity;
                        }

                        const color = `rgb(${r}, ${g}, ${b})`;
                        changeSpan.style.color = color;

                        overlappingContainer.appendChild(changeSpan);

                        // Append to button
                        button.appendChild(overlappingContainer);

                        // Append button to container
                        container.appendChild(button);
                    });

                    // Create a text element to display the last update time
                    const lastUpdateText = document.createElement('p');
                    lastUpdateText.textContent = `${lastUpdateTime}`;
                    lastUpdateText.style.textAlign = 'center';
                    lastUpdateText.style.marginBottom = '0px';
                    lastUpdateText.style.color = 'white';
                    lastUpdateText.style.fontFamily = 'Lora';
                    lastUpdateText.style.fontSize = '0.8rem';

                    // Insert the text element at the beginning of the container
                    container.insertBefore(lastUpdateText, container.firstChild);

                })
                .catch(error => {
                    console.error('Error fetching or processing data:', error);
                });

            document.body.appendChild(container);
        }
        function createButtonForUrl(url, name) {
            const button = document.createElement('button');
            button.textContent = name; // Utilise le nom pour le texte du bouton
            button.addEventListener('click', () => {
            // Désactive tous les boutons
            const allButtons = document.querySelectorAll('#container-country-name button');
            allButtons.forEach(btn => {
              btn.classList.remove('active');
              btn.style.backgroundColor = ''; // Réinitialise la couleur de fond
            });
            console.log(url)
            // Active le bouton cliqué et applique le style
            button.classList.add('active');
            button.style.backgroundColor = 'lightblue';

            createButtons(url);
        });

        return button;
        }

        function generateButtons() {
            const container = document.createElement('container-country-name'); // Crée un div
            container.id = 'container-country-name'; // Ajoute l'ID
            container.style.display = 'grid-row';

            urls.forEach(item => {
                const button = createButtonForUrl(item.url, item.name); // Passe le nom à createButtonForUrl
                console.log('created')
                container.appendChild(button);
            });
            document.body.appendChild(container)
        }

        // Appelle cette fonction pour générer les boutons au chargement de la page
        generateButtons();
        //createButtons();
    </script>