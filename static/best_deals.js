<script>
        function createButtons() {
            const container = document.createElement('container');
            container.style.display = 'grid';
            container.style.gap = '20px';
            container.style.padding = '20px';

            fetch('https://storage.googleapis.com/prixlouisdor/best_deals.json',  {
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
                })
                .catch(error => {
                    console.error('Error fetching or processing data:', error);
                });

            document.body.appendChild(container);
        }

        createButtons();
    </script>