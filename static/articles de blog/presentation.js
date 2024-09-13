<script>// Create the main div element
// Create the outer container div
const layoutElementDiv = document.createElement('div');
layoutElementDiv.classList.add('layout-element', 'layout-element--layout', 'layout-element', 'transition', 'transition--undefined');
layoutElementDiv.style = '--m-element-margin: 0 0 16px 0; --z-index: 2; --grid-row: 3/4; --grid-column: 2/7; --m-grid-row: 4/5; --m-grid-column: 1/2; --11a26299: 1278px; --5ac4fa85: 1612px;';
layoutElementDiv.dataset.v9ddc5313 = '';

const textBoxDiv = document.createElement('div');
textBoxDiv.classList.add('text-box', 'layout-element__component', 'layout-element__component--GridTextBox');
textBoxDiv.id = 'z8ufBY';
textBoxDiv.dataset.v9ddc5313 = '';
textBoxDiv.style = '--e37ab634: break-spaces; --d41b3428: rgb(241, 241, 241); --397f45b0: break-spaces;';
textBoxDiv.dataset.qa = 'gridtextbox:z8ufby';
textBoxDiv.style.backgroundColor = 'rgb(250, 250, 250)'; // Ou une autre couleur presque blanche de votre choix
textBoxDiv.style.padding = '40px';
textBoxDiv.style.fontFamily = 'Manrope, sans-serif';

// Append textBoxDiv to the outer container
layoutElementDiv.appendChild(textBoxDiv);

// Create the h1 element
const h1 = document.createElement('h1');
h1.dir = 'auto';
h1.style = 'color: rgb(29, 30, 32); --lineHeightDesktop: 1.3; --fontSizeDesktop: 48px';
h1.textContent = 'Chers passionnés de numismatique et investisseurs avisés,';
h1.style.marginBottom = '3rem';
h1.style.fontSize = '36px';

// Create the paragraphs
const p1 = document.createElement('p');
p1.dir = 'auto';
p1.style = 'color: rgb(29, 30, 32); --lineHeightDesktop: 1.3; --fontSizeDesktop: 24px';
p1.classList.add('body');
p1.innerHTML = '&nbsp;&nbsp;&nbsp;&nbsp; Nous sommes ravis de vous accueillir sur notre plateforme, spécialement conçue pour vous aider à naviguer dans le monde fascinant des Louis d\'or. Vous vous demandez quel est le <strong>prix d\'un Louis d\'or</strong> aujourd\'hui ? Vous souhaitez comparer les offres des différentes plateformes françaises ? Ne cherchez plus, vous êtes au bon endroit !';
p1.style.marginBottom = '1rem';
p1.style.fontSize = '24px';

const p2 = document.createElement('p');
p2.dir = 'auto';
p2.style = 'color: rgb(29, 30, 32); --lineHeightDesktop: 1.3; --fontSizeDesktop: 24px';
p2.classList.add('body');
p2.innerHTML = 'Notre site répertorie en temps réel les <strong>prix des Louis d\'or</strong> proposés par les principales plateformes françaises. Plus besoin de passer des heures à éplucher les sites un par un, nous avons fait le travail pour vous.';
p2.style.marginBottom = '1rem';
p2.style.fontSize = '24px';

const p3 = document.createElement('p');
p3.dir = 'auto';
p3.style = 'color: rgb(29, 30, 32); --lineHeightDesktop: 1.3; --fontSizeDesktop: 24px';
p3.classList.add('body');
p3.textContent = 'Pourquoi choisir notre comparateur ?';
p3.style.marginBottom = '1rem';
p3.style.fontSize = '24px';

// Create the unordered list (ul)
const ul = document.createElement('ul');
ul.dir = 'auto';

// Create the list items (li) and their content
const li1 = document.createElement('li');
li1.style = 'color: rgb(29, 30, 32)';
const pLi1 = document.createElement('p');
pLi1.dir = 'auto';
pLi1.style = 'color: rgb(29, 30, 32); --lineHeightDesktop: 1.3; --fontSizeDesktop: 24px';
pLi1.classList.add('body');
pLi1.innerHTML = '<strong>Simple</strong> : Une interface claire et intuitive pour trouver rapidement l\'information que vous cherchez.';
li1.appendChild(pLi1);
const pLi1Empty = document.createElement('p');
pLi1Empty.dir = 'auto';
pLi1Empty.style = 'color: rgb(29, 30, 32); --lineHeightDesktop: 1.3; --fontSizeDesktop: 24px';
pLi1Empty.classList.add('body');
li1.appendChild(pLi1Empty);
li1.style.marginBottom = '1rem';
li1.style.marginLeft = '2rem';
li1.style.fontSize = '24px';

const li2 = document.createElement('li');
li2.style = 'color: rgb(29, 30, 32)';
const pLi2 = document.createElement('p');
pLi2.dir = 'auto';
pLi2.style = 'color: rgb(29, 30, 32); --lineHeightDesktop: 1.3; --fontSizeDesktop: 24px';
pLi2.classList.add('body');
pLi2.innerHTML = '<strong>Actualisé</strong> : Les prix sont mis à jour 2 fois par jour pour vous proposer les données les plus récentes.*';
li2.appendChild(pLi2);
const pLi2Empty = document.createElement('p');
pLi2Empty.dir = 'auto';
pLi2Empty.style = 'color: rgb(29, 30, 32); --lineHeightDesktop: 1.3; --fontSizeDesktop: 24px';
pLi2Empty.classList.add('body');
li2.appendChild(pLi2Empty);
li2.style.marginBottom = '1rem';
li2.style.marginLeft = '2rem';
li2.style.fontSize = '24px';

const li3 = document.createElement('li');
li3.style = 'color: rgb(29, 30, 32)';
const pLi3 = document.createElement('p');
pLi3.dir = 'auto';
pLi3.style = 'color: rgb(29, 30, 32); --lineHeightDesktop: 1.3; --fontSizeDesktop: 24px';
pLi3.classList.add('body');
pLi3.innerHTML = '<strong>Comparatif</strong> : Visualisez en un clin d\'œil les offres des différentes plateformes et faites le meilleur choix.';
li3.appendChild(pLi3);
const pLi3Empty = document.createElement('p');
pLi3Empty.dir = 'auto';
pLi3Empty.style = 'color: rgb(29, 30, 32); --lineHeightDesktop: 1.3; --fontSizeDesktop: 24px';
pLi3Empty.classList.add('body');
li3.appendChild(pLi3Empty);
li3.style.marginBottom = '1rem';
li3.style.marginLeft = '2rem';
li3.style.fontSize = '24px';

const li4 = document.createElement('li');
li4.style = 'color: rgb(29, 30, 32)';
const pLi4 = document.createElement('p');
pLi4.dir = 'auto';
pLi4.style = 'color: rgb(29, 30, 32); --lineHeightDesktop: 1.3; --fontSizeDesktop: 24px';
pLi4.classList.add('body');
pLi4.innerHTML = '<strong>Fiabilité</strong> : Nous sélectionnons rigoureusement les plateformes référencées pour vous assurer des transactions sécurisées.';
li4.appendChild(pLi4);
const pLi4Empty = document.createElement('p');
pLi4Empty.dir = 'auto';
pLi4Empty.style = 'color: rgb(29, 30, 32); --lineHeightDesktop: 1.3; --fontSizeDesktop: 24px';
pLi4Empty.classList.add('body');
li4.appendChild(pLi4Empty);
li4.style.marginBottom = '1rem';
li4.style.marginLeft = '2rem';
li4.style.fontSize = '24px';

// ... (Similarly create li3 and li4 with their content)

// Append list items to the unordered list
ul.appendChild(li1);
ul.appendChild(li2);
ul.appendChild(li3);
ul.appendChild(li4);
// ... (Append li3 and li4 to ul)

// Create the remaining paragraphs
const p4 = document.createElement('p');
p4.dir = 'auto';
p4.style = 'color: rgb(29, 30, 32); --lineHeightDesktop: 1.3; --fontSizeDesktop: 24px';
p4.classList.add('body');
p4.innerHTML = 'Que vous soyez un collectionneur chevronné ou un investisseur débutant, notre site est votre allié pour acheter ou vendre des Louis d\'or au meilleur <strong>prix</strong>.';
p4.style.marginBottom = '1rem';
p4.style.fontSize = '24px';

const p5 = document.createElement('p');
p5.dir = 'auto';
p5.style = 'color: rgb(29, 30, 32); --lineHeightDesktop: 1.3; --fontSizeDesktop: 24px';
p5.classList.add('body');
p5.textContent = 'N\'attendez plus, plongez dans l\'univers des Louis d\'or et faites des affaires en toute confiance !';
p5.style.marginBottom = '3rem';
p5.style.fontSize = '24px';

const p6 = document.createElement('p');
p6.dir = 'auto';
p6.style = 'color: rgb(29, 30, 32); --lineHeightDesktop: 1.3; --fontSizeDesktop: 24px';
p6.classList.add('body');
p6.innerHTML = 'L\'équipe du comparateur de <strong>prix Louis d\'or</strong>.';
p6.style.marginBottom = '2rem';
p6.style.fontSize = '24px';

const p7 = document.createElement('p');
p7.dir = 'auto';
p7.style = 'color: rgb(29, 30, 32); --lineHeightDesktop: 0.5; --fontSizeDesktop: 18px';
p7.classList.add('body');
p7.style.marginBottom = '1rem';
p7.style.fontSize = '24px';

// Append all elements to the main div
textBoxDiv.appendChild(h1);
textBoxDiv.appendChild(p1);
textBoxDiv.appendChild(p2);
textBoxDiv.appendChild(p3);
textBoxDiv.appendChild(ul);
textBoxDiv.appendChild(p4);
textBoxDiv.appendChild(p5);
textBoxDiv.appendChild(p6);
textBoxDiv.appendChild(p7);

// Append the main div to the desired location in your document
document.body.appendChild(layoutElementDiv); // Or append to another specific element</script>