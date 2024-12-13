from dash import html, dcc
import dash_bootstrap_components as dbc

def layout():
    return dbc.Container(fluid=True, children=[
        dbc.Row(justify="center", children=[
            dbc.Col(lg=10, children=[
                html.H1("L'avenir de la monnaie : Métaux précieux, monnaies fiduciaires et cryptomonnaies", className="display-4 text-center mb-4 fw-bold"),

                html.P(
                    "Le système monétaire, pilier fondamental de toute économie, est en constante évolution. De la dépendance historique aux métaux précieux comme l'or et l'argent à la domination actuelle des monnaies fiduciaires gérées par les banques centrales, la forme et la fonction de la monnaie ont subi des transformations significatives. Cet article explore l'avenir de la monnaie, en examinant le système monétaire actuel, en analysant les arguments pour et contre un retour à l'étalon-or, en discutant du rôle potentiel des métaux précieux dans un futur système monétaire et en examinant l'émergence des cryptomonnaies comme force disruptive. Enfin, nous explorerons le concept d'une monnaie décentralisée avec un taux d'inflation prévisible et ses implications potentielles pour l'économie mondiale.",
                    className="lead"
                ),

                html.H2("Le système monétaire actuel : Une analyse approfondie", className="display-6 mt-5 mb-4 fw-bold"),

                html.P(
                    "Le système monétaire mondial actuel est principalement basé sur des monnaies fiduciaires, qui ne sont pas garanties par une marchandise physique comme l'or ou l'argent. Leur valeur découle d'un décret gouvernemental et de la confiance du marché."
                ),

                html.H3("Le rôle des banques centrales", className="display-7 mt-4 mb-3 fw-bold"),

                html.Ul([
                    html.Li(
                        "Les banques centrales, telles que la Réserve fédérale américaine ou la Banque centrale européenne (BCE), jouent un rôle crucial dans la gestion de la masse monétaire, la fixation des taux d'intérêt et agissent en tant que prêteurs en dernier ressort lors des crises financières. Elles utilisent des outils de politique monétaire pour influencer l'inflation, l'emploi et la croissance économique. Grâce à des mécanismes comme le système de réserve fractionnaire et l'assouplissement quantitatif, les banques centrales peuvent augmenter la masse monétaire pour stimuler l'activité économique ou fournir des liquidités en période de stress."
                    ),
                    html.Li(
                        "Contre-argument : Les critiques soutiennent que la capacité des banques centrales à créer de la monnaie sans support tangible peut conduire à une création monétaire excessive, à l'inflation et à des bulles d'actifs. Ils affirment que la déconnexion entre la monnaie et la valeur réelle inhérente aux systèmes fiduciaires crée de l'instabilité et fausse les mécanismes du marché.",
                        className="mt-3"
                    ),
                ], className="list-unstyled"),

                html.H3("Monnaies fiduciaires et augmentation de la masse monétaire", className="display-7 mt-4 mb-3 fw-bold"),

                html.Ul([
                    html.Li(
                        "Les monnaies fiduciaires, contrairement à l'or ou à l'argent, peuvent être créées par les banques centrales par le biais de divers mécanismes. L'assouplissement quantitatif, où les banques centrales achètent des obligations d'État ou d'autres actifs, a conduit à une augmentation spectaculaire de la masse monétaire ces dernières années."
                    ),
                    html.Li(
                        "Argument : Les partisans des monnaies fiduciaires soutiennent que cette flexibilité est nécessaire pour gérer les cycles économiques, stimuler la croissance et répondre aux crises financières. Ils affirment qu'une masse monétaire fixe, comme dans le cadre d'un étalon-or, serait trop restrictive et pourrait conduire à la déflation et à la contraction économique.",
                        className="mt-3"
                    ),
                    html.Li(
                        "Contre-argument : Les critiques soutiennent que l'expansion incontrôlée de la masse monétaire dilue la valeur de la monnaie existante, entraînant l'inflation et l'érosion du pouvoir d'achat. Ils expriment des inquiétudes quant à la durabilité à long terme d'un système basé sur une dette et une création monétaire sans cesse croissantes.",
                        className="mt-3"
                    ),
                ], className="list-unstyled"),

                html.H2("Les cryptomonnaies comme alternative aux monnaies fiduciaires : Une analyse",
                        className="display-6 mt-5 mb-4 fw-bold"),

                html.P(
                    "Les cryptomonnaies, telles que Bitcoin ou Ethereum, sont apparues comme une alternative potentielle aux monnaies fiduciaires, offrant une forme de monnaie décentralisée et numérique."
                ),

                html.H3("Avantages des cryptomonnaies", className="display-7 mt-4 mb-3 fw-bold"),

                html.Ul([
                    html.Li(
                        "Décentralisation : Les cryptomonnaies ne sont pas contrôlées par une autorité centrale, ce qui les rend résistantes à la manipulation ou à la censure gouvernementale."
                    ),
                    html.Li(
                        "Transparence : Les transactions sont enregistrées sur une blockchain publique, améliorant la transparence et la vérifiabilité.",
                        className="mt-3"
                    ),
                    html.Li(
                        "Sécurité : Les techniques cryptographiques sécurisent les transactions et protègent contre la fraude.",
                        className="mt-3"
                    ),
                    html.Li(
                        "Frais de transaction moins élevés : Les transactions en cryptomonnaies peuvent avoir des frais moins élevés que les systèmes bancaires traditionnels, en particulier pour les transferts internationaux.",
                        className="mt-3"
                    ),
                ], className="list-unstyled"),

                html.H3("Inconvénients des cryptomonnaies", className="display-7 mt-4 mb-3 fw-bold"),

                html.Ul([
                    html.Li(
                        "Volatilité : Les prix des cryptomonnaies sont notoirement volatils, ce qui en fait un investissement risqué."
                    ),
                    html.Li(
                        "Évolutivité : De nombreuses cryptomonnaies sont confrontées à des défis pour s'adapter à un volume important de transactions.",
                        className="mt-3"
                    ),
                    html.Li(
                        "Réglementation : Le cadre réglementaire des cryptomonnaies est encore en évolution et varie d'une juridiction à l'autre, créant de l'incertitude pour les investisseurs et les entreprises.",
                        className="mt-3"
                    ),
                    html.Li(
                        "Risques de sécurité : Bien que la blockchain elle-même soit sécurisée, les portefeuilles et les plateformes d'échange individuels sont vulnérables au piratage et au vol.",
                        className="mt-3"
                    ),
                ], className="list-unstyled"),

                html.H2("Monnaie décentralisée avec inflation prévisible : Explorer le concept",
                        className="display-6 mt-5 mb-4 fw-bold"),

                html.P(
                    "Un concept qui gagne du terrain est celui d'une monnaie numérique décentralisée avec un taux d'inflation intégré et prévisible. Cette approche vise à combiner les avantages de la décentralisation avec une plus grande stabilité des prix."
                ),

                html.Ul([
                    html.Li(
                        "Inflation prévisible : Un taux d'inflation prédéterminé, potentiellement lié à des facteurs tels que la croissance démographique ou la production économique, pourrait atténuer les risques déflationnistes associés à une masse monétaire fixe tout en évitant l'inflation imprévisible des monnaies fiduciaires."
                    ),
                    html.Li(
                        "Contrôle décentralisé : Des mécanismes de gouvernance décentralisés pourraient garantir la transparence et la responsabilité, empêchant la manipulation par une autorité centrale.",
                        className="mt-3"
                    ),
                    html.Li(
                        "Monnaie programmable : Les contrats intelligents sur une blockchain pourraient automatiser la politique monétaire et permettre des instruments financiers innovants.",
                        className="mt-3"
                    ),
                ], className="list-unstyled"),

                # ... (The rest of the article with the same styling pattern) ...

            ]),  # Close the dbc.Col
        ]),  # Close the dbc.Row
    ])  # Close the dbc.Container