from dash import html,dcc
import dash_bootstrap_components as dbc

def layout():
    return dbc.Container(fluid=True, children=[
        dbc.Row(justify="center", children=[
            dbc.Col(lg=8, children=[
                html.H1(children="Achat de métaux précieux physique: les fondamentaux", className="display-4 text-center mb-4 fw-bold"),
                html.P(children="""Le marché des métaux précieux, englobant l'or, l'argent, le platine et le
                palladium, offre un paysage d'investissement unique aux investisseurs avertis. Bien que
                souvent présentés comme une valeur refuge et une protection contre l'inflation, naviguer sur
                ce marché exige une compréhension nuancée de ses complexités.""", className="lead text-center"),

                html.H2(children="I. S'approvisionner en métaux précieux : Professionnels vs. Particuliers vs. Places de marché en ligne", className="display-6 mt-5 mb-4"),
                html.P(children="""Une décision fondamentale pour tout investisseur en métaux précieux est de
                savoir où les acquérir. Chaque source - négociants professionnels, particuliers et
                places de marché en ligne - présente ses propres avantages et inconvénients, exigeant un examen attentif.""",
                       className="lead"),

                html.H3(children="Négociants professionnels", className="display-7 mt-4 mb-3"),

                html.H4(children="- Avantages -", className="mb-3 text-center"),
                html.Ul(className="list-unstyled", children=[
                    html.Li(children=[
                        html.Span("Authenticité et fiabilité : ", className="fw-bold"),
                        """Les négociants réputés garantissent l'authenticité de leurs produits, atténuant
                        drastiquement le risque de contrefaçons. Les professionnels sont eux même
                        exposés à ce risque: cette concurrence déloyale des «faux»
                        est devenue une préoccupation majeure sur le marché des métaux
                        précieux. Ils fournissent souvent des certificats d'authenticité et
                        des informations détaillées sur les produits, renforçant la
                        transparence et la confiance. Les négociants établis ont une
                        réputation à défendre et sont incités à maintenir des normes
                        élevées. Certains professionnels vont même jusqu’à frapper leur
                        propre pièce afin d’y ajouter une empreinte difficilement
                        falsifiable et/ou s’appuient sur une technologie de type blockchain
                        afin d’enregistrer la transaction et limiter le risque de
                        falsification informatique."""
                    ]),
                    html.Li(className="mt-3", children=[
                        html.Span("Gamme de produits et services : ", className="fw-bold"),
                        """Les négociants professionnels offrent généralement une sélection diversifiée de
                        produits en lingots et des pièces, avec des stocks plus élevés que chez les particulier,
                        de différentes tailles et poids. Ils peuvent également fournir des
                        services supplémentaires tels que le stockage sécurisé, des
                        programmes de rachat et des conseils d'experts. 
                        Ils s'occupent souvent pour vous de faire la déclaration à l'administration fiscale. C'est un point qui est toujours à vérifier avant l'achat ou la vente de métaux précieux."""
                    ]),
                    html.Li(className="mt-3", children=[
                        html.Span("Recours juridique : ", className="fw-bold"),
                        """Les transactions avec des négociants professionnels sont généralement documentées
                        avec des factures et des reçus, offrant un recours juridique en cas de litige ou de
                        divergence. Ceci est crucial pour les déclarations fiscales, les réclamations
                        d'assurance, la gestion d’un héritage."""
                    ]),
                ]),

                html.H4(children="- Inconvénients -", className="mt-4 mb-3 text-center"),
                html.Ul(className="list-unstyled", children=[
                    html.Li(children=[
                        html.Span("Primes un peu plus élevées : ", className="fw-bold"),
                        """Les négociants professionnels facturent souvent des primes plus élevées que les
                        vendeurs privés ou les places de marché en ligne. Cela est dû à leurs frais
                        généraux, notamment la sécurité, l'assurance et le personnel."""
                    ]),
                    html.Li(className="mt-3", children=[
                        html.Span("Négociation limitée : ", className="fw-bold"),
                        """Les prix chez les négociants établis sont généralement fixes, laissant peu de place
                        à la négociation."""
                    ]),
                ]),

                html.H3(children="Particuliers", className="display-7 mt-4 mb-3"),

                html.H4(children="- Avantages", className="mb-3 text-center"),
                html.Ul(className="list-unstyled", children=[
                    html.Li(children=[
                        html.Span("Potentiel de prix plus bas : ", className="fw-bold"),
                        """Acheter auprès de particuliers, souvent par le biais de réseaux locaux ou de petites
                        annonces, peut permettre d'obtenir des primes plus basses que chez les négociants
                        professionnels. Les vendeurs peuvent être motivés à liquider rapidement leurs métaux précieux ou ne pas
                        être pleinement conscients de la valeur marchande actuelle. Leur annonces ne sont pas actualisées
                        en effet aussi régulièrement que chez un professionnel."""
                    ]),
                    html.Li(className="mt-3", children=[
                        html.Span("Possibilités de négociation : ", className="fw-bold"),
                        """Les transactions privées offrent une plus grande flexibilité pour la négociation,
                        permettant aux investisseurs de conclure de meilleures affaires."""
                    ]),
                    html.Li(className="mt-3", children=[
                        html.Span("Discrétion (avec réserves) : ", className="fw-bold"),
                        """Les ventes privées peuvent offrir un certain degré d'anonymat, bien que de plus en plus, les
                        gouvernements surveillent les sites de petites annonces en ligne et encouragent les transactions
                        traçables pour lutter contre le blanchiment d'argent."""
                    ]),
                ]),

                html.H4(children="- Inconvénients -", className="mt-4 mb-3 text-center"),
                html.Ul(className="list-unstyled", children=[
                    html.Li(children=[
                        html.Span("Limite de disponibilité : ", className="fw-bold"),
                        """Les particuliers ne possèdent souvent pas un stock important de pièces et vendent avec une taille de lot correspondant à leur besoin et non pas le vôtre."""
                    ]),
                    html.Li(children=[
                        html.Span("Risque accru de faux : ", className="fw-bold"),
                        """Le risque d'acquérir des produits contrefaits est considérablement plus élevé
                        lorsqu'on traite avec des particuliers. L'authentification devient la seule responsabilité de
                        l'acheteur."""
                    ]),
                    html.Li(className="mt-3", children=[
                        html.Span("Préoccupations en matière de sécurité : ", className="fw-bold"),
                        """Rencontrer des étrangers pour effectuer des transactions peut présenter des risques
                        pour la sécurité. Il est essentiel de privilégier la sécurité personnelle et de choisir des
                        lieux publics et bien éclairés pour les rencontres."""
                    ]),
                    html.Li(className="mt-3", children=[
                        html.Span("Recours limité : ", className="fw-bold"),
                        """Les transactions privées manquent souvent de documentation formelle, ce qui rend
                        difficile l'engagement de poursuites judiciaires en cas de fraude ou de litige."""
                    ]),
                ]),

                html.H3(children="Marketplace (eBay, Leboncoin)", className="display-7 mt-4 mb-3"),

                html.H4(children="- Avantages -", className="mb-3 text-center"),
                html.Ul(className="list-unstyled", children=[
                    html.Li(children=[
                        html.Span("Large sélection et comparaison des prix : ", className="fw-bold"),
                        """Les places de marché en ligne donnent accès à un vaste inventaire de métaux précieux
                        provenant de vendeurs du monde entier, permettant une comparaison complète des prix et
                        l'identification d'articles potentiellement sous-évalués."""
                    ]),
                    html.Li(className="mt-3", children=[
                        html.Span("Commodité : ", className="fw-bold"),
                        """Les plateformes en ligne offrent le confort de naviguer et d'acheter de n'importe où
                        avec une connexion Internet, éliminant le besoin de se déplacer ou de rencontrer des personnes
                        en personne."""
                    ]),
                    html.Li(className="mt-3", children=[
                        html.Span("Potentiel d'aubaines : ", className="fw-bold"),
                        """Les enchères en ligne ou les petites annonces peuvent générer des aubaines, en
                        particulier pour les pièces moins courantes ou en circulation."""
                    ]),
                ]),

                html.H4(children="- Inconvénients -", className="mt-4 mb-3 text-center"),
                html.Ul(className="list-unstyled", children=[
                    html.Li(children=[
                        html.Span("Risque élevé de contrefaçon : ", className="fw-bold mt-3"),
                        """Les places de marché en ligne regorgent de produits contrefaits, nécessitant une extrême
                        prudence et une authentification attentif. Les politiques de protection des acheteurs varient
                        d'une plateforme à l'autre et peuvent ne pas toujours offrir un recours adéquat."""
                    ]),
                    html.Li(className="mt-3", children=[
                        html.Span("Expédition et logistique : ", className="fw-bold"),
                        """Les frais d'expédition, l'assurance et les éventuels droits de douane peuvent ajouter
                        considérablement au coût total, en particulier pour les achats internationaux. Les retards de
                        livraison et les colis perdus sont des risques supplémentaires à prendre en compte."""
                    ]),
                    html.Li(className="mt-3", children=[
                        html.Span("Fiabilité du vendeur : ", className="fw-bold"),
                        """Évaluer la fiabilité et la réputation des vendeurs en ligne peut être difficile. Il est
                        crucial d'examiner attentivement les commentaires, les évaluations et les politiques de retour
                        des vendeurs avant d'effectuer un achat."""
                    ]),
                ]),

                html.H2(children="II. La prime : le B.A.-BA", className="display-6 mt-5 mb-4"),
                html.P(children="""Les primes, la différence entre le prix au comptant et le prix d'achat réel d'un produit
                en métal précieux, sont un facteur critique dans l'investissement dans les métaux précieux. Comprendre les variations
                de primes et savoir les utiliser peut avoir un impact significatif
                sur le rendement des investissements.""", className="lead"),

                html.H3(children="Calcul des primes", className="display-7 mt-4 mb-4"),
                html.Ul(className="list-unstyled mt-3", children=[
                    html.Li(children=[
                        html.Span("Formule de base : ", className="fw-bold"),
                        "Prime = (Prix d'achat - Cours du métal) / Cours du métal * 100"
                    ]),
                    html.Li(className="mt-3", children=[
                        html.Span("Facteurs affectant les primes : ", className="fw-bold"),
                        """La rareté, l'état, la demande, les coûts de production, la marge du négociant,
                        la tension du marché et même la taille et le type de produit (pièce vs. lingot) peuvent influencer
                        les primes."""
                    ]),
                    html.Li(className="mt-3", children=[
                        html.Span("Considérations : ", className="fw-bold"),
                        """Le prix au comptant fluctuant, les primes variables d'un négociant à l'autre et
                        la distinction entre les pièces de qualité investissement et les pièces de collection ajoutent de
                        la complexité aux calculs de prime. Par exemple, une pièce rare peut avoir une prime élevée mais
                        aussi avoir une valeur numismatique significative, qui doit être considérée séparément."""
                    ]),
                ]),

                html.H3(children="Comparaison des primes", className="display-7 mt-4 mb-3"),
                html.Ul(className="list-unstyled", children=[
                    html.Li(children=[
                        html.Span("Entre les produits : ", className="fw-bold mt-3"),
                        """La comparaison des primes entre différents produits (par exemple, pièce d'or de 1/10 oz
                        vs. lingot d'or de 1 oz) nécessite la conversion des primes en une unité commune, telle que la
                        prime par once de métal pur."""
                    ]),
                    html.Li(className="mt-3", children=[
                        html.Span("Entre les négociants : ", className="fw-bold"),
                        """Une comparaison minutieuse entre plusieurs négociants, en ligne et hors ligne, est
                        essentielle pour identifier les primes les plus compétitives. 
                        Bullion-sniper vous propose le comparatif des primes, des grandes plateformes en ligne, le plus complet de France."""
                    ]),
                    html.Li(className="mt-3", children=[
                        html.Span("Au fil du temps : ", className="fw-bold"),
                        """Le suivi des tendances des primes pour le même produit au fil du temps peut fournir des
                        informations sur la dynamique du marché et les opportunités potentielles d'achat ou de vente.
                        Des primes en hausse pourraient suggérer une augmentation de la demande ou de la rareté, tandis
                        que des primes en baisse pourraient indiquer un refroidissement du marché ou une offre
                        excédentaire."""
                    ]),
                ]),

                html.H3(children="Stratégies avancées", className="display-7 mt-4 mb-3"),
                html.Ul(className="list-unstyled", children=[
                    html.Li(children=[
                        html.Span("Se concentrer sur les faibles primes (avec réserves) : ", className="fw-bold"),
                        """En général, les investisseurs qui cherchent à maximiser leurs rendements devraient
                        privilégier les produits avec les primes les plus basses, en particulier pour les investissements
                        plus importants. Cependant, des primes excessivement basses pourraient soulever des inquiétudes
                        quant à l'authenticité, en particulier sur les places de marché en ligne ou les transactions
                        privées."""
                    ]),
                    html.Li(className="mt-3", children=[
                        html.Span("Tenir compte de la valeur numismatique : ", className="fw-bold"),
                        """Pour les pièces de collection, la prime reflète non seulement les coûts de production
                        mais aussi la valeur numismatique, qui peut fluctuer indépendamment du prix au comptant du métal.
                        Les collectionneurs tiennent compte de la rareté, de l'importance historique et de la
                        demande du marché lorsqu'ils évaluent les primes numismatiques."""
                    ]),
                    html.Li(className="mt-3", children=[
                        html.Span("Tenir compte de la TVA : ", className="fw-bold"),
                        """Dans certaines juridictions, la TVA est appliquée à certains produits en métaux précieux, ce
                        qui a un impact significatif sur le coût total. Les investisseurs doivent tenir compte de la TVA
                        lorsqu'ils comparent les prix et les primes, en particulier pour les lingots d'argent qui sont
                        souvent soumis à la TVA tandis que certaines pièces en sont exemptées."""
                    ]),
                ]),

                html.H2(children="III. Due diligence", className="display-6 mt-5 mb-4"),
                html.P(children="""Une analyse approfondie de chaque offre est essentielle pour atténuer les risques sur lors de l'achat de métaux précieux.
                Voici quelques points clés :""", className="lead"),

                html.Ul(className="list-unstyled", children=[
                    html.Li(children=[
                        html.Span("Vérifier la réputation du négociant : ", className="fw-bold"),
                        """Avant d'acheter auprès de n'importe quel négociant, en particulier en ligne ou auprès de vendeurs privés,
                        recherchez minutieusement sa réputation et sa légitimité. Consultez les avis en ligne, que le SIRET dans les mentions légales est toujours valide et les forums et pour obtenir des commentaires et des plaintes."""
                    ]),
                    html.Li(className="mt-3", children=[
                        html.Span("Authentifier les produits : ", className="fw-bold"),
                        """Utilisez plusieurs méthodes d'authentification lors de l'acquisition de métaux précieux, en particulier
                        lorsque vous traitez avec des vendeurs non professionnels. L'inspection visuelle, la vérification du poids et lorsque c'est possible,
                        les tests sonores, les tests magnétiques et les tests à l'acide (avec prudence) doivent être combinés pour
                        obtenir des résultats fiables. Pour les achats de plus grande valeur, des services d'authentification
                        professionnels peuvent être nécessaires."""
                    ]),
                    html.Li(className="mt-3", children=[
                        html.Span("Comprendre les spécifications du produit : ", className="fw-bold"),
                        """Vérifier la teneur en métal par année de frappe, l'état général (boursable ou non), le poids et toute les caractéristique
                        distinctive du produit. Comparez ces spécifications avec des sources réputées comme Numista ou les sites
                        web officiels des hôtels des monnaies."""
                    ]),
                    html.Li(className="mt-3", children=[
                        html.Span("Documents sécurisés : ", className="fw-bold"),
                        """Conservez tous les documents relatifs à vos achats, y compris les factures, les certificats
                        d'authenticité et les reçus d'expédition. Ceci est crucial pour les réclamations d'assurance, les déclarations
                        fiscales et la preuve de propriété."""
                    ]),
                    html.Li(className="mt-3", children=[
                        html.Span("Rester informé : ", className="fw-bold"),
                        """Surveillez continuellement les tendances du marché, les indicateurs économiques et les nouvelles
                        relatives au marché des métaux précieux. Abonnez-vous à des publications sectorielles réputées et suivez les
                        analyses d'experts pour anticiper les risques et opportunités potentiels."""
                    ]),
                ]),  # Close the html.Ul
            ]),  # Close the dbc.Col
        ]),  # Close the dbc.Row
    ])  # Close the dbc.Container