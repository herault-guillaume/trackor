from dash import html, dcc
import dash_bootstrap_components as dbc


def layout():
    return dbc.Container(fluid=True, children=[
        dbc.Row(justify="center", children=[
            dbc.Col(lg=10, children=[
                html.H1("Authentification des métaux précieux : Techniques avancées pour identifier les contrefaçons",
                        className="display-4 text-center mb-4 fw-bold"),

                html.P(
                    "Le marché des métaux précieux, avec son attrait pour les actifs tangibles et son potentiel d'appréciation à long terme, attire malheureusement les contrefacteurs. Pour les investisseurs, en particulier ceux qui acquièrent de l'or et de l'argent physiques, l'authentification est primordiale. Distinguer les produits authentiques des contrefaçons nécessite une approche à multiples facettes, employant une combinaison de tests et de techniques. Cet article sert de guide complet des méthodes d'authentification avancées pour les métaux précieux, en approfondissant les forces et les limites de chaque test, en explorant les techniques de contrefaçon courantes et en fournissant des conseils pratiques pour garantir l'authenticité de vos investissements."
                ),

                html.H2("Méthodes d'authentification : Un guide complet", className="display-6 mt-5 mb-4 fw-bold"),

                html.P(
                    "Aucune méthode d'authentification ne garantit une certitude absolue, surtout avec des techniques de contrefaçon de plus en plus sophistiquées. Une combinaison de tests fournit les résultats les plus fiables."
                ),

                html.H3("Inspection visuelle", className="display-7 mt-4 mb-3 fw-bold"),

                html.Ul([
                    html.Li(
                        "Examen détaillé : Examinez attentivement la pièce ou le lingot pour déceler toute incohérence dans le dessin, les inscriptions, les marques d'atelier et les lettres sur la tranche. Comparez l'objet suspect à des images ou à des échantillons authentiques du même produit, en portant une attention particulière aux détails. Les contrefacteurs commettent souvent de légères erreurs dans la conception, le lettrage ou l'espacement des éléments."
                    ),
                    html.Li(
                        "Irrégularités de surface : Recherchez des textures de surface inhabituelles, des imperfections ou des marques d'outils qui pourraient indiquer un moulage ou d'autres méthodes de production non standard. Examinez la tranche de la pièce pour déceler des irrégularités ou des incohérences dans le crénelage (bord strié).",
                        className="mt-3"
                    ),
                    html.Li(
                        "Couleur et lustre : L'or véritable possède un lustre et une couleur caractéristiques. Comparez la couleur de l'objet suspect à des échantillons authentiques connus. Cependant, la couleur seule n'est pas déterminante, car le placage ou l'alliage peuvent imiter l'apparence de l'or. L'argent a un lustre brillant et réfléchissant lorsqu'il est neuf, mais il se ternit avec le temps, développant une patine. Les différentes puretés d'argent et les traitements de surface affectent également l'apparence.",
                        className="mt-3"
                    ),
                    html.Li(
                        "Limites : L'inspection visuelle est subjective et nécessite de l'expérience. Les contrefaçons de haute qualité peuvent être visuellement trompeuses, surtout sur les photographies. L'inspection visuelle doit être la première étape, mais jamais la seule.",
                        className="mt-3"
                    ),
                ], className="list-unstyled"),

                html.H3("Test sonore", className="display-7 mt-4 mb-3 fw-bold"),

                html.Ul([
                    html.Li(
                        "Le «test du ping» : Les pièces d'or et d'argent authentiques produisent un son clair distinctif lorsqu'elles sont frappées ou laissées tomber sur une surface dure. Ce «ping» est dû à la densité et à l'élasticité du métal. Comparez le son de l'objet suspect à un exemple authentique connu. Un bruit sourd au lieu d'un son clair peut suggérer une contrefaçon."
                    ),
                    html.Li(
                        "Applications mobiles : Plusieurs applications mobiles analysent les fréquences sonores d'une pièce lorsqu'elle est frappée, en les comparant à une base de données de pièces authentiques connues. Bien que potentiellement utiles, ces applications ne sont pas infaillibles et doivent être utilisées conjointement avec d'autres tests. Des facteurs externes comme le bruit de fond ou la force de la frappe peuvent influencer les résultats.",
                        className="mt-3"
                    ),
                    html.Li(
                        "Limites : Le test du ping est subjectif et nécessite de l'expérience pour discerner les différences subtiles de son. Il est également moins fiable pour les petites pièces ou les lingots.",
                        className="mt-3"
                    ),
                ], className="list-unstyled"),

                html.H3("Test magnétique", className="display-7 mt-4 mb-3 fw-bold"),

                html.Ul([
                    html.Li(
                        "L'or et l'argent sont diamagnétiques, ce qui signifie qu'ils sont faiblement repoussés par les aimants. Un aimant puissant en néodyme peut aider à détecter les matériaux ferromagnétiques (comme le fer ou l'acier) souvent utilisés dans les noyaux de contrefaçon. Si une pièce ou un lingot est fortement attiré par un aimant, il ne s'agit certainement pas d'or ou d'argent."
                    ),
                    html.Li(
                        "Test de glissement : Faire glisser un aimant puissant le long d'une barre d'argent authentique crée un effet de freinage dû aux courants de Foucault générés par le champ magnétique en mouvement interagissant avec l'argent conducteur. Une fausse barre avec un noyau non argenté ne présentera pas cet effet de freinage.",
                        className="mt-3"
                    ),
                    html.Li(
                        "Limites : Certains contrefacteurs utilisent des métaux non magnétiques comme le tungstène ou le plomb, ce qui peut tromper le test magnétique. Le test de glissement est plus efficace sur les grandes barres que sur les petites pièces.",
                        className="mt-3"
                    ),
                ], className="list-unstyled"),

                html.H3("Test de poids et dimensions", className="display-7 mt-4 mb-3 fw-bold"),

                html.Ul([
                    html.Li(
                        "Mesure précise : L'or et l'argent ont des densités spécifiques. Mesurer avec précision le poids et les dimensions (à l'aide d'une balance calibrée et d'un pied à coulisse numérique) et calculer la densité peut aider à confirmer l'authenticité. Comparez la densité calculée aux valeurs connues pour le métal. Des variations mineures de poids peuvent se produire en raison de l'usure, en particulier pour les pièces anciennes."
                    ),
                    html.Li(
                        "Limites : Nécessite des outils de mesure et des calculs précis. Les contrefacteurs utilisent parfois du tungstène, un métal dont la densité est similaire à celle de l'or, pour créer de fausses pièces ou de faux lingots qui peuvent réussir le test de poids.",
                        className="mt-3"
                    ),
                ], className="list-unstyled"),

                html.H3("Test à l'acide", className="display-7 mt-4 mb-3 fw-bold"),

                html.Ul([
                    html.Li(
                        "L'or est résistant à la plupart des acides, tandis que l'argent réagit différemment à des solutions acides spécifiques. L'application d'une petite goutte d'acide de test sur une zone discrète du métal peut indiquer sa réaction et fournir des indices sur sa composition. Un changement de couleur ou son absence peut aider à identifier le métal. Différents carats d'or réagissent différemment à l'acide, et des kits de test à l'acide sont disponibles pour diverses puretés d'or."
                    ),
                    html.Li(
                        "Limites : Le test à l'acide est destructif, laissant une petite marque sur la zone testée. Il ne teste que la surface et peut être trompé par des objets plaqués. Nécessite une manipulation prudente des acides corrosifs et des précautions de sécurité appropriées.",
                        className="mt-3"
                    ),
                ], className="list-unstyled"),

                html.H3("Test de densité (pesée hydrostatique)", className="display-7 mt-4 mb-3 fw-bold"),

                html.Ul([
                    html.Li(
                        "Ce test précis mesure la densité d'un objet en comparant son poids dans l'air à son poids lorsqu'il est immergé dans l'eau. C'est une méthode fiable pour déterminer la densité spécifique d'un métal et la comparer aux valeurs connues pour l'or ou l'argent. Cette méthode nécessite un équipement spécifique (une balance de précision, un bécher et un fil fin) et prend plus de temps que d'autres tests."
                    ),
                    html.Li(
                        "Limites : Peut être peu pratique pour les tests en déplacement et nécessite des procédures de mesure soigneuses pour des résultats précis. Ne peut pas être effectué sur des objets poreux ou comportant des cavités creuses.",
                        className="mt-3"
                    ),
                ], className="list-unstyled"),

                html.H3("Outils et technologies spécialisés", className="display-7 mt-4 mb-3 fw-bold"),

                html.Ul([
                    html.Li(
                        "Testeurs électroniques : Divers appareils électroniques utilisent la conductivité électrique ou d'autres propriétés pour tester la composition des métaux. Le Sigma Metalyzer, par exemple, est un appareil non destructif utilisé par les professionnels pour déterminer la pureté et l'authenticité des métaux précieux. Les analyseurs par fluorescence X (XRF) peuvent également fournir une analyse élémentaire précise."
                    ),
                    html.Li(
                        "Spectroscopie : L'analyse spectroscopique examine la lumière émise ou absorbée par un métal lorsqu'il est chauffé ou exposé à des longueurs d'onde spécifiques de la lumière. Cette méthode permet d'identifier avec précision le métal et ses composants. Cela nécessite un équipement et une expertise spécialisés.",
                        className="mt-3"
                    ),
                ], className="list-unstyled"),

                html.H2("Techniques de contrefaçon courantes", className="display-6 mt-5 mb-4 fw-bold"),

                html.P(
                    "Les contrefacteurs utilisent diverses méthodes pour créer de faux produits en métaux précieux. Comprendre ces techniques est crucial pour une authentification efficace."
                ),

                html.Ul([
                    html.Li(
                        "Placage : Recouvrir un métal de base d'une fine couche d'or ou d'argent peut tromper des tests simples comme le test magnétique ou un test rapide à l'acide."
                    ),
                    html.Li(
                        "Alliage : Mélanger une petite quantité d'or ou d'argent avec un métal de base moins cher peut créer un alliage qui imite l'apparence et certaines propriétés du métal authentique.",
                        className="mt-3"
                    ),
                    html.Li(
                        "Moulage : Les faux lingots ou pièces peuvent être moulés à partir de moules, souvent avec de légères imperfections de conception ou de poids.",
                        className="mt-3"
                    ),
                    html.Li(
                        "Noyaux en tungstène : Le tungstène a une densité similaire à celle de l'or et est parfois utilisé comme noyau pour les faux lingots ou pièces d'or afin de tromper le test de poids.",
                        className="mt-3"
                    ),
                    html.Li(
                        "Répliques et refrappes : Les reproductions de pièces historiques ou les refrappes non autorisées (pièces frappées à partir de matrices originales mais pas par l'atelier monétaire officiel) peuvent tromper les collectionneurs inexpérimentés si elles ne sont pas examinées attentivement.",
                        className="mt-3"
                    ),
                ], className="list-unstyled"),

                html.H2("Dispositifs de sécurité sur les pièces modernes", className="display-6 mt-5 mb-4 fw-bold"),

                html.P(
                    "De nombreuses pièces d'investissement et de collection modernes intègrent des dispositifs de sécurité pour dissuader la contrefaçon."
                ),

                html.Ul([
                    html.Li(
                        "Micro-gravure : Des détails microscopiques complexes, souvent visibles uniquement sous grossissement, ajoutent une couche de sécurité."
                    ),
                    html.Li(
                        "Marquages laser : Des marquages laser précis créent des motifs ou des identifiants uniques.",
                        className="mt-3"
                    ),
                    html.Li(
                        "Hologrammes : Les images holographiques ou les bandes de sécurité ajoutent un élément visuel difficile à reproduire.",
                        className="mt-3"
                    ),
                    html.Li(
                        "Marques privées : De petites marques ou symboles uniques à la surface de la pièce indiquent une année, un atelier ou une série spécifique.",
                        className="mt-3"
                    ),
                ], className="list-unstyled"),

                html.H2("Le «problème des blisters»", className="display-6 mt-5 mb-4 fw-bold"),

                html.P(
                    "De nombreuses pièces d'investissement modernes sont vendues dans des blisters ou des capsules scellés pour les protéger. Cela pose un défi pour l'authentification, car le retrait de la pièce de son emballage peut diminuer sa valeur."
                ),

                html.Ul([
                    html.Li(
                        "Sources fiables : La meilleure approche consiste à n'acheter des pièces encapsulées qu'auprès de revendeurs réputés qui garantissent l'authenticité."
                    ),
                    html.Li(
                        "Tests non destructifs : Envisagez des méthodes non destructives comme l'inspection visuelle de l'emballage, la vérification du poids de l'emballage scellé et la comparaison de l'apparence de la pièce avec des images certifiées. Des testeurs électroniques spécialisés peuvent parfois authentifier les pièces à travers l'emballage.",
                        className="mt-3"
                    ),
                    html.Li(
                        "Acceptation du risque : Pour les pièces achetées auprès de sources moins réputées, l'ouverture de l'emballage pour effectuer une authentification approfondie peut être nécessaire, malgré l'impact potentiel sur la valeur de revente.",
                        className="mt-3"
                    ),
                ], className="list-unstyled"),

            ]),  # Close the dbc.Col
        ]),  # Close the dbc.Row
    ])  # Close the dbc.Container