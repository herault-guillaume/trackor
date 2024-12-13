from dash import html,dcc
import dash_bootstrap_components as dbc


def layout():
    return dbc.Container(fluid=True, children=[
        dbc.Row(justify="center", children=[
            dbc.Col(lg=10, children=[
                html.H1("Optimisation fiscale pour les investisseurs en métaux précieux : Guide pour naviguer dans les réglementations complexes", className="display-4 text-center mb-4 fw-bold"),

                html.P(
                    "Investir dans les métaux précieux, bien qu'offrant des avantages potentiels tels que la diversification de portefeuille et une protection contre l'inflation, implique de naviguer dans un paysage complexe de réglementations fiscales. Ces réglementations varient considérablement selon les juridictions et peuvent avoir un impact profond sur le rendement des investissements. Cet article propose une analyse complète des stratégies d'optimisation fiscale pour les investisseurs en métaux précieux, en se concentrant principalement sur le système fiscal français tout en abordant les considérations internationales et les pièges courants à éviter. Ce guide s'adresse aux investisseurs avertis cherchant à minimiser leur charge fiscale et à maximiser leurs rendements après impôts.",
                    className="lead"
                ),

                html.P("Avertissement : Cet article est fourni à titre informatif seulement et ne constitue pas un conseil financier ou fiscal. Consultez un professionnel qualifié pour obtenir des conseils personnalisés."),

                html.H2("Implications fiscales des métaux précieux en France : Un aperçu complet", className="display-6 mt-5 mb-4 fw-bold"),

                html.P(
                    "Le système fiscal français applique des règles spécifiques à la cession de métaux précieux, notamment l'impôt sur les plus-values, la taxe sur la valeur ajoutée (TVA) et certaines exemptions. La compréhension de ces règles est essentielle pour prendre des décisions d'investissement éclairées."
                ),

                html.H3("Taxe sur les métaux précieux (11,5 %)", className="display-7 mt-4 mb-3 fw-bold"),

                html.Ul([
                    html.Li(
                        "La taxe standard appliquée à la cession de métaux précieux en France est de 11,5 % de la valeur totale de la transaction. Cette taxe s'applique indépendamment du fait que la vente génère un profit ou une perte, ce qui peut impacter le rendement global de l'investissement, en particulier pour les détenteurs à court terme ou ceux qui vendent lors de baisses de marché."
                    ),
                ], className="list-unstyled"),

                html.H3("Impôt sur les plus-values (36,2 % avec abattements)", className="display-7 mt-4 mb-3 fw-bold"),

                html.Ul([
                    html.Li(
                        "Alternativement à la taxe de 11,5 %, les investisseurs peuvent opter pour le régime de l'impôt sur les plus-values. Ce régime applique un impôt d'environ 36,2 % sur la plus-value réalisée, plutôt que sur le montant total de la vente. Cela peut être avantageux pour les investisseurs qui détiennent leurs métaux précieux depuis une période prolongée et ont accumulé des gains importants."
                    ),
                    html.Li(
                        "Avantage clé : Le régime de l'impôt sur les plus-values comprend un abattement annuel de 5 % après la deuxième année de détention. Cet abattement réduit efficacement la plus-value imposable, diminuant ainsi la charge fiscale globale.",
                        className="mt-3"
                    ),
                ], className="list-unstyled"),

                html.H3("Taxe sur la valeur ajoutée (TVA)", className="display-7 mt-4 mb-3 fw-bold"),

                html.Ul([
                    html.Li(
                        "Les lingots d'argent, considérés comme des matières premières industrielles en France, sont soumis à une TVA de 20 %. Cela augmente considérablement le coût d'investissement initial et impacte les rendements potentiels. C'est un facteur crucial à prendre en compte lors de la comparaison des lingots d'argent avec d'autres options d'investissement."
                    ),
                    html.Li(
                        "Exemption clé : Les pièces d'argent ayant cours légal sont exemptées de TVA en France. Cette exemption les rend plus attrayantes pour les investisseurs par rapport aux lingots d'argent, permettant une acquisition d'argent physique plus rentable. L'or d'investissement est généralement également exempté de TVA.",
                        className="mt-3"
                    ),
                ], className="list-unstyled"),

                html.H2("Cours légal et fiscalité : Pièces démonétisées, pièces ayant cours légal et jetons",
                        className="display-6 mt-5 mb-4 fw-bold"),

                html.P(
                    "Le cours légal d'une pièce joue un rôle important dans la détermination de son traitement fiscal en France."
                ),

                html.H3("Pièces démonétisées (« Piège Napoléon »)", className="display-7 mt-4 mb-3 fw-bold"),

                html.Ul([
                    html.Li(
                        "Les pièces démonétisées, telles que la pièce d'or Napoléon française ou la pièce d'argent Hercule de 50 francs, n'ont plus cours légal et sont considérées comme des objets en métaux précieux. À ce titre, elles sont soumises à la taxe standard de 11,5 % sur les métaux précieux lors de leur revente, même si elles ont déjà circulé comme monnaie."
                    ),
                    html.Li(
                        "Le « piège Napoléon » fait référence à l'idée fausse répandue selon laquelle les pièces Napoléon, en raison de leur importance historique et de leur large reconnaissance, seraient exemptées de cette taxe. Les investisseurs doivent être conscients de ce piège potentiel lorsqu'ils envisagent les pièces Napoléon comme un investissement.",
                        className="mt-3"
                    ),
                ], className="list-unstyled"),

                html.H3("Pièces ayant cours légal", className="display-7 mt-4 mb-3 fw-bold"),

                html.Ul([
                    html.Li(
                        "Les pièces ayant actuellement cours légal, telles que la pièce d'or Philharmonique de Vienne ou le Souverain britannique, sont considérées comme des biens meubles en droit français. La revente de ces pièces est exonérée d'impôt jusqu'à une limite de 5 000 € par transaction. Cette exemption peut être très avantageuse pour les investisseurs, notamment pour gérer les liquidités ou effectuer des transactions plus petites et régulières."
                    ),
                ], className="list-unstyled"),

                html.H3("Jetons (par exemple, refrappes de 20 francs suisses)",
                        className="display-7 mt-4 mb-3 fw-bold"),

                html.Ul([
                    html.Li(
                        "Les jetons, tels que les refrappes de la pièce d'or suisse de 20 francs, ressemblent à des pièces mais n'ont jamais eu de cours légal officiel. Cependant, en vertu du droit fiscal français, ils entrent dans la même catégorie que les bijoux et sont exonérés d'impôt jusqu'à une limite de 5 000 € par transaction. Cela rend certains jetons spécifiques fiscalement avantageux pour les investisseurs, en particulier ceux qui cherchent à diversifier leurs avoirs en or."
                    ),
                ], className="list-unstyled"),

                html.H2("Stratégies avancées de minimisation fiscale", className="display-6 mt-5 mb-4 fw-bold"),

                html.P(
                    "Les investisseurs avisés peuvent employer diverses stratégies pour minimiser leur charge fiscale lors de la cession de métaux précieux."
                ),

                html.H3("Factures et preuves d'achat", className="display-7 mt-4 mb-3 fw-bold"),

                html.Ul([
                    html.Li(
                        "Conserver la facture originale ou une preuve d'achat auprès d'un vendeur réputé est essentiel pour opter pour le régime de l'impôt sur les plus-values. Cette documentation permet aux investisseurs de justifier le prix d'achat initial et de calculer la plus-value réelle, qui est ensuite soumise au taux d'imposition plus bas sur les plus-values (36,2 %) au lieu de la taxe standard de 11,5 % sur le montant total de la vente."
                    ),
                ], className="list-unstyled"),

                html.H3("Emballage scellé", className="display-7 mt-4 mb-3 fw-bold"),

                html.Ul([
                    html.Li(
                        "Conserver les produits en métaux précieux dans leur emballage d'origine scellé peut encore améliorer les avantages fiscaux. En France, les produits scellés non ouverts accompagnés d'une facture valide bénéficient d'un traitement fiscal plus favorable dans le cadre du régime des plus-values, y compris le précieux abattement annuel de 5 % après la deuxième année."
                    ),
                ], className="list-unstyled"),

                html.H3("Comprendre les niches fiscales", className="display-7 mt-4 mb-3 fw-bold"),

                html.Ul([
                    html.Li(
                        "Les investisseurs doivent se tenir informés des lois et réglementations fiscales en vigueur concernant les métaux précieux. Les changements législatifs peuvent créer des opportunités ou supprimer des niches fiscales. Consulter un conseiller fiscal spécialisé dans les actifs d'investissement peut fournir des informations précieuses pour naviguer dans les réglementations complexes et maximiser l'efficacité fiscale."
                    ),
                ], className="list-unstyled"),

                html.H2("Considérations fiscales internationales", className="display-6 mt-5 mb-4 fw-bold"),

                html.P(
                    "Les lois fiscales varient considérablement d'une juridiction à l'autre, ce qui a une incidence sur la façon dont les bénéfices des cessions de métaux précieux sont traités."
                ),

                html.P(
                    "(Développer cette section avec des exemples spécifiques comparant les lois fiscales françaises avec celles d'autres pays pertinents pour votre public cible, par exemple, le Royaume-Uni, les États-Unis, l'Allemagne. Prendre en compte des aspects tels que les impôts sur les plus-values, la TVA/taxe sur les ventes, les obligations déclaratives et toutes exemptions ou réglementations spécifiques.)"
                ),

                html.Ul([
                    html.Li(
                        "États-Unis : Aborder brièvement les impôts sur les plus-values des métaux précieux, en distinguant les détentions à long terme et à court terme. Mentionner les implications fiscales des comptes d'épargne-retraite en or (Gold IRA)."
                    ),
                    html.Li(
                        "Royaume-Uni : Aborder l'impôt sur les plus-values (Capital Gains Tax) sur les métaux précieux, en mentionnant les exemptions et abattements potentiels. Discuter brièvement de la TVA sur l'argent et l'or.",
                        className="mt-3"
                    ),
                    html.Li(
                        "Allemagne : Aborder brièvement le traitement fiscal des métaux précieux, y compris la TVA sur les lingots d'argent et les exemptions potentielles pour l'or d'investissement.",
                        className="mt-3"
                    ),
                ], className="list-unstyled"),

            ]),  # Close the dbc.Col
        ]),  # Close the dbc.Row
    ])  # Close the dbc.Container
