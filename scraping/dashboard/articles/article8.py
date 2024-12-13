from dash import html
from dash import dcc

def layout():
    return html.Div(children=[
    html.H1(children="Achat de métaux précieux physique: les notions de bases"),

    html.P(children="""Le marché des métaux précieux, englobant l'or, l'argent, le platine et le palladium, 
    offre un paysage d'investissement unique aux investisseurs avertis. Bien que souvent présentés comme une 
    valeur refuge et une protection contre l'inflation, naviguer sur ce marché exige une compréhension 
    nuancée de ses complexités."""),

    html.H2(children="I. S'approvisionner en métaux précieux : Professionnels vs. Particuliers vs. Places de marché en ligne"),

    html.P(children="""Une décision fondamentale pour tout investisseur en métaux précieux est de savoir où 
    acquérir ses actifs. Chaque source - négociants professionnels, particuliers et places de marché en 
    ligne - présente ses propres avantages et inconvénients, exigeant un examen attentif."""),

    html.H3(children="A. Négociants professionnels :"),

    html.Ul(children=[
        html.Li(children="""Authenticité et fiabilité : Les négociants réputés garantissent l'authenticité de 
        leurs produits, atténuant drastiquement le risque de contrefaçons. Les professionnels sont eux même 
        exposés à ce risque : cette concurrence déloyale des « faux » est devenue une préoccupation majeure 
        sur le marché des métaux précieux. Ils fournissent souvent des certificats d'authenticité et des 
        informations détaillées sur les produits, renforçant la transparence et la confiance. Les négociants 
        établis ont une réputation à défendre et sont incités à maintenir des normes élevées. Certains 
        professionnels vont même jusqu’à frapper leur propre pièce afin d’y ajouter une empreinte 
        difficilement falsifiable et/ou s’appuie sur une technologie de type blockchain afin d’enregistrer 
        la transaction et limiter le risque de falsification informatique."""),
        html.Li(children="""Gamme de produits et services : Les négociants professionnels offrent généralement 
        une sélection diversifiée de produits en lingots et des pièces, avec des stocks plus élevés que chez 
        les particulier, de différentes tailles et poids. Ils peuvent également fournir des services 
        supplémentaires tels que le stockage sécurisé, des programmes de rachat et des conseils d'experts."""),
        html.Li(children="""Recours juridique : Les transactions avec des négociants professionnels sont 
        généralement documentées avec des factures et des reçus, offrant un recours juridique en cas de 
        litige ou de divergence. Ceci est crucial pour les déclarations fiscales, les réclamations 
        d'assurance, la gestion d’un héritage.""")
    ]),

    html.Ul(children=[
        html.Li(children="""Primes un peu plus élevées : Les négociants professionnels facturent souvent des 
        primes plus élevées que les vendeurs privés ou les places de marché en ligne. Cela est dû à leurs 
        frais généraux, notamment la sécurité, l'assurance et le personnel."""),
        html.Li(children="""Négociation limitée : Les prix chez les négociants établis sont généralement 
        fixes, laissant peu de place à la négociation.""")
    ]),

    html.H3(children="B. Particuliers :"),

    html.Ul(children=[
        html.Li(children="""Potentiel de prix plus bas : Acheter auprès de particuliers, souvent par le biais 
        de réseaux locaux ou de petites annonces, peut permettre d'obtenir des prix et des primes plus bas 
        que chez les négociants professionnels. Les vendeurs peuvent être motivés à liquider rapidement 
        leurs actifs ou ne pas être pleinement conscients de la valeur marchande actuelle. Les annonces ne 
        sont pas actualisées en effet aussi régulièrement que chez un professionnel."""),
        html.Li(children="""Possibilités de négociation : Les transactions privées offrent une plus grande 
        flexibilité pour la négociation, permettant aux investisseurs avisés de conclure de meilleures 
        affaires."""),
        html.Li(children="""Discrétion (avec réserves) : Les ventes privées peuvent offrir un certain degré 
        d'anonymat, bien que de plus en plus, les gouvernements surveillent les sites de petites annonces en 
        ligne et encouragent les transactions traçables pour lutter contre le blanchiment d'argent.""")
    ]),

    html.Ul(children=[
        html.Li(children="""Risque accru de contrefaçons : Le risque d'acquérir des produits contrefaits est 
        considérablement plus élevé lorsqu'on traite avec des particuliers. L'authentification devient la 
        seule responsabilité de l'acheteur."""),
        html.Li(children="""Préoccupations en matière de sécurité : Rencontrer des étrangers pour effectuer 
        des transactions peut présenter des risques pour la sécurité. Il est essentiel de privilégier la 
        sécurité personnelle et de choisir des lieux publics et bien éclairés pour les rencontres."""),
        html.Li(children="""Recours limité : Les transactions privées manquent souvent de documentation 
        formelle, ce qui rend difficile l'engagement de poursuites judiciaires en cas de fraude ou de 
        litige.""")
    ]),

    html.H3(children="C. Places de marché en ligne (eBay, Leboncoin) :"),

    html.Ul(children=[
        html.Li(children="""Large sélection et comparaison des prix : Les places de marché en ligne donnent 
        accès à un vaste inventaire de métaux précieux provenant de vendeurs du monde entier, permettant une 
        comparaison complète des prix et l'identification d'articles potentiellement sous-évalués."""),
        html.Li(children="""Commodité : Les plateformes en ligne offrent la commodité de naviguer et d'acheter 
        de n'importe où avec une connexion Internet, éliminant le besoin de se déplacer ou de rencontrer des 
        personnes en personne."""),
        html.Li(children="""Potentiel d'aubaines : Les enchères en ligne ou les petites annonces peuvent 
        générer des aubaines, en particulier pour les pièces moins courantes ou en circulation.""")
    ]),

    html.Ul(children=[
        html.Li(children="""Risque élevé de contrefaçon : Les places de marché en ligne regorgent de 
        produits contrefaits, nécessitant une extrême prudence et une authentification diligente. Les 
        politiques de protection des acheteurs varient d'une plateforme à l'autre et peuvent ne pas toujours 
        offrir un recours adéquat."""),
        html.Li(children="""Expédition et logistique : Les frais d'expédition, l'assurance et les éventuels 
        droits de douane peuvent ajouter considérablement au coût total, en particulier pour les achats 
        internationaux. Les retards de livraison et les colis perdus sont des risques supplémentaires à 
        prendre en compte."""),
        html.Li(children="""Fiabilité du vendeur : Évaluer la fiabilité et la réputation des vendeurs en 
        ligne peut être difficile. Il est crucial d'examiner attentivement les commentaires, les évaluations 
        et les politiques de retour des vendeurs avant d'effectuer un achat.""")
    ]),
        html.H2(children="II. La prime : le B.A.-BA"),
        html.P(children="""Les primes, la différence entre le prix au comptant et le prix d'achat réel d'un produit en métal précieux, 
            sont un facteur critique dans l'investissement dans les métaux précieux. Comprendre les variations de primes et utiliser 
            des stratégies avancées pour calculer et comparer les primes peut avoir un impact significatif sur le rendement des 
            investissements."""),
        html.H3(children="A. Calcul des primes :"),
        html.Ul(children=[
            html.Li(
                children="Formule de base : Prime = (Prix d'achat - Valeur du métal fondu) / Valeur du métal fondu * 100"),
            html.Li(children="""Facteurs affectant les primes : La rareté, l'état, la demande, les coûts de production, la marge du 
                négociant, la tension du marché et même la taille et le type de produit (pièce vs. lingot) peuvent influencer les primes."""),
            html.Li(children="""Considérations avancées : Le prix au comptant fluctuant, les primes variables d'un négociant à l'autre 
                et la distinction entre les pièces de qualité investissement et les pièces de collection ajoutent de la complexité aux 
                calculs de prime. Par exemple, une pièce rare peut avoir une prime élevée mais aussi avoir une valeur numismatique 
                significative, qui doit être considérée séparément.""")
        ]),
        html.H3(children="B. Comparaison des primes :"),
        html.Ul(children=[
            html.Li(children="""Entre les produits : La comparaison des primes entre différents produits (par exemple, pièce d'or de 
                1/10 oz vs. lingot d'or de 1 oz) nécessite la conversion des primes en une unité commune, telle que la prime par once de 
                métal pur."""),
            html.Li(children="""Entre les négociants : Une comparaison minutieuse entre plusieurs négociants, en ligne et hors ligne, 
                est essentielle pour identifier les primes les plus compétitives."""),
            html.Li(children="""Au fil du temps : Le suivi des tendances des primes pour le même produit au fil du temps peut fournir des 
                informations sur la dynamique du marché et les opportunités potentielles d'achat ou de vente. Des primes en hausse 
                pourraient suggérer une augmentation de la demande ou de la rareté, tandis que des primes en baisse pourraient indiquer un 
                refroidissement du marché ou une offre excédentaire.""")
        ]),
        html.H3(children="C. Stratégies avancées :"),
        html.Ul(children=[
            html.Li(children="""Se concentrer sur les faibles primes (avec réserves) : En général, les investisseurs qui cherchent à 
                maximiser leurs rendements devraient privilégier les produits avec les primes les plus basses, en particulier pour les 
                investissements plus importants. Cependant, des primes excessivement basses pourraient soulever des inquiétudes quant à 
                l'authenticité, en particulier sur les places de marché en ligne ou les transactions privées."""),
            html.Li(children="""Tenir compte de la valeur numismatique : Pour les pièces de collection, la prime reflète non seulement 
                les coûts de production mais aussi la valeur numismatique, qui peut fluctuer indépendamment du prix au comptant du métal. 
                Les collectionneurs avertis tiennent compte de la rareté, de l'importance historique et de la demande du marché lorsqu'ils 
                évaluent les primes numismatiques."""),
            html.Li(children="""Tenir compte de la TVA : Dans certaines juridictions, la TVA est appliquée à certains produits en métaux 
                précieux, ce qui a un impact significatif sur le coût total. Les investisseurs doivent tenir compte de la TVA lorsqu'ils 
                comparent les prix et les primes, en particulier pour les lingots d'argent, qui sont souvent soumises à la TVA tandis que 
                certaines pièces en sont exemptées.""")
        ]),

        dcc.Tabs(id="articles-tabs", value='tab-1', children=[
            dcc.Tab(label='Le Platine', value='tab-1', children=[
                html.H2(children="III. Le platine : Une analyse détaillée pour les investisseurs avertis"),
                html.P(children="""Le platine, souvent éclipsé par l'or et l'argent, offre une proposition d'investissement unique avec son 
                propre ensemble de risques et de récompenses. Les investisseurs avertis doivent analyser attentivement ses utilisations 
                industrielles, la volatilité de son prix et ses perspectives à long terme."""),
                html.H3(children="A. Propriétés et rareté :"),
                html.Ul(children=[
                    html.Li(children="""Le platine est plus rare que l'or et possède des propriétés physiques et chimiques uniques, ce qui le rend 
                    très apprécié dans diverses applications industrielles. Sa densité et son point de fusion élevés rendent la contrefaçon 
                    extrêmement difficile.""")
                ]),
                html.H3(children="B. Demande industrielle et volatilité des prix :"),
                html.Ul(children=[
                    html.Li(children="""La majorité de la production de platine est consommée par des applications industrielles, en particulier 
                    les convertisseurs catalytiques des automobiles. Cela rend le prix du platine fortement dépendant de la demande industrielle et 
                    des cycles économiques. L'essor des véhicules électriques, qui ne nécessitent pas de convertisseurs catalytiques 
                    traditionnels, pose un défi important à la demande industrielle future de platine. Cette dépendance à un seul secteur 
                    contribue à la volatilité du prix du platine.""")
                ]),
                html.H3(children="C. Considérations d'investissement :"),
                html.Ul(children=[
                    html.Li(children="""Bien que le marché limité du platine et sa liquidité plus faible par rapport à l'or et à l'argent puissent 
                    rendre sa revente plus difficile, il peut constituer un outil de diversification. Ses propriétés uniques et ses applications 
                    futures potentielles dans les piles à combustible à hydrogène et d'autres technologies émergentes pourraient faire grimper 
                    son prix à long terme.""")
                ]),
                html.H3(children="D. Comparaison avec l'or et l'argent :"),
                html.Ul(children=[
                    html.Li(children="""L'or est principalement considéré comme une valeur refuge et une protection contre l'inflation, tandis que 
                    l'argent a des utilisations à la fois d'investissement et industrielles, ce qui le rend plus volatile que l'or. Le platine 
                    partage certaines similitudes avec les deux métaux, offrant une certaine protection contre l'incertitude économique tout en 
                    présentant des fluctuations de prix importantes en raison de sa demande industrielle. Le prix actuel du platine, plus bas que 
                    celui de l'or, pourrait présenter une opportunité d'achat pour les investisseurs ayant une tolérance au risque plus élevée et un 
                    horizon d'investissement à long terme.""")
                ])
            ]),
            dcc.Tab(label='Due Diligence', value='tab-2', children=[
                html.H2(children="IV. Due diligence"),
                html.P(children="""Une due diligence approfondie est essentielle pour atténuer les risques sur le marché des métaux précieux. 
                Voici quelques stratégies clés :"""),
                html.Ul(children=[
                    html.Li(children="""Vérifier la réputation du négociant : Avant d'acheter auprès de n'importe quel négociant, en 
                    particulier en ligne ou auprès de vendeurs privés, recherchez minutieusement sa réputation et sa légitimité. Consultez les 
                    avis en ligne, les forums et les associations professionnelles pour obtenir des commentaires et des plaintes."""),
                    html.Li(children="""Authentifier les produits : Utilisez plusieurs méthodes d'authentification lors de l'acquisition de 
                    métaux précieux, en particulier lorsque vous traitez avec des vendeurs non professionnels. L'inspection visuelle, la 
                    vérification du poids, les tests sonores, les tests magnétiques et les tests à l'acide (avec prudence) doivent être 
                    combinés pour obtenir des résultats fiables. Pour les achats de plus grande valeur, des services d'authentification 
                    professionnels peuvent être nécessaires."""),
                    html.Li(children="""Comprendre les spécifications du produit : Soyez pleinement conscient de la teneur en métal, de la 
                    pureté, du poids et de toute caractéristique distinctive du produit. Comparez ces spécifications avec des sources réputées 
                    comme Numista ou les sites web officiels des hôtels des monnaies."""),
                    html.Li(children="""Documents sécurisés : Conservez tous les documents relatifs à vos achats, y compris les factures, les 
                    certificats d'authenticité et les reçus d'expédition. Ceci est crucial pour les réclamations d'assurance, les déclarations 
                    fiscales et la preuve de propriété."""),
                    html.Li(children="""Rester informé : Surveillez continuellement les tendances du marché, les indicateurs économiques et 
                    les nouvelles relatives au marché des métaux précieux. Abonnez-vous à des publications sectorielles réputées et suivez les 
                    analyses d'experts pour anticiper les risques et opportunités potentiels.""")
                ])
            ]),
    ]),

    html.Div(id='tabs-content')
])