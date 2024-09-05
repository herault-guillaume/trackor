<script>function generateTable() {
  const tableData = [
    {
      lieu: "En ligne - Professionnel",
      avantages: ["Large choix de pièces", "Facilité de comparaison des prix", "Avis clients disponibles"],
      inconvenients: ["Impossibilité d'examiner les pièces physiquement avant l'achat", "Délais de livraison", "Frais de port éventuels"]
    },
    {
      lieu: "En ligne - Particulier",
      avantages: ["Prix potentiellement plus bas", "Accès à des pièces rares ou insolites", "Transactions plus discrètes"],
      inconvenients: ["Risque d'arnaques ou de fausses pièces", "Difficulté à évaluer l'authenticité", "Frais de port et risques liés à l'envoi postal"]
    },
    {
      lieu: "En boutique - Professionnel",
      avantages: ["Expertise et conseils personnalisés", "Garantie d'authenticité", "Possibilité de négocier (parfois)"],
      inconvenients: ["Prix généralement plus élevés", "Moins de discrétion (transactions traçables)", "Stock potentiellement limité en boutique physique"]
    },
    {
      lieu: "En boutique - Particulier",
      avantages: ["Examen direct des pièces", "Possibilité de négocier le prix", "Échange direct avec le vendeur"],
      inconvenients: ["Choix limité", "Nécessité de se déplacer", "Risque de tomber sur un vendeur malhonnête"]
    }
  ];

  const tableContainer = document.getElementById('tableContainer');
  const table = document.createElement('table');
  table.classList.add('professional-table');


  // En-tête du tableau
  const headerRow = table.insertRow();
  ['Lieu d\'achat/Type de vendeur', 'Avantages', 'Inconvénients'].forEach(headerText => {
    const th = document.createElement('th');
    th.textContent = headerText;
    headerRow.appendChild(th);
  });

  // Lignes du tableau
  tableData.forEach(rowData => {
    const row = table.insertRow();
    const lieuCell = row.insertCell();
    lieuCell.textContent = rowData.lieu;

    ['avantages', 'inconvenients'].forEach(colData => {
      const cell = row.insertCell();
      const ul = document.createElement('ul');
      rowData[colData].forEach(item => {
        const li = document.createElement('li');
        li.textContent = item;
        ul.appendChild(li);
      });
      cell.appendChild(ul);
    });
  });

  // Appliquer le style directement avec JavaScript
  table.style.color = 'white';
  table.style.fontFamily = 'Lora, serif';
  table.style.borderCollapse = 'collapse';
  table.style.width = '100%';

  // Appliquer le style aux en-têtes (<th>)
  const tableHeaders = table.querySelectorAll('th');
  tableHeaders.forEach(th => {
    th.style.backgroundColor = '#333';
    th.style.padding = '12px';
    th.style.textAlign = 'left';
    th.style.border = '1px solid white';
    th.style.color = 'white';
  });

  // Appliquer le style aux cellules de données (<td>)
  const tableCells = table.querySelectorAll('td');
  tableCells.forEach(td => {
    td.style.padding = '12px';
    td.style.border = '1px solid white';
  });

  // Appliquer le style aux listes à puces (ul)
  const unorderedLists = table.querySelectorAll('ul');
  unorderedLists.forEach(ul => {
    ul.style.listStyle = 'disc';
    ul.style.paddingLeft = '20px';
  });

  tableContainer.appendChild(table);
}

// Appeler la fonction pour générer le tableau
generateTable();</script>