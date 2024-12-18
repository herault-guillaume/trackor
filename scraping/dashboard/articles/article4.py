from dash import html,dcc
import dash_bootstrap_components as dbc

data = [
    {
        "Pays": "France",
        "Métal": "Or d'investissement (pièces, lingots)",
        "Achat": "Exonéré de TVA",
        "Vente": "Taxe sur les métaux précieux (TMP) : 11,5% du prix de vente ou Taxe sur la plus-value (TPV) : 36,2% avec abattement de 5% par an après la 2ème année de détention",
        "Source": "Article 297 A du Code Général des Impôts BOI-RPPM-PVBMI-20-10-20-40"
    },
    {
        "Pays": "France",
        "Métal": "Argent d'investissement (pièces)",
        "Achat": "Exonéré de TVA",
        "Vente": "Taxe sur les métaux précieux (TMP) : 11,5% du prix de vente ou Taxe sur la plus-value (TPV) : 36,2% avec abattement de 5% par an après la 2ème année de détention",
        "Source": "Article 297 A du Code Général des Impôts BOI-RPPM-PVBMI-20-10-20-40"
    },
    {
        "Pays": "France",
        "Métal": "Lingots d'argent",
        "Achat": "TVA 20%",
        "Vente": "Taxe sur les métaux précieux (TMP) : 11,5% du prix de vente ou Impôt sur la plus-value (IR) : 36,2% avec abattement de 5% par an après la 2ème année de détention",
        "Source": "Article 297 A du Code Général des Impôts BOI-RPPM-PVBMI-20-10-20-40"
    },
    {
        "Pays": "Belgique",
        "Métal": "Or d'investissement",
        "Achat": "Pas de TMP ni de TVA",
        "Vente": "Pas de TMP ni de TVA",
        "Source": "Administration Générale des Douanes et Accises belge"
    },
    {
        "Pays": "Belgique",
        "Métal": "Argent",
        "Achat": "TVA 21%",
        "Vente": "TVA 21%",
        "Source": "Administration Générale des Douanes et Accises belge"
    },
    {
        "Pays": "Allemagne",
        "Métal": "Or d'investissement",
        "Achat": "Pas de TMP",
        "Vente": "Pas de TMP",
        "Source": "Ministère fédéral des Finances allemand"
    },
    {
        "Pays": "Allemagne",
        "Métal": "Argent",
        "Achat": "TVA 19%",
        "Vente": "TVA 19%",
        "Source": "Ministère fédéral des Finances allemand"
    },
    {
        "Pays": "Italie",
        "Métal": "Or et argent",
        "Achat": "TVA 22%",
        "Vente": "Taxe sur les plus-values de 26% pour les particuliers",
        "Source": "Agence des revenus italienne"
    },
    {
        "Pays": "Espagne",
        "Métal": "Or et argent",
        "Achat": "TVA 21%",
        "Vente": "Taxe sur les plus-values de 19% à 23% selon le montant du gain",
        "Source": "Agence fiscale espagnole"
    },
    {
        "Pays": "Suisse",
        "Métal": "Or d'investissement",
        "Achat": "Pas de TMP ni de TVA",
        "Vente": "Pas de TMP ni de TVA",
        "Source": "Administration fédérale des contributions suisse"
    },
    {
        "Pays": "Suisse",
        "Métal": "Argent",
        "Achat": "TVA 7,7%",
        "Vente": "TVA 7,7%",
        "Source": "Administration fédérale des contributions suisse"
    },
    {
        "Pays": "Royaume-Uni",
        "Métal": "Or d'investissement",
        "Achat": "Pas de TMP",
        "Vente": "Capital Gains Tax (impôt sur les plus-values) sur les plus-values réalisées lors de la vente d'or, avec des exemptions et des abattements possibles",
        "Source": "Her Majesty's Revenue and Customs (HMRC)"
    },
    {
        "Pays": "Royaume-Uni",
        "Métal": "Argent",
        "Achat": "TVA 20%",
        "Vente": "TVA 20%",
        "Source": "Her Majesty's Revenue and Customs (HMRC)"
    }
]

def layout():
    return dbc.Container(fluid=True, children=[
        dbc.Row(justify="center", children=[
            dbc.Col(lg=9, children=[
                html.H1("Fiscalité et réglementations en métaux précieux", className="display-4 text-center mb-4 fw-bold"),

                html.P(
                    "Investir dans les métaux précieux, bien qu'offrant des avantages potentiels tels que la diversification de portefeuille et une protection contre l'inflation, implique de naviguer dans un paysage complexe de réglementations fiscales. Ces réglementations varient considérablement selon les juridictions et peuvent avoir un impact profond sur le rendement des investissements. Cet article propose une analyse complète des stratégies d'optimisation fiscale pour les investisseurs en métaux précieux, en se concentrant principalement sur le système fiscal français tout en abordant les considérations internationales et les pièges courants à éviter. Ce guide s'adresse aux investisseurs cherchant à minimiser leur charge fiscale et à maximiser leurs rendements après impôts.",
                    className="lead"
                ),

                dbc.Card(
                    dbc.CardHeader(
                        html.P(
                            "Avertissement : Cet article est fourni à titre informatif seulement et ne constitue pas un conseil financier ou fiscal. Consultez un professionnel qualifié pour obtenir des conseils personnalisés.")
                    ),
                    color="warning",  # Use Bootstrap's "warning" color for gold
                    outline=True  # Set outline to True for a more subtle look
                ),
                html.H2("I. Implications fiscales des métaux précieux en France", className="display-6 mt-5 mb-4 fw-bold"),

                html.P(
                    "Le système fiscal français applique des règles spécifiques à la cession de métaux précieux, notamment l'impôt sur les plus-values, la taxe sur la valeur ajoutée (TVA) et certaines exemptions. La compréhension de ces règles est essentielle pour prendre des décisions d'investissement éclairées."
                ),

                html.H3("Taxe sur les métaux précieux (11,5 %)", className="display-7 mt-4 mb-3 fw-bold"),

                html.Ul([
                    html.Li(
                        ["La taxe standard appliquée à la cession de métaux précieux en France est de 11,5 % de la valeur totale de la transaction. Cette taxe s'applique indépendamment du fait que la vente génère un profit ou une perte, ce qui peut impacter le rendement global de l'investissement, en particulier pour les détenteurs à court terme ou ceux qui vendent lors de baisses de marché. Si vous ne passez pas par un vendeur professionnel, il sera néccessaire de remplir et envoyer à l'administration fiscale le ",
                         html.A(
                             "Formulaire n° 2091-SD.",  # Text to display for the link
                             href="https://www.impots.gouv.fr/portail/files/formulaires/2091-sd/2020/2091-sd_2976.pdf",
                             # The URL
                             target="_blank"  # Open the link in a new tab
                         ),]
                    ),

                    html.Li(className="mt-3", children=[
                        html.Span("Avantage : ", className="fw-bold"),
                        "Voir graphique ci dessous. Applicable par exemple dans le cas d'une facture perdue ou d'un scellé ouvert.",
                    ]),
                    html.Li(className="mt-3", children=[
                        html.Span("Inconvénient : ", className="fw-bold"),
                        "Les moins-values sont aussi imposables.",
                    ]),
                ], className="list-unstyled"),

                html.H3("Impôt sur les plus-values (36,2 % avec abattements)", className="display-7 mt-4 mb-3 fw-bold"),

                html.Ul([
                    html.Li([
                        "Alternativement à la taxe de 11,5 %, les investisseurs peuvent opter pour le régime de l'impôt sur les plus-values. Ce régime applique un impôt d'environ 36,2 % sur la plus-value réalisée, plutôt que sur le montant total de la vente. Si vous ne passez pas par un vendeur professionnel, il sera néccessaire de remplir et envoyer à l'administration fiscale le ",
                        html.A(
                            "Formulaire n° 2092-SD.",  # Text to display for the link
                            href="https://www.impots.gouv.fr/sites/default/files/formulaires/2092-sd/2020/2092-sd_1662.pdf",
                            # The URL
                            target="_blank"  # Open the link in a new tab
                        ), ]
                    ),
                    html.Li(className="mt-3", children=[
                        html.Span("Avantages : ", className="fw-bold"),
                        "Le régime de l'impôt sur les plus-values comprend un abattement annuel de 5 % à partir de la 3ème année de détention. Cet abattement réduit efficacement la plus-value imposable, diminuant ainsi la charge fiscale globale. Il n'y a également aucune taxe en cas de moins-value.",
                    ]),
                    html.Li(className="mt-3", children=[
                        html.Span("Inconvénient : ", className="fw-bold"),
                        "Une longue période de conservation ou des gains importants sont néccessaires pour que cette taxation devienne intéressante (voir graphique ci dessous).",
                    ]),
                ], className="list-unstyled"),

                dbc.Row([
                    dbc.Col([
                        dbc.Label("Montant total (€)", html_for="total-amount"),
                        dbc.Input(type="number", id="total-amount", value=1500),
                    ], className="mb-3", width=6),  # Add width=6 to each Col

                    dbc.Col([
                        dbc.Label("Rendement annuel (%)", html_for="annual-yield"),
                        dbc.Input(type="number", id="annual-yield", value=10),
                    ], className="mb-3", width=6),  # Add width=6 to each Col
                ],className="mt-5"),

                dcc.Graph(id="tax-comparison-graph"),

                html.H3("Taxe sur la valeur ajoutée (TVA)", className="display-7 mt-4 mb-3 fw-bold"),

                html.Ul([
                    html.Li(
                        "Les lingots d'argent, considérés comme des matières premières industrielles en France, sont soumis à une TVA de 20 %. Cela augmente considérablement le coût d'investissement initial et impacte les rendements potentiels. C'est un facteur crucial à prendre en compte lors de la comparaison des lingots d'argent avec d'autres options d'investissement."
                    ),
                    html.Li(className="mt-3", children=[
                        html.Span("Exemption clé : ", className="fw-bold"),
                        "Les pièces d'argent ayant cours légal sont exemptées de TVA en France. Cette exemption les rend plus attrayantes pour les investisseurs par rapport aux lingots d'argent, permettant une acquisition d'argent physique plus rentable. L'or d'investissement est généralement également exempté de TVA.",
                    ]),
                ], className="list-unstyled"),

                html.Ul([
                    html.Li(
                        "Les lingots d'argent, considérés comme des matières premières industrielles en France, sont soumis à une TVA de 20 %. Cela augmente considérablement le coût d'investissement initial et impacte les rendements potentiels. C'est un facteur crucial à prendre en compte lors de la comparaison des lingots d'argent avec d'autres options d'investissement."
                    ),
                    html.Li(className="mt-3", children=[
                        html.Span("Exemption clé : ", className="fw-bold"),
                        "Les pièces d'argent ayant cours légal sont exemptées de TVA en France. Cette exemption les rend plus attrayantes pour les investisseurs par rapport aux lingots d'argent, permettant une acquisition d'argent physique plus rentable. L'or d'investissement est généralement également exempté de TVA et les objets en or destinés à la fonte sont totalement exonérés de taxe en France.",
                    ]),
                ], className="list-unstyled"),

                html.H2("II. Cours légal et fiscalité : Pièces démonétisées, pièces ayant cours légal et jetons",
                        className="display-6 mt-5 mb-4 fw-bold"),

                html.P(
                    "Le cours légal d'une pièce joue un rôle important dans la détermination de son traitement fiscal en France."
                ),

                html.H3("Pièces démonétisées", className="display-7 mt-4 mb-3 fw-bold"),

                html.Ul([
                    html.Li(
                        "Les pièces démonétisées, telles que la pièce d'or Napoléon française ou la pièce d'argent Hercule de 50 francs, n'ont plus cours légal et sont considérées comme des objets en métaux précieux. À ce titre, elles sont soumises à la TMP ou TPV lors de leur revente, même si elles ont déjà circulé comme monnaie."
                    ),
                ], className="list-unstyled"),

                html.H3("Pièces ayant cours légal", className="display-7 mt-4 mb-3 fw-bold"),

                html.Ul([
                    html.Li(
                        "Les pièces ayant actuellement cours légal, telles que la pièce d'or Philharmonique de Vienne ou les monnaies en € de diverses formes frappées par la Monnaie de Paris, sont considérées comme des biens meubles en droit français. La revente de ces pièces est exonérée d'impôt jusqu'à une limite de 5000 € par transaction. Cette exemption peut être très avantageuse pour les investisseurs, notamment pour gérer les liquidités ou effectuer des transactions plus petites et régulières."
                    ),
                ], className="list-unstyled"),

                html.H3("Jetons",
                        className="display-7 mt-4 mb-3 fw-bold"),

                html.Ul([
                    html.Li(
                        "Les jetons tels que les refrappes 20 francs suisse Vreneli ou refrappes 20 francs Marianne Coq dites 'Pinnay' sont rarement exonérées d'impôt en France. Il existe plusieurs interprétations quant à leur fiscalité. Elles peuvent être considérées comme 'pièces d'investissement' par un inspecteur des impôts même si elles n'ont jamais eu un cours légal et n'ont donc pas pu être démonétisées. La majorité des professionels appliquent la TMP ou la TVP. Vous pouvez demander à votre centre des impôts comment sont considérées spécifiquement vos jetons (par rescrit fiscal) mais il existe bien une pluralité de réponses."
                        "Les autres jetons ne ressemblant pas à des pièces ayant eu cours légal sont exemptés de taxe jusqu'à 5000€. Au delà, c'est la TMP ou TPV qui s'applique."

                    ),
                ], className="list-unstyled"),

                html.H2("III. Stratégies de minimisation fiscale", className="display-6 mt-5 mb-4 fw-bold"),

                html.P(
                    "Les investisseurs peuvent employer diverses stratégies pour minimiser leur charge fiscale lors de la cession de métaux précieux."
                ),

                html.H3("Factures et preuves d'achat", className="display-7 mt-4 mb-3 fw-bold"),

                html.Ul([
                    html.Li(
                        "Conserver la facture originale ou une preuve d'achat auprès d'un vendeur réputé est essentiel pour opter pour le régime de l'impôt sur les plus-values. Cette documentation permet aux investisseurs de justifier le prix d'achat initial et de calculer la plus-value réelle, qui est ensuite soumise au taux d'imposition plus bas sur les plus-values (TPV) au lieu de la taxe standard de 11,5 % sur le montant total de la vente (TMP)."
                    ),
                ], className="list-unstyled"),

                html.H3("Emballage scellé", className="display-7 mt-4 mb-3 fw-bold"),

                html.Ul([
                    html.Li(
                        "En France, les produits scellés non ouverts accompagnés d'une facture avec numéro de scellés correspondant bénéficient d'un traitement fiscal plus favorable dans le cadre du régime des plus-values, notamment l'abattement annuel de 5 % après la deuxième année (TPV)."
                    ),
                ], className="list-unstyled"),

                html.H2("IV. Considérations fiscales internationales", className="display-6 mt-5 mb-4 fw-bold"),

                html.P(
                    "Les lois fiscales varient considérablement d'une juridiction à l'autre, cependant vous devez toujours régler la taxe française TMP ou TPV si vous êtes résidant fiscal français."
                ),

                html.H2("V. Pièges fiscaux courants à éviter", className="display-6 mt-5 mb-4 fw-bold"),

                html.P(
                    "Être conscient des pièges potentiels peut éviter aux investisseurs des coûts et des soucis importants."
                ),

                html.H3("Mauvaise identification des jetons", className="display-7 mt-4 mb-3 fw-bold"),

                html.Ul([
                    html.Li(
                        "S'assurer d'identifier correctement les jetons et de les différencier des pièces démonétisées. Ceci est crucial pour appliquer le traitement fiscal correct et éviter d'éventuels litiges avec l'administration fiscale. Effectuer des recherches et consulter des experts en cas d'incertitude."
                    ),
                ], className="list-unstyled"),

                html.H3("Documentation inadéquate", className="display-7 mt-4 mb-3 fw-bold"),

                html.Ul([
                    html.Li(
                        "Conserver méticuleusement tous les justificatifs d'achat, y compris les factures, les certificats et les confirmations de paiement. Cette documentation est essentielle pour les déclarations fiscales et la minimisation des obligations fiscales potentielles."
                    ),
                ], className="list-unstyled"),

                html.H3("Négliger les implications internationales", className="display-7 mt-4 mb-3 fw-bold"),

                html.Ul([
                    html.Li(
                        "Pour les investisseurs détenant des actifs ou réalisant des transactions dans plusieurs pays, les considérations fiscales internationales peuvent être complexes. Demander conseil à un spécialiste fiscal international qualifié pour comprendre les implications transfrontalières, les conventions fiscales et les obligations déclaratives."
                    ),
                ], className="list-unstyled"),

            ]),  # Close the dbc.Col
        ]),  # Close the dbc.Row
    ])  # Close the dbc.Container