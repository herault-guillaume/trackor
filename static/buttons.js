<script>
        const urls = [
            { url: "https://storage.googleapis.com/prixlouisdor/20_fr_france.json", name: '20 Fr 🇫🇷', id: '20-francs-france' },
            { url: "https://storage.googleapis.com/prixlouisdor/10_fr_france.json", name: '10 Fr 🇫🇷', id: '10-francs-france' },
            { url: "https://storage.googleapis.com/prixlouisdor/20_fr_suisse.json", name: '20 Fr 🇨🇭', id: '20-francs-suisse' },
            { url: "https://storage.googleapis.com/prixlouisdor/5_dol_usa.json", name: '5 $ 🇺🇸', id: '5-dollars-usa' },
            { url: "https://storage.googleapis.com/prixlouisdor/10_dol_usa.json", name: '10 $ 🇺🇸', id: '10-dollars-usa' },
            { url:"https://storage.googleapis.com/prixlouisdor/20_dol_usa.json", name: '20 $ 🇺🇸', id: '20-dollars-usa' },
            { url: "https://storage.googleapis.com/prixlouisdor/1_oz_krugerrand.json", name: '1 Oz 🇿🇦', id: '1-oz-afrique' },
            { url: "https://storage.googleapis.com/prixlouisdor/1_2_souv_ru.json", name: 'Demi Souv. 🇬🇧', id: 'demi-souv-ru' },
            { url:"https://storage.googleapis.com/prixlouisdor/1_souv_ru.json", name: '1 Souv. 🇬🇧', id: '1-souv-ru' },
            { url:"https://storage.googleapis.com/prixlouisdor/20_fr_belgique.json", name: '20 Fr 🇧🇪', id: '20-fr-belgique' },
            { url: "https://storage.googleapis.com/prixlouisdor/20_lires_italie.json", name: '20 Lires 🇮🇹', id: '20-lires-italie' },
            { url: "https://storage.googleapis.com/prixlouisdor/20_mark_all.json", name: '20 Marks 🇩🇪', id: '20-mark-all' },
            { url: "https://storage.googleapis.com/prixlouisdor/50_pesos_mex.json", name: '50 Pesos 🇲🇽', id: '50-pesos-mex' },
            { url: "https://storage.googleapis.com/prixlouisdor/best_deals.json", name: '↘️ €/g', id:'best_deals' },
        ];


        // Crée le conteneur principal
        const containerMain = document.createElement('container');
        containerMain.id = 'container-main';
        containerMain.style.display = 'grid';
        containerMain.style.gridTemplateColumns = '1fr';
        containerMain.style.gap = '20px';
        containerMain.style.padding = '5px';

        // Crée le conteneur pour les boutons de pièces une seule fois
        const containerCoins = document.createElement('container');
        containerCoins.id = 'container-coins-name';
        containerCoins.style.display = 'grid';
        containerCoins.style.gridTemplateColumns = '1fr';
        containerCoins.style.gap = '20px';
        containerCoins.style.padding = '20px';

        // Ajoute le conteneur des boutons de pièces au conteneur principal

        containerCoins.style.gridColumn = '1 / 2';
        containerCoins.style.justifySelf = 'center';

        function createButtons(url,button_id) {
               // Supprime l'ancien conteneur s'il existe
              while (containerCoins.firstChild) {
                containerCoins.removeChild(containerCoins.firstChild);
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
                         if (button_id === 'best_deals') {
                          button.textContent = item.name;
                        } else {
                          button.textContent = url.hostname.replace(/(?:www\.|\.fr|\.be|\.com)/gi, '');
                        }
                        textSpan.style.color = '#fff';
                        button.appendChild(textSpan);

                        // Button styling
                        button.style.padding = '10px 30px'; // Adjusted padding to accommodate the overlapping container
                        button.style.fontFamily = 'Manrope';
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
                        const rainbowSquare = document.createElement('container');
                        rainbowSquare.style.content = "''";
                        rainbowSquare.style.width = '800px';
                        rainbowSquare.style.height = '800px';
                        rainbowSquare.style.position = 'absolute';
                        rainbowSquare.style.top = '-100px';
                        rainbowSquare.style.left = '-200px';
                        rainbowSquare.style.backgroundImage = 'linear-gradient(225deg, #9c6e2aff 0%, #fccc7c 50%, #fcc069 100%)';
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
                        const overlappingContainer = document.createElement('container');
                        overlappingContainer.style.position = 'absolute';
                        overlappingContainer.style.bottom = '50%';
                        overlappingContainer.style.right = '10%';
                        overlappingContainer.style.transform = 'translate(50%, 50%)';
                        overlappingContainer.style.display = 'flex';
                        overlappingContainer.style.alignItems = 'center';
                        overlappingContainer.style.color = '#fff';
                        overlappingContainer.style.zIndex = '1';

                        const changeSpan = document.createElement('span');

                        changeSpan.textContent = item.prime + ' %';

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
                        containerCoins.appendChild(button);
                    });

                    // Create a text element to display the last update time
                    const lastUpdateText = document.createElement('p');
                    lastUpdateText.textContent = `${lastUpdateTime}`;
                    lastUpdateText.style.textAlign = 'center';
                    lastUpdateText.style.marginBottom = '0px';
                    lastUpdateText.style.color = 'white';
                    lastUpdateText.style.fontFamily = 'Manrope';
                    lastUpdateText.style.fontSize = '0.8rem';

                    // Insert the text element at the beginning of the container
                    containerCoins.insertBefore(lastUpdateText, containerCoins.firstChild);

                })
                .catch(error => {
                    console.error('Error fetching or processing data:', error);
                });

        }
        function createButtonForUrl(url, name, id) {
            const button = document.createElement('button');

            button.textContent = name; // Utilise le nom pour le texte du bouton
            button.id = id; // Utilise le nom pour le texte du bouton
            button.style.padding = '5px 5px'; // Adjusted padding to accommodate the overlapping container
            button.style.fontFamily = 'Manrope';
            button.style.fontWeight = 'bold';
            button.style.fontSize = '1.0rem';
            button.style.textAlign = 'center';
            button.style.cursor = 'crosshair';
            button.style.border = 'solid';
            button.style.borderColor = 'transparent';
            button.style.borderWidth = 'medium';
            button.style.background = 'transparent';
            button.style.transition = 'all 0.2s';
            button.style.overflow = 'hidden'; // Keep overflow hidden
            button.style.color = '#fff';
            button.style.borderRadius = '30px';
            button.style.boxShadow = '0px -0px 0px 0px rgba(143, 64, 248, .5), 0px 0px 0px 0px rgba(39, 200, 255, .5)';
            // Apply CSS styles directly to the button element
            button.style.position = 'absolute';
            button.style.minWidth = '100px'


            // Rainbow Square Effect (Optional)
            const rainbowSquare = document.createElement('container');
            rainbowSquare.style.content = "''";
            rainbowSquare.style.width = '200px';
            rainbowSquare.style.height = '200px';
            rainbowSquare.style.position = 'absolute';
            rainbowSquare.style.top = '-100px';
            rainbowSquare.style.left = '0px';
            rainbowSquare.style.backgroundImage = 'linear-gradient(225deg, #fcc069 0%, #fccc7c 50%, #9c6e2aff 100%)';
            rainbowSquare.style.zIndex = '-1';
            rainbowSquare.style.transition = 'all .5s';

            button.addEventListener('mouseover', () => {
            rainbowSquare.style.transform = 'rotate(180deg)';

            });

            button.addEventListener('mouseout', () => {
                rainbowSquare.style.transform = 'none';
                button.style.transform = 'none';
            });

            button.appendChild(rainbowSquare);

            button.addEventListener('click', () => {
            // Désactive tous les boutons
            const allButtons = document.querySelectorAll('#tagscloud button');
            allButtons.forEach(btn => {
              btn.classList.remove('active'); // Bordure dorée par défaut
              btn.style.borderColor = 'transparent';


            });

            // Active le bouton cliqué et applique le style
            button.classList.add('active');
            button.style.border = 'solid';
            button.style.borderColor = '#5dda39';
            button.style.borderWidth = 'medium';

            createButtons(url,button.id);
        });

        return button;
        }

        function generateButtons() {
            const tagsCloudContainer = document.createElement('container');
            tagsCloudContainer.id = 'tagscloud';
            tagsCloudContainer.style.display = 'grid';
            tagsCloudContainer.style.gridTemplateColumns = '1fr';
            tagsCloudContainer.style.gridColumn = '1 / 2';
            tagsCloudContainer.style.justifySelf = 'center';
            tagsCloudContainer.style.position = 'relative';
            tagsCloudContainer.style.height = '210px'
            tagsCloudContainer.style.width = '90%';
            // Center the tagsCloudContainer
            //tagsCloudContainer.style.top = '0%';
            //tagsCloudContainer.style.left = '0%';
            //tagsCloudContainer.style.transform = 'translate(0%, 0%)';

            urls.forEach(item => {
                const button = createButtonForUrl(item.url, item.name, item.id);
                tagsCloudContainer.appendChild(button);
            });
            // Append the tagsCloudContainer and containerCoins to the main container
            containerMain.appendChild(tagsCloudContainer);
            containerMain.appendChild(containerCoins);
            document.body.appendChild(containerMain);

            var radius = 90;
            var d = 210;
            var dtr = Math.PI / 180;
            var mcList = [];
            var lasta = 1;
            var lastb = 1;
            var distr = true;
            var tspeed = 11;
            var size = 210;
            var mouseX = 0;
            var mouseY = 10;
            var howElliptical = 1;
            var bB = null;
            var oDiv = null;
            window.onload=function ()
            {
                var i=0;
                var oTag=null;
                oDiv=document.getElementById('tagscloud');
                bB=oDiv.getElementsByTagName('button');
                for(i=0;i<bB.length;i++)
                {
                    oTag={};
                    bB[i].onmouseover = (function (obj) {
                        return function () {
                            obj.on = true;
                            this.style.zIndex = 9999;
                            this.style.color = '#fff';
                            this.style.padding = '5px 5px';
                            this.style.filter = "alpha(opacity=100)";
                            this.style.opacity = 1;
                        }
                    })(oTag)
                    bB[i].onmouseout = (function (obj) {
                        return function () {
                            obj.on = false;
                            this.style.zIndex = obj.zIndex;
                            this.style.color = '#fff';
                            this.style.padding = '5px';
                            this.style.filter = "alpha(opacity=" + 100 * obj.alpha + ")";
                            this.style.opacity = obj.alpha;
                            this.style.zIndex = obj.zIndex;
                        }
                    })(oTag)
                    oTag.offsetWidth = bB[i].offsetWidth;
                    oTag.offsetHeight = bB[i].offsetHeight;
                    mcList.push(oTag);
                }
                sineCosine( 0,0,0 );
                positionAll();
                (function () {
                        update();
                        setTimeout(arguments.callee, 40);
                    })();
                    // Get the first button (or identify your default button using another method)
                const defaultButton = document.querySelector('#tagscloud button');

                // Simulate a click on the default button
                if (defaultButton) {
                  defaultButton.click();
                }
            };
            function update()
            {
                var a, b, c = 0;
                a = (Math.min(Math.max(-mouseY, -size), size) / radius) * tspeed;
                b = (-Math.min(Math.max(-mouseX, -size), size) / radius) * tspeed;
                lasta = a;
                lastb = b;
                if (Math.abs(a) <= 0.01 && Math.abs(b) <= 0.01) {
                    return;
                }
                sineCosine(a, b, c);

                const activeButton = Array.from(bB).find(btn => btn.classList.contains('active'));

                for (var i = 0; i < mcList.length; i++) {
                    if (mcList[i].on) {
                        continue;
                    }
                                        // Adjust z-index based on whether the button is clicked or not
                    if (activeButton && bB[i] === activeButton) {
                        // If it's the clicked button, set its z-index to the highest
                        mcList[i].zIndex = mcList.length;
                        activeButton.style.opacity =1;
                        continue
                    } else {
                        // Otherwise, calculate z-index normally but ensure it's lower than the clicked button
                        mcList[i].zIndex = Math.ceil(100 - Math.floor(mcList[i].cz));
                        if (activeButton) {
                            mcList[i].zIndex = Math.min(mcList[i].zIndex, mcList.length - 1);
                        }
                    }
                            // Check if the button is clicked (has the 'active' class)
                    if (bB[i].classList.contains('active')) {
                        continue; // Skip updating position, z-index, and alpha if clicked
                    }
                    var rx1 = mcList[i].cx;
                    var ry1 = mcList[i].cy * ca + mcList[i].cz * (-sa);
                    var rz1 = mcList[i].cy * sa + mcList[i].cz * ca;

                    var rx2 = rx1 * cb + rz1 * sb;
                    var ry2 = ry1;
                    var rz2 = rx1 * (-sb) + rz1 * cb;

                    var rx3 = rx2 * cc + ry2 * (-sc);
                    var ry3 = rx2 * sc + ry2 * cc;
                    var rz3 = rz2;

                    mcList[i].cx = rx3;
                    mcList[i].cy = ry3;
                    mcList[i].cz = rz3;

                    per = d / (d + rz3);

                    mcList[i].x = (howElliptical * rx3 * per) - (howElliptical * 2);
                    mcList[i].y = ry3 * per;
                    mcList[i].scale = per;
                    var alpha = per;
                    alpha = (alpha - 0.6) * (10 / 6);
                    mcList[i].alpha = alpha * alpha * alpha - 0.2;


                }
                doPosition();
            }
            function positionAll()
            {
                var phi = 0;
                var theta = 0;
                var max = mcList.length;
                for (var i = 0; i < max; i++) {
                    if (distr) {
                        phi = Math.acos(-1 + (2 * (i + 1) - 1) / max);
                        theta = Math.sqrt(max * Math.PI) * phi;
                    } else {
                        phi = Math.random() * (Math.PI);
                        theta = Math.random() * (2 * Math.PI);
                    }
                    //坐标变换
                    mcList[i].cx = radius * Math.cos(theta) * Math.sin(phi);
                    mcList[i].cy = radius * Math.sin(theta) * Math.sin(phi);
                    mcList[i].cz = radius * Math.cos(phi);

                    bB[i].style.left = mcList[i].cx + oDiv.offsetWidth / 2 - mcList[i].offsetWidth / 2 + 'px';
                    bB[i].style.top = mcList[i].cy + oDiv.offsetHeight / 2 - mcList[i].offsetHeight / 2 + 'px';
                }
            }
            function doPosition()
            {
                var l = oDiv.offsetWidth / 2;
                    var t = oDiv.offsetHeight / 2;
                    for (var i = 0; i < mcList.length; i++) {
                        if (mcList[i].on) {
                            continue;
                        }
                        var aAs = bB[i].style;
                        if (mcList[i].alpha > 0.1) {
                            if (aAs.display != '')
                                aAs.display = '';
                        } else {
                            if (aAs.display != 'none')
                                aAs.display = 'none';
                            continue;
                        }
                        aAs.left = mcList[i].cx + l - mcList[i].offsetWidth / 2 + 'px';
                        aAs.top = mcList[i].cy + t - mcList[i].offsetHeight / 2 + 'px';
                        //aAs.fontSize=Math.ceil(12*mcList[i].scale/2)+8+'px';
                        //aAs.filter="progid:DXImageTransform.Microsoft.Alpha(opacity="+100*mcList[i].alpha+")";
                        if (bB[i].classList.contains('active')) {
                            aAs.opacity = 1;
                        } else {
                            aAs.filter = "alpha(opacity=" + 100 * mcList[i].alpha + ")";
                            aAs.opacity = mcList[i].alpha;
                        }
                        aAs.zIndex = mcList[i].zIndex;
                    }
            }
            function sineCosine( a, b, c)
            {
                sa = Math.sin(a * dtr);
                ca = Math.cos(a * dtr);
                sb = Math.sin(b * dtr);
                cb = Math.cos(b * dtr);
                sc = Math.sin(c * dtr);
                cc = Math.cos(c * dtr);
            }
        }

        // Appelle cette fonction pour générer les boutons au chargement de la page
        generateButtons();

        //createButtons();
    </script>