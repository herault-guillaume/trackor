from dash import html, dcc
import dash_bootstrap_components as dbc

def layout():
    return dbc.Container(fluid=True, children=[
        dbc.Row(justify="center", children=[
            dbc.Col(lg=10, children=[
                html.H1("Sécurité et stockage des métaux précieux : Protéger votre investissement", className="display-4 text-center mb-4 fw-bold"),

                html.P(
                    "L'acquisition de métaux précieux implique un engagement financier important. Par conséquent, il est primordial d'assurer la sécurité et le stockage adéquat de ces actifs. Qu'il s'agisse d'or, d'argent, de platine ou d'autres métaux précieux, les investisseurs doivent examiner attentivement les différentes options de stockage, évaluer les risques potentiels et mettre en œuvre des mesures de sécurité robustes pour protéger leur investissement. Cet article fournit un guide complet sur les solutions de stockage sécurisé, les stratégies d'atténuation des risques et les options d'assurance pour préserver la valeur et l'intégrité des avoirs en métaux précieux.",
                    className="lead"
                ),

                html.H2("Options de stockage sécurisé pour les métaux précieux : Un guide complet", className="display-6 mt-5 mb-4 fw-bold"),

                html.P(
                    "Il existe plusieurs options de stockage, chacune ayant ses propres avantages et inconvénients en termes de coût, de sécurité, d'accessibilité et de discrétion."
                ),

                html.H3("Stockage à domicile", className="display-7 mt-4 mb-3 fw-bold"),

                html.Ul([
                    html.Li(className="mt-3", children=[
                        html.Span("Coffres-forts à domicile : ", className="fw-bold"),
                        "Un coffre-fort robuste, correctement installé et fixé à la structure du bâtiment, peut offrir un bon niveau de protection contre le vol. Choisissez un coffre-fort avec un indice de résistance au feu élevé pour le protéger contre les dommages causés par le feu."
                    ]),
                    html.Li(className="mt-3", children=[
                        html.Span("Cachettes : ", className="fw-bold"),
                        "Pour les petites quantités de métaux précieux, des cachettes discrètes dans la maison peuvent fournir une couche de sécurité supplémentaire. Des emplacements créatifs et bien dissimulés peuvent dissuader les voleurs opportunistes.",
                    ]),
                    html.Li(className="mt-3", children=[
                        html.Span("Avantages : ", className="fw-bold"),
                        "Contrôle direct sur les actifs, accessibilité facile, absence de frais de stockage récurrents et plus grande confidentialité.",

                    ]),
                    html.Li(className="mt-3", children=[
                        html.Span("Inconvénients : ", className="fw-bold"),
                        "Risque de vol plus élevé si le coffre-fort n'est pas correctement sécurisé ou si la cachette est découverte, vulnérabilité au feu ou aux catastrophes naturelles, et risque de perte ou de dommage accidentel. Les coffres-forts bon marché offrent une protection minimale et peuvent être facilement forcés.",

                    ]),
                ], className="list-unstyled"),

                html.H3("Coffres bancaires", className="display-7 mt-4 mb-3 fw-bold"),

                html.Ul([
                    html.Li(
                        "Les coffres bancaires dans des banques réputées offrent une solution de stockage hors site sécurisée. Les banques disposent généralement de mesures de sécurité robustes, notamment des coffres-forts, des alarmes et des systèmes de surveillance. Certaines banques offrent une assurance pour le contenu des coffres, mais les limitations de couverture et les conditions spécifiques doivent être examinées attentivement."
                    ),
                    html.Li(className="mt-3", children=[
                        html.Span("Avantages : ", className="fw-bold"),
                        "Sécurité renforcée par rapport au stockage à domicile, protection contre le feu et les catastrophes naturelles (dans les limites des paramètres de sécurité de la banque) et tranquillité d'esprit en sachant que les actifs sont stockés dans un environnement géré par des professionnels.",

                    ]),
                    html.Li(className="mt-3", children=[
                        html.Span("Inconvénients : ", className="fw-bold"),
                        "Frais de location récurrents, accessibilité limitée aux heures d'ouverture des banques, restrictions potentielles d'accès pendant les crises financières ou les jours fériés, et moins de confidentialité par rapport au stockage à domicile. De plus, le contenu des coffres bancaires n'est généralement pas couvert par l'assurance-dépôts (ou un système d'assurance-dépôts équivalent).",

                    ]),
                ], className="list-unstyled"),

                html.H3("Coffres-forts privés et installations de stockage", className="display-7 mt-4 mb-3 fw-bold"),

                html.Ul([
                    html.Li(
                        "Les coffres-forts privés spécialisés ou les installations de stockage sécurisé offrent le plus haut niveau de protection pour les avoirs importants en métaux précieux. Ces installations disposent de systèmes de sécurité avancés, notamment plusieurs couches de contrôle d'accès physique et électronique, des environnements à température contrôlée et des options d'assurance complètes."
                    ),
                    html.Li(className="mt-3", children=[
                        html.Span("Avantages : ", className="fw-bold"),
                        "Sécurité maximale, protection contre le vol, le feu et les catastrophes naturelles, protocoles de manutention et de stockage spécialisés pour les métaux précieux et possibilité de stockage séparé (vos actifs sont physiquement séparés des autres).",

                    ]),
                    html.Li(className="mt-3", children=[
                        html.Span("Inconvénients : ", className="fw-bold"),
                        "Frais de stockage les plus élevés, accès potentiellement moins pratique que le stockage à domicile ou en banque, et nécessite une diligence raisonnable approfondie pour s'assurer de la réputation et de la stabilité financière de l'installation.",

                    ]),
                ], className="list-unstyled"),

                html.H2("Risques de sécurité et stratégies d'atténuation : Une discussion approfondie",
                        className="display-6 mt-5 mb-4 fw-bold"),

                html.P(
                    "La protection des investissements en métaux précieux nécessite une approche proactive de l'atténuation des risques."
                ),

                html.H3("Vol", className="display-7 mt-4 mb-3 fw-bold"),

                html.Ul([
                    html.Li(className="mt-3", children=[
                        html.Span("Stockage à domicile : ", className="fw-bold"),
                        "Investissez dans un coffre-fort de haute qualité, installé par des professionnels et boulonné à la structure du bâtiment. Évitez de divulguer vos avoirs en métaux précieux. Envisagez un coffre-fort leurre ou une cachette pour détourner l'attention du véritable emplacement de stockage. Installez un système d'alarme avec des capteurs sur les portes et les fenêtres, et envisagez des détecteurs de mouvement ou des caméras de sécurité."
                    ]),
                    html.Li(className="mt-3", children=[
                        html.Span("Coffres bancaires : ", className="fw-bold"),
                        "Choisissez une banque réputée avec des mesures de sécurité robustes. Soyez discret lorsque vous accédez à votre coffre-fort.",

                    ]),
                    html.Li(className="mt-3", children=[
                        html.Span("Coffres-forts privés : ", className="fw-bold"),
                        "Examinez attentivement les protocoles de sécurité de l'installation, y compris les contrôles d'accès, la vérification des antécédents du personnel et la couverture d'assurance.",

                    ]),
                ], className="list-unstyled"),

                html.H3("Incendie", className="display-7 mt-4 mb-3 fw-bold"),

                html.Ul([
                    html.Li(className="mt-3", children=[
                        html.Span("Stockage à domicile : ", className="fw-bold"),
                        "Stockez les métaux dans un coffre-fort ignifuge avec une certification. Mettez en œuvre des mesures générales de sécurité incendie dans votre maison, y compris des détecteurs de fumée, des extincteurs et un plan d'évacuation."
                    ]),
                    html.Li(className="mt-3", children=[
                        html.Span("Coffres bancaires et coffres-forts privés : ", className="fw-bold"),
                        "Ces installations sont généralement équipées de systèmes d'extinction d'incendie et sont conçues pour résister aux dommages causés par le feu, offrant une meilleure protection que le stockage à domicile.",

                    ]),
                ], className="list-unstyled"),

                html.H3("Risque de contrepartie", className="display-7 mt-4 mb-3 fw-bold"),

                html.Ul([
                    html.Li(
                        "Le risque de contrepartie survient lorsque l'on confie des actifs à un tiers, tel qu'une banque ou une installation de stockage. Le risque est que l'institution devienne insolvable, restreigne l'accès aux actifs ou se livre à des activités frauduleuses."
                    ),
                    html.Li(className="mt-3", children=[
                        html.Span("Atténuation du risque de contrepartie : ", className="fw-bold"),
                        "Détenir du métal physique à domicile élimine ce risque, mais augmente les risques de vol et de perte. Lorsque vous utilisez une banque ou une installation privée, effectuez une diligence raisonnable approfondie pour évaluer leur stabilité financière, leur réputation et leur conformité légale. Diversifiez les emplacements de stockage et envisagez des options de stockage séparé.",
                    ]),
                ], className="list-unstyled"),

                html.H3("Catastrophes naturelles", className="display-7 mt-4 mb-3 fw-bold"),

                html.Ul([
                    html.Li(
                        "Les catastrophes naturelles, comme les inondations, les tremblements de terre ou les ouragans, peuvent constituer une menace importante pour les avoirs en métaux précieux."
                    ),
                    html.Li(className="mt-3", children=[
                        html.Span("Atténuation : ", className="fw-bold"),
                        "Choisissez des emplacements de stockage géographiquement moins sujets à des catastrophes naturelles spécifiques. Les coffres bancaires et les coffres-forts privés, souvent situés dans des bâtiments renforcés, offrent généralement une meilleure protection que le stockage à domicile. Assurez-vous que les polices d'assurance couvrent les risques spécifiques de catastrophes naturelles.",

                    ]),
                ], className="list-unstyled"),

                html.H3("Escroqueries et contrefaçons", className="display-7 mt-4 mb-3 fw-bold"),

                html.Ul([
                    html.Li(
                        "Le marché des métaux précieux, en particulier les marchés en ligne et les transactions privées, est sensible aux escroqueries et aux produits contrefaits."
                    ),
                    html.Li(className="mt-3", children=[
                        html.Span("Atténuation : ", className="fw-bold"),
                        "N'achetez qu'auprès de revendeurs réputés ou de vendeurs privés ayant des antécédents vérifiables. Authentifiez tous les achats en utilisant plusieurs méthodes de test. Méfiez-vous des offres qui semblent trop belles pour être vraies.",

                    ]),
                ], className="list-unstyled"),

                html.H3("Perte ou oubli", className="display-7 mt-4 mb-3 fw-bold"),

                html.Ul([
                    html.Li(
                        "Égarer ou oublier l'emplacement des métaux précieux cachés est un événement étonnamment courant."
                    ),
                    html.Li(className="mt-3", children=[
                        html.Span("Atténuation : ", className="fw-bold"),
                        "Tenez des registres détaillés de vos avoirs et de leurs emplacements de stockage. Si vous utilisez une cachette, créez une carte ou des instructions écrites et conservez-les en lieu sûr dans un endroit séparé. Informez un membre de votre famille ou un conseiller juridique de confiance de vos avoirs et de vos modalités de stockage.",

                    ]),
                ], className="list-unstyled"),

                html.H2("Analyse des méthodes de stockage: avantages, inconvénients et considérations",
                        className="display-6 mt-5 mb-4 fw-bold"),

                html.P(
                    "(Développez cette section en ajoutant plus de détails sur chaque méthode, en comparant les coûts (achat d'un coffre-fort vs frais de location), les options d'assurance et l'accessibilité):"
                ),

                html.H3("Stockage à domicile", className="display-7 mt-4 mb-3 fw-bold"),

                html.P(
                    "Discuter des différents types de coffres-forts à domicile (ignifuges, résistants au cambriolage, à combinaison, biométriques), des compartiments cachés et des coffres-forts leurres. Analyser les coûts d’achat et d’installation d’un coffre-fort par rapport aux frais de location récurrents pour d’autres options de stockage."
                ),

                html.H3("Coffres bancaires", className="display-7 mt-4 mb-3 fw-bold"),

                html.P(
                    "Comparer les frais de location entre différentes banques. Examiner les options d’assurance offertes par les banques et leurs limitations de couverture. Discuter des restrictions d’accessibilité et des difficultés potentielles pendant les jours fériés ou les crises financières."
                ),

                html.H3("Coffres privés", className="display-7 mt-4 mb-3 fw-bold"),

                html.P(
                    "Rechercher des sociétés de coffres privés réputées et comparer leurs services, leurs frais, leurs mesures de sécurité et leurs options d’assurance. Discuter des avantages du stockage séparé, du stockage alloué et d’autres services spécialisés."
                ),

                html.H2("Tactiques de diversion et mesures de sécurité supplémentaires",
                        className="display-6 mt-5 mb-4 fw-bold"),

                html.P(
                    "L'amélioration de la sécurité nécessite une approche multicouche. Combinez la sécurité physique avec des tactiques de diversion et d'autres mesures proactives."
                ),

                html.Ul([
                    html.Li(className="mt-3", children=[
                        html.Span("Coffres-forts leurres : ", className="fw-bold"),
                        "Un coffre-fort moins sécurisé et facilement accessible contenant une petite quantité d'objets de valeur peut détourner l'attention du véritable emplacement de stockage."
                    ]),
                    html.Li(className="mt-3", children=[
                        html.Span("Fausses caméras de sécurité : ", className="fw-bold"),
                        " : Des caméras de sécurité visibles mais non fonctionnelles peuvent dissuader les voleurs opportunistes.",

                    ]),
                    html.Li(className="mt-3", children=[
                        html.Span("Sécurité domiciliaire renforcée : ", className="fw-bold"),
                        "Des portes et fenêtres renforcées, un film de sécurité sur les fenêtres, un éclairage activé par le mouvement et une signalisation du système d'alarme peuvent améliorer la sécurité générale de la maison.",

                    ]),
                    html.Li(className="mt-3", children=[
                        html.Span("Discrétion : ", className="fw-bold"),
                        "Évitez de divulguer vos avoirs en métaux précieux. Soyez discret lorsque vous transportez ou accédez à vos métaux.",

                    ]),
                ], className="list-unstyled"),
                html.H2("Options d'assurance et documentation", className="display-6 mt-5 mb-4 fw-bold"),

                html.P(
                    "L'assurance est essentielle pour protéger les investissements en métaux précieux contre les événements imprévus."
                ),

                html.H3("Assurance habitation ou locataire", className="display-7 mt-4 mb-3 fw-bold"),

                html.Ul([
                    html.Li(
                        "Vérifiez votre police actuelle pour connaître la couverture des métaux précieux. La plupart des polices ont des limitations de couverture pour les objets de valeur, et des «avenants» supplémentaires peuvent être nécessaires pour assurer adéquatement les avoirs en métaux précieux. Fournissez à votre compagnie d'assurance une documentation détaillée de vos métaux, y compris les reçus d'achat, les photos et les évaluations."
                    ),
                ], className="list-unstyled"),

                html.H3("Assurance spécialisée pour les métaux précieux", className="display-7 mt-4 mb-3 fw-bold"),

                html.Ul([
                    html.Li(
                        "Certains assureurs proposent des polices spécifiquement conçues pour les métaux précieux, offrant une couverture plus large et des limites plus élevées que l'assurance habitation ou locataire standard."
                    ),
                ], className="list-unstyled"),

                html.H3("Assurance pour coffre bancaire", className="display-7 mt-4 mb-3 fw-bold"),

                html.Ul([
                    html.Li(
                        "Certaines banques offrent une assurance pour le contenu des coffres bancaires. Examinez attentivement les détails de la couverture, les exclusions et le processus de réclamation."
                    ),
                ], className="list-unstyled"),

                html.H3("Assurance pour coffre-fort privé", className="display-7 mt-4 mb-3 fw-bold"),

                html.Ul([
                    html.Li(
                        "Les installations de coffres-forts privés réputées incluent une assurance complète dans leur forfait de services. Examinez les détails de la police et assurez-vous que les limites de couverture sont adéquates."
                    ),
                ], className="list-unstyled"),

            ]),  # Close the dbc.Col
        ]),  # Close the dbc.Row
    ])  # Close the dbc.Container