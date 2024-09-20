<script>
// Create the main div element
const layoutElementDiv = document.createElement('div');
layoutElementDiv.classList.add('layout-element', 'layout-element--layout', 'layout-element', 'transition', 'transition--undefined');
layoutElementDiv.style = '--m-element-margin: 0 0 16px 0; --z-index: 2; --grid-row: 3/4; --grid-column: 2/7; --m-grid-row: 4/5; --m-grid-column: 1/2; --11a26299: 1278px; --5ac4fa85: 1612px;';
layoutElementDiv.dataset.v9ddc5313 = '';

// Create the text box div
const textBoxDiv = document.createElement('div');
textBoxDiv.classList.add('text-box', 'layout-element__component', 'layout-element__component--GridTextBox');
textBoxDiv.id = 'z8ufBY';
textBoxDiv.dataset.v9ddc5313 = '';
textBoxDiv.style = '--e37ab634: break-spaces; --d41b3428: rgb(241, 241, 241); --397f45b0: break-spaces;';
textBoxDiv.dataset.qa = 'gridtextbox:z8ufby';
textBoxDiv.style.backgroundColor = 'rgb(250, 250, 250)';
textBoxDiv.style.padding = '40px';
textBoxDiv.style.fontFamily = 'Manrope, sans-serif';


// Append textBoxDiv to the outer container
layoutElementDiv.appendChild(textBoxDiv);

// Create the h1 element
const h1 = document.createElement('h1');
h1.dir = 'auto';
h1.style = 'color: rgb(29, 30, 32); --lineHeightDesktop: 1.3; --fontSizeDesktop: 48px';
h1.textContent = 'L\'Utilisation de la Prime des Pièces dans l\'Investissement en Or : Opportunités et Stratégies';
h1.style.marginBottom = '3rem';
h1.style.fontSize = '36px';

// Create the paragraphs
const paragraphs = [
    "La prime d'une pièce d'or, c'est-à-dire la différence entre son prix de marché et la valeur intrinsèque de l'or qu'elle contient, est un élément clé à prendre en compte lors d'un investissement dans les pièces d'or. Elle peut fluctuer en fonction de divers facteurs, tels que la rareté, l'état de conservation, la demande des collectionneurs et le contexte économique. Comprendre comment la prime évolue et comment l'utiliser peut s'avérer crucial pour optimiser ses investissements.",

    "L'histoire regorge d'exemples où la prime de certaines pièces d'or a connu une forte augmentation, offrant ainsi des gains substantiels aux investisseurs avisés.",

    "* La Double Eagle de 1933 : Cette pièce américaine, dont la plupart des exemplaires ont été fondus, est devenue l'une des pièces les plus chères au monde, avec une prime atteignant des millions de dollars. Sa rareté et son histoire tumultueuse ont contribué à cette envolée de sa prime.",

    "* Le Souverain d'Or Britannique de 1933 : Frappée en très petit nombre, cette pièce est très recherchée par les collectionneurs. Sa prime a considérablement augmenté au fil des ans, reflétant sa rareté et son attrait historique.",

    "* Les Napoléons en 2008 : La crise financière de 2008 a entraîné une ruée vers l'or, faisant grimper le prix de l'or et, par conséquent, la prime de nombreuses pièces, y compris les populaires Napoléons français. Certaines pièces ont vu leur prime doubler, voire tripler, pendant cette période.",

    "### Cas d'Usage d'une Prime Faible",

    "Acheter des pièces d'or avec une prime faible peut être une stratégie intéressante dans certaines situations :",

    "* Investissement axé sur le cours de l'or : Lorsque la prime est faible, le prix de la pièce est proche de la valeur de l'or qu'elle contient. Dans ce cas, l'investissement est principalement axé sur l'évolution du cours de l'or. Si le cours de l'or augmente, la valeur de la pièce suivra, même si sa prime reste stable ou augmente légèrement.",

    "* Potentiel d'appréciation de la prime : Une prime faible peut offrir un potentiel d'appréciation future. Si la pièce devient plus rare ou plus recherchée par les collectionneurs, sa prime pourrait augmenter, générant ainsi un gain supplémentaire en plus de l'augmentation du cours de l'or.",

    "* Diversification du portefeuille : Les pièces à faible prime peuvent être un moyen de diversifier un portefeuille d'investissement en or. Elles offrent une exposition au cours de l'or tout en limitant le risque lié à la fluctuation de la prime.",

    "**Ce que signifie une prime faible**",

    "Une prime faible signifie que vous payez un prix proche de la valeur intrinsèque de l'or contenu dans la pièce. Cela peut être dû à plusieurs facteurs :",

    "* Grande disponibilité : La pièce est courante et facilement accessible sur le marché.",
    "* Faible demande des collectionneurs** : La pièce n'est pas particulièrement recherchée par les collectionneurs.",
    "* Production récente : La pièce a été frappée récemment et n'a pas encore acquis une valeur numismatique significative.",

    "### Conclusion",

    "La prime des pièces d'or est un facteur important à considérer lors de l'investissement dans l'or physique. En comprenant comment la prime fonctionne et en identifiant les opportunités offertes par les pièces à faible prime, les investisseurs peuvent optimiser leurs stratégies et maximiser leurs rendements potentiels. Il est toutefois essentiel de se rappeler que l'investissement dans l'or comporte des risques, et il est recommandé de consulter un conseiller financier avant de prendre toute décision d'investissement."
];

// Create and append paragraph elements
paragraphs.forEach(paragraphText => {
    const p = document.createElement('p');
    p.dir = 'auto';
    p.style = 'color: rgb(29, 30, 32); --lineHeightDesktop: 1.3; --fontSizeDesktop: 24px';
    p.classList.add('body');

    // Check if the paragraph starts with ### (heading) or * (list item)
    if (paragraphText.startsWith('### ')) {
        p.innerHTML = `<h3>${paragraphText.substring(4)}</h3>`; // Remove ### and use <h3>
        p.style.marginBottom = '3rem';
        p.style.marginTop = '3rem';
    } else if (paragraphText.startsWith('* ')) {
        p.innerHTML = `<li>${paragraphText.substring(2)}</li>`; // Remove * and use <li>
        p.style.marginBottom = '1rem';
        p.style.marginLeft = '2rem';
    } else {
        p.textContent = paragraphText;
        p.style.marginBottom = '2rem';
    }

    p.style.fontSize = '24px'; // Adjust font size as needed

    textBoxDiv.appendChild(p);
});


// Append the main div to the desired location in your document
document.body.appendChild(layoutElementDiv);
</script>