from dash import html,dcc
import dash_bootstrap_components as dbc

def layout():
    return dbc.Container(fluid=True, children=[
        dbc.Row(justify="center", children=[
            dbc.Col(lg=10, children=[
                html.H1("Stratégies d'investissement dans l'or : Compléments", className="display-4 text-center mb-4"),

                html.P(
                    "L'or captive les investisseurs depuis des millénaires, servant de réserve de valeur, de moyen d'échange et de symbole de richesse et de pouvoir. Dans le paysage de l'investissement moderne, l'or continue d'occuper une position unique, souvent considéré comme une valeur refuge et une protection contre l'inflation et l'incertitude économique. Cet article explore les stratégies avancées d'investissement dans l'or, fournissant aux investisseurs expérimentés les connaissances et les outils nécessaires pour naviguer dans les complexités du marché de l'or et optimiser leurs portefeuilles.",
                    className="lead"
                ),

                html.H2("L'or comme investissement : Une perspective avancée", className="display-6 mt-5 mb-4 "),

                html.P(
                    "L'attrait de l'or en tant qu'investissement découle de sa résilience historique, de sa rareté et de sa valeur intrinsèque perçue. Bien qu'il ne génère pas de revenus comme les actions ou les obligations, il peut servir de puissant facteur de diversification et de protecteur de patrimoine en période de turbulences économiques.",
                       className="lead"
                ),

                html.H3("Protection contre l'inflation", className="display-7 mt-4 mb-3 "),

                html.Ul([
                    html.Li(
                        "À mesure que les monnaies fiduciaires perdent leur pouvoir d'achat en raison de l'inflation, la valeur de l'or a tendance à augmenter. Les données historiques suggèrent une corrélation positive entre les prix de l'or et l'inflation, bien que cette relation ne soit pas toujours constante à court terme.",
                    ),
                    html.Li(
                        "Cependant, il est crucial de noter que pendant les périodes de forte inflation, d'autres classes d'actifs, comme l'immobilier ou certaines matières premières, pourraient surpasser l'or. Par conséquent, l'or doit être considéré comme une composante d'une stratégie diversifiée de couverture contre l'inflation.",
                        className="mt-3"
                    ),
                ], className="list-unstyled"),

                html.H3("Valeur refuge", className="display-7 mt-4 mb-3 "),

                html.Ul([
                    html.Li(
                        "En période de ralentissement économique, de krach boursier ou d'instabilité géopolitique, les investisseurs se tournent souvent vers l'or comme valeur refuge, faisant grimper son prix. Ce phénomène de « fuite vers la sécurité » renforce la réputation de l'or en tant que réserve de valeur en période d'incertitude.",

                    ),
                    html.Li(
                        "Cependant, la performance de l'or pendant les crises peut être imprévisible. Par exemple, lors du krach boursier de 2020 déclenché par la pandémie, de nombreux investisseurs ont initialement vendu de l'or pour couvrir les pertes sur d'autres actifs, démontrant que même les valeurs refuges peuvent connaître une volatilité à court terme.",
                        className="mt-3"
                    ),
                ], className="list-unstyled"),

                html.H3("Diversification du portefeuille", className="display-7 mt-4 mb-3 "),

                html.Ul([
                    html.Li(
                        "L'inclusion de l'or dans un portefeuille diversifié peut contribuer à réduire le risque global du portefeuille. Les fluctuations du prix de l'or ont souvent une corrélation faible ou négative avec d'autres classes d'actifs, ce qui a un effet stabilisateur. Cela peut améliorer les rendements corrigés du risque à long terme.",
                    ),
                    html.Li(
                        "L'allocation optimale de l'or dans un portefeuille dépend de la tolérance au risque individuelle, des objectifs d'investissement et des perspectives du marché. Une recommandation courante est d'allouer 5 à 20 % d'un portefeuille à l'or, mais cela peut varier en fonction des circonstances spécifiques.",
                        className="mt-3"
                    ),
                ], className="list-unstyled"),

                html.H2("Produits aurifères : Une analyse complète", className="display-6 mt-5 mb-4 "),

                html.P(
                    "Les investissements dans l'or se présentent sous diverses formes, chacune ayant ses propres caractéristiques, avantages et inconvénients.",
                       className="lead"
                ),

                html.H3("Pièces d'or", className="display-7 mt-4 mb-3 "),

                html.Ul([
                    html.Li(className="mt-3", children=[
                        html.Span("Avantages : ", className="fw-bold"),
                        "Grande liquidité, facilité d'authentification, attrait esthétique et valeur numismatique potentielle. Certaines pièces d'or ayant cours légal peuvent offrir des avantages fiscaux selon la juridiction. Les pièces d'or fractionnaires (par exemple, 1/10 oz) permettent des investissements plus petits et réguliers.",
                    ]),
                    html.Li(className="mt-3", children=[
                        html.Span("Inconvénients : ", className="fw-bold"),
                        "Primes plus élevées par rapport aux lingots d'or, potentiel de contrefaçon et sensibilité aux rayures ou à l'usure, en particulier pour les pièces en or pur comme la Britannia.",
                    ]),
                ], className="list-unstyled"),

                html.H3("Lingots d'or", className="display-7 mt-4 mb-3 "),

                html.Ul([
                    html.Li(className="mt-3", children=[
                        html.Span("Avantages : ", className="fw-bold"),
                        "Primes plus faibles par rapport aux pièces, efficaces pour stocker de grandes quantités d'or, et disponibilité dans une large gamme de tailles et de poids.",
                    ]),
                    html.Li(className="mt-3", children=[
                        html.Span("Inconvénients : ", className="fw-bold"),
                        "Moins liquides que les pièces, plus difficiles à authentifier, surtout lorsqu'ils ne sont pas scellés et manquent de provenance claire, et coûts de stockage potentiellement plus élevés pour les lingots plus gros.",
                    ]),
                ], className="list-unstyled"),

                html.H3("Bijoux en or", className="display-7 mt-4 mb-3 "),

                html.Ul([
                    html.Li(className="mt-3", children=[
                        html.Span("Avantages : ", className="fw-bold"),
                        "Attrait esthétique, peuvent être portés et appréciés, et potentiel d'appréciation de la valeur pour les pièces anciennes ou de créateurs.",
                    ]),
                    html.Li(className="mt-3", children=[
                        html.Span("Inconvénients : ", className="fw-bold"),
                        "Soumis à la TVA dans de nombreuses juridictions, marges plus élevées par rapport aux produits en lingots, potentiel de valeur de revente plus faible en raison du design ou de l'usure, et nécessite une expertise pour évaluer la valeur de l'or ancien ou de la ferraille.",
                    ]),
                ], className="list-unstyled"),

                html.H3("FNB aurifères (Fonds négociés en bourse)", className="display-7 mt-4 mb-3 "),

                html.Ul([
                    html.Li(className="mt-3", children=[
                        html.Span("Avantages : ", className="fw-bold"),
                        "Facilité d'achat et de vente par l'intermédiaire de comptes de courtage, élimine le besoin de stockage physique et offre une plus grande liquidité par rapport à l'or physique.",
                    ]),
                    html.Li(className="mt-3", children=[
                        html.Span("Inconvénients : ", className="fw-bold"),
                        "Les investisseurs ne possèdent pas l'or physique, risque de contrepartie associé au fournisseur du FNB, potentiel d'écarts par rapport au prix de l'or en raison de la structure et des frais de gestion du FNB, et préoccupations quant à la capacité de convertir les actions en or physique pendant une crise. De plus, certains soutiennent que les FNB sont complices de la manipulation du marché, en particulier sur le marché de l'argent.",
                    ]),
                ], className="list-unstyled"),

                html.H2("Stratégies avancées de calcul des primes", className="display-6 mt-5 mb-4 "),

                html.P(
                    "Le calcul et la comparaison précis des primes sur l'or exigent d'aller au-delà de la formule de base et de tenir compte de divers facteurs du marché.",
                       className="lead"
                ),

                html.Ul([
                    html.Li(className="mt-3", children=[
                        html.Span("Fluctuations du prix au comptant : ", className="fw-bold"),
                        "Le prix au comptant de l'or change constamment, ce qui a un impact direct sur la valeur du métal fondu et, par conséquent, sur le calcul de la prime. Les investisseurs doivent utiliser le prix au comptant le plus récent lorsqu'ils calculent les primes. Bullion-Sniper le fait pour vous, plusieurs fois par jour!",
                    ]),
                    html.Li(className="mt-3", children=[
                        html.Span("Marges des négociants : ", className="fw-bold"),
                        "Les marges des négociants varient, et même des différences apparemment faibles en pourcentage peuvent se traduire par des coûts importants au fil du temps, en particulier pour les gros investissements. Il est essentiel de comparer les prix de plusieurs négociants, y compris les détaillants en ligne et les boutiques locales.",

                    ]),
                    html.Li(className="mt-3", children=[
                        html.Span("Coûts cachés : ", className="fw-bold"),
                        "Tenez compte de tous les coûts associés à un achat, y compris l'expédition, l'assurance et toutes taxes ou droits applicables. Ces coûts peuvent considérablement réduire les rendements, en particulier pour les petits achats.",

                    ]),
                    html.Li(className="mt-3", children=[
                        html.Span("Tendances des primes : ", className="fw-bold"),
                        "Le suivi des tendances historiques des primes pour des pièces spécifiques peut fournir des informations sur la demande du marché, la rareté et les opportunités d'achat potentielles. Une hausse soudaine des primes pourrait indiquer une pénurie d'approvisionnement à court terme ou un intérêt accru des investisseurs.",

                    ]),
                ], className="list-unstyled"),

                html.H2("Démystifier les mythes de la confiscation de l'or", className="display-6 mt-5 mb-4 "),

                html.P(
                    "La crainte de la confiscation de l'or est un thème récurrent chez les investisseurs en métaux précieux. Comprendre les précédents historiques et les réglementations actuelles peut aider à dissiper ces mythes et à prendre des décisions éclairées.",
                       className="lead"
                ),

                html.Ul([
                    html.Li(
                        "Souvent cité comme un exemple de confiscation, le rappel de l'or américain de 1933 sous le président Roosevelt n'était pas une confiscation mais plutôt un rachat par le gouvernement au prix en vigueur. Bien que tous les citoyens n'aient pas obtempéré, et que la dévaluation ultérieure du dollar ait sans doute réduit la valeur de la compensation, il ne s'agissait pas d'une saisie sans contrepartie. Il faut tenir compte du contexte historique de la Grande Dépression et de la nécessité de stabiliser le dollar américain.",

                    ),
                    html.Li(
                        "L'accent mis actuellement sur la traçabilité des transactions et les exigences de déclaration pour les achats de métaux précieux vise principalement à lutter contre le blanchiment d'argent et les activités illicites, et non à faciliter une confiscation future. Bien que des changements législatifs soient toujours possibles, une confiscation pure et simple dans les économies développées est peu probable en raison de ses conséquences négatives potentielles sur la confiance du marché et les relations internationales.",
                        className="mt-3"
                    ),
                ], className="list-unstyled"),

            ]),  # Close the dbc.Col
        ]),  # Close the dbc.Row
    ])  # Close the dbc.Container