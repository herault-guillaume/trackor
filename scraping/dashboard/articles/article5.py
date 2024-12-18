from dash import html, dcc
import dash_bootstrap_components as dbc

def layout():
    return dbc.Container(fluid=True, children=[
        dbc.Row(justify="center", children=[
            dbc.Col(lg=9, children=[
                html.H1("Métaux précieux et diversification de portefeuille", className="display-4 text-center mb-4 fw-bold"),

                html.P(
                    "La diversification de portefeuille, pierre angulaire d'une gestion saine des investissements, consiste à allouer stratégiquement des capitaux entre différentes classes d'actifs afin de réduire le risque global et d'accroître le potentiel de rendement à long terme. Les métaux précieux, en particulier l'or et l'argent, ont historiquement joué un rôle unique dans les portefeuilles diversifiés, offrant une protection contre l'inflation, l'incertitude économique et les risques géopolitiques. Cet article explore des stratégies pour intégrer les métaux précieux dans un portefeuille bien structuré, en examinant leurs avantages, leurs limites et les aspects psychologiques à prendre en compte pour une préservation optimale du patrimoine.",
                    className="lead"
                ),

                html.H2("II. Rôles", className="display-6 mt-5 mb-4 fw-bold"),

                html.H3("Couverture contre l'inflation", className="display-7 mt-4 mb-3 fw-bold"),

                html.Ul([
                    html.Li(
                        "L'inflation érode le pouvoir d'achat des monnaies fiduciaires, diminuant la valeur réelle des investissements libellés dans ces monnaies. Les métaux précieux, avec leur rareté intrinsèque et leur valeur intrinsèque perçue, ont historiquement servi de réserve de valeur pendant les périodes inflationnistes. À mesure que la valeur de la monnaie papier diminue, le prix des métaux précieux a tendance à augmenter, compensant une partie de la pression inflationniste."
                    ),
                    html.Li(className="mt-3", children=[
                        html.Span("Mais ...", className="fw-bold"),
                        "Si les métaux précieux peuvent constituer une couverture contre l'inflation à long terme, leur prix peut fluctuer à court terme et ne pas toujours suivre ou dépasser parfaitement la hausse des taux d'inflation. D'autres classes d'actifs, comme l'immobilier ou certaines matières premières, pourraient offrir une meilleure protection contre l'inflation dans des conditions économiques spécifiques. Par conséquent, les métaux précieux devraient faire partie d'une stratégie de couverture contre l'inflation plus large, et non constituer la seule solution.",
                    ]),
                ], className="list-unstyled"),

                html.H3("Atténuation de l'incertitude économique", className="display-7 mt-4 mb-3 fw-bold"),

                html.Ul([
                    html.Li(
                        "En période de ralentissement économique ou de crise financière, les métaux précieux agissent souvent comme des valeurs refuges. Les investisseurs qui recherchent la stabilité et la préservation du capital ont tendance à se détourner des actifs plus risqués comme les actions et les obligations, et à se tourner vers les métaux précieux, ce qui fait augmenter la demande et les prix. Ce phénomène de «fuite vers la sécurité» peut contribuer à préserver la valeur du portefeuille pendant les périodes de volatilité des marchés."
                    ),
                    html.Li(className="mt-3", children=[
                        html.Span("Mais ...", className="fw-bold"),
                        "Bien que l'or, en particulier, soit considéré comme une valeur refuge, sa performance pendant les crises peut être imprévisible. Même pendant les ralentissements économiques majeurs, il peut y avoir des périodes où les prix de l'or baissent, car les investisseurs liquident leurs actifs pour couvrir leurs pertes ou répondre aux appels de marge. Cela a été observé au cours des premières phases du krach boursier de 2020 déclenché par la pandémie.",
                    ]),
                ], className="list-unstyled"),

                html.H3("Atténuation du risque géopolitique", className="display-7 mt-4 mb-3 fw-bold"),

                html.Ul([
                    html.Li(
                        "Les métaux précieux peuvent également servir de couverture contre les risques géopolitiques, tels que la guerre, l'instabilité politique ou les sanctions. Ces événements peuvent créer de l'incertitude sur les marchés financiers traditionnels, conduisant les investisseurs à rechercher la stabilité relative des métaux précieux. Le rôle historique de l'or en tant que réserve de valeur mondialement reconnue le rend particulièrement attrayant en période de tensions internationales."
                    ),
                    html.Li(className="mt-3", children=[
                        html.Span("Mais ... ", className="fw-bold"),
                        "L'impact des événements géopolitiques sur les prix des métaux précieux peut être de courte durée. Si une hausse initiale des prix peut se produire, les prix se stabilisent ou même baissent souvent une fois la situation résolue ou que le marché s'est adapté. Une perspective à long terme est essentielle lorsque l'on considère les métaux précieux comme une couverture contre les risques géopolitiques.",
                    ]),
                ], className="list-unstyled"),

                html.H2("II. Allocation dans un portefeuille", className="display-6 mt-5 mb-4 fw-bold"),

                html.P(
                    "Déterminer l'allocation optimale des métaux précieux au sein d'un portefeuille nécessite une approche nuancée, en tenant compte de divers facteurs."
                ),

                html.H3("Allocation en pourcentage", className="display-7 mt-4 mb-3 fw-bold"),

                html.Ul([
                    html.Li(
                        "Une stratégie courante consiste à allouer un pourcentage spécifique du portefeuille global aux métaux précieux, généralement entre 5% et 20%. Ce pourcentage dépend de la tolérance au risque individuelle, des objectifs d'investissement et des perspectives de l'économie et du système financier. Un investisseur plus prudent, préoccupé par la stabilité économique, pourrait allouer un pourcentage plus élevé aux métaux précieux, tandis qu'un investisseur plus agressif, axé sur la croissance, pourrait allouer un pourcentage plus faible."
                    ),
                    html.Li(className="mt-3", children=[
                        html.Span("Mais ... ", className="fw-bold"),
                        "Maintenir une allocation précise en pourcentage peut être difficile en raison des fluctuations du marché. Le rééquilibrage constant du portefeuille pour maintenir l'allocation cible peut entraîner des coûts de transaction et potentiellement des implications fiscales. Il est essentiel de laisser une certaine flexibilité et d'éviter les transactions excessives.",
                    ]),
                ], className="list-unstyled"),

                html.H3("Moyennisation des coûts en dollars (DCA)", className="display-7 mt-4 mb-3 fw-bold"),

                html.Ul([
                    html.Li(
                        "La DCA consiste à investir un montant fixe d'argent dans les métaux précieux à intervalles réguliers, quel que soit le prix. Cette stratégie permet de lisser les achats au fil du temps, en achetant plus de métal lorsque les prix sont bas et moins lorsqu'ils sont élevés. La DCA réduit le risque d'acheter au plus haut du marché et élimine le besoin d'un timing parfait du marché."
                    ),
                    html.Li(className="mt-3", children=[
                        html.Span("Mais ...", className="fw-bold"),
                        "Bien que la DCA soit un outil précieux pour de nombreuses classes d'actifs, elle peut être moins efficace pour les métaux précieux physiques en raison des coûts supplémentaires liés aux primes, à l'expédition et à l'assurance pour chaque transaction. Des achats plus importants et moins fréquents pourraient être plus rentables pour l'acquisition de métal physique.",
                    ]),
                ], className="list-unstyled"),

                html.H3("Investissement axé sur les objectifs", className="display-7 mt-4 mb-3 fw-bold"),

                html.Ul([
                    html.Li(
                        "L'investissement axé sur les objectifs consiste à fixer des objectifs spécifiques pour les avoirs en métaux précieux, tels que l'accumulation d'un certain nombre d'onces d'or ou d'une valeur particulière d'argent. Cette stratégie fournit un objectif clair et peut être motivante pour les investisseurs."
                    ),
                    html.Li(className="mt-3", children=[
                        html.Span("Mais ...", className="fw-bold"),
                        "Contre-argument : Une fois l'objectif atteint, il existe un risque de perdre le focus ou de se fixer un objectif encore plus élevé, potentiellement irréaliste. L'investissement axé sur les objectifs doit faire partie d'une stratégie plus large et à long terme, et non un objectif isolé.",
                    ]),
                ], className="list-unstyled"),

                html.H2("III. Limites : Équilibre entre risque et rendement",
                        className="display-6 mt-5 mb-4 fw-bold"),

                html.P(
                    "La détermination de la limite d'investissement appropriée pour les métaux précieux dépend de la situation individuelle."
                ),

                html.H3("Aucune limite d'investissement (avec mises en garde)",
                        className="display-7 mt-4 mb-3 fw-bold"),

                html.Ul([
                    html.Li(
                        "Si les métaux précieux constituent le principal véhicule d'épargne d'un individu dont les autres options d'investissement sont limitées, et qu'il a du mal à épargner autrement, il peut ne pas y avoir de limite stricte. Cependant, deux risques importants doivent être pris en compte : les problèmes de sécurité liés au stockage de grandes quantités de métal physique et le risque de dépenses excessives et de négligence d'autres objectifs financiers essentiels."
                    ),
                ], className="list-unstyled"),

                html.H3("Limite d'investissement fixe", className="display-7 mt-4 mb-3 fw-bold"),

                html.Ul([
                    html.Li(
                        "La définition d'une limite fixe, soit sous forme de somme totale, soit sous forme de montant d'investissement périodique, peut fournir une structure et une discipline budgétaire. Cependant, une limite fixe peut devenir non pertinente au fil du temps, à mesure que la situation financière évolue."
                    ),
                ], className="list-unstyled"),

                html.H3("Limite en pourcentage", className="display-7 mt-4 mb-3 fw-bold"),

                html.Ul([
                    html.Li(
                        "Lier la limite d'investissement à un pourcentage de la valeur nette ou des actifs investissables offre une approche dynamique qui s'adapte à l'évolution de la situation financière."
                    ),
                ], className="list-unstyled"),

                html.H3("Limite axée sur les objectifs", className="display-7 mt-4 mb-3 fw-bold"),

                html.Ul([
                    html.Li(
                        "Une limite axée sur les objectifs, comme l'accumulation d'une quantité spécifique d'or ou d'argent, fournit une cible claire, mais elle doit être revue régulièrement et intégrée à une stratégie d'investissement à long terme."
                    ),
                ], className="list-unstyled"),

            ]),  # Close the dbc.Col
        ]),  # Close the dbc.Row
    ])  # Close the dbc.Container