from dotenv import load_dotenv
load_dotenv()

from scraping.dashboard.pieces import weights

import os
import pandas as pd
import sshtunnel
import pytz
import datetime

from scipy.optimize import minimize
from math import floor

from sqlalchemy import func
import dash
from dash import dcc, html, Input, Output, State, callback_context
import dash_bootstrap_components as dbc
from articles import article1, article2, article3, article4, article5, article6, article7, article8, article9

from flask import Flask, request, session, send_from_directory
from flask_sqlalchemy import SQLAlchemy

server = Flask(__name__)

server.config['SQLALCHEMY_POOL_PRE_PING'] = True
server.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY')
server.config['SSH_HOST'] = os.getenv('SSH_HOST')
server.config['SSH_USERNAME'] = os.getenv('SSH_USERNAME')
server.config['SSH_PASSWORD'] = os.getenv('SSH_PASSWORD')
server.config['REMOTE_BIND_ADDRESS'] = os.getenv('REMOTE_BIND_ADDRESS')
server.config['REMOTE_PORT_ADDRESS'] = int(os.getenv('REMOTE_PORT_ADDRESS', 3306))
sshtunnel.SSH_TIMEOUT = float(os.getenv('SSH_TIMEOUT', 3600.0))
sshtunnel.TUNNEL_TIMEOUT = float(os.getenv('TUNNEL_TIMEOUT', 3600.0))

def create_tunnel():
    return sshtunnel.SSHTunnelForwarder(
        (os.getenv('SSH_HOST')),
        ssh_username=os.getenv('SSH_USERNAME'),
        ssh_password=os.getenv('SSH_PASSWORD'),
        remote_bind_address=(os.getenv('REMOTE_BIND_ADDRESS'), int(os.getenv('REMOTE_PORT_ADDRESS', 3306)))
    )

tunnel = create_tunnel()
tunnel.start()

### DATABASE CONNECTION AND MODELS #####################################################################################

# Configuration using environment variables
server.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI').format(tunnel.local_bind_port)
server.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle' : 280}
db = SQLAlchemy(server)

def query_to_dict(rset):
    """
    Converts a SQLAlchemy query result set to a pandas.Dataframe compatible dictionary .

    Args:
        rset: The result set from a SQLAlchemy query.

    Returns:
        A dictionary where keys are column names and values are lists of column values.
    """
    if not rset:
        return {}  # Return an empty dictionary if the result set is empty

    # Get column names from the first result object
    column_names = [column.name for column in rset[0].__table__.columns]

    # Construct the dictionary using list comprehensions
    return {
        column_name: [getattr(row, column_name) for row in rset]
        for column_name in column_names
    }

class Item(db.Model):
    __tablename__ = 'item'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=True, index=True)
    price_ranges = db.Column(db.String(255), nullable=True)
    sell = db.Column(db.Float, nullable=True)
    quantity = db.Column(db.Integer, nullable=False)
    minimum = db.Column(db.Integer, nullable=True)
    buy_premiums = db.Column(db.String(2000), nullable=True)
    delivery_fees = db.Column(db.String(2000), nullable=True)
    source = db.Column(db.String(1024), nullable=False)
    timestamp = db.Column(db.DateTime)
    session_id = db.Column(db.String(36), index=True)
    bullion_type = db.Column(db.String(2), nullable=True, index=False)

    @classmethod
    def get_items_by_bullion_type_and_quantity(cls, bullion_type, session_id, quantity):
        """
        Fetches items from the database that match the given bullion type, session_id and quantity.

        Args:
            session: SQLAlchemy session object.
            bullion_type: The type of bullion.
            session_id: The session ID.
            quantity: The desired quantity.

        Returns:
            A list of Item objects that match the criteria.
        """
        res = query_to_dict(
            db.session.query(cls)
            .filter(
                cls.bullion_type == bullion_type,
                cls.session_id == session_id,
                cls.minimum <= quantity,
                cls.quantity <= quantity,
            )
            .all()
        )
        db.session.close()
        return res

class MetalPrice(db.Model):
    __tablename__ = 'metal_price'
    id = db.Column(db.Integer, primary_key=True)
    buy_price = db.Column(db.Float, nullable=True)
    sell_price = db.Column(db.Float, nullable=True)
    timestamp = db.Column(db.DateTime)
    session_id = db.Column(db.String(36), index=True)
    bullion_type = db.Column(db.String(2), nullable=True, index=True)

    @classmethod
    def get_previous_price(cls, bullion_type):
        """
        Fetches the metal price for the specified bullion type from the previous session.

        Args:
            session: SQLAlchemy session object.
            bullion_type: The type of bullion.

        Returns:
            The result of the query.
        """

        france_timezone = pytz.timezone('Europe/Paris')
        now_france = datetime.datetime.now(france_timezone)
        thirty_minutes_ago = now_france - datetime.timedelta(minutes=30)

        subquery = (
            db.session.query(cls.session_id)
            .group_by(cls.session_id)
            .having(db.func.max(cls.timestamp) < thirty_minutes_ago)
            .order_by(db.func.max(cls.timestamp).desc())
            .limit(1)
        ).subquery()

        query = (
            db.session.query(cls)
            .filter(
                cls.bullion_type == bullion_type,
                cls.session_id == subquery.c.session_id
            )
        )
        db.session.close()
        return query_to_dict(query.all())

class UserChoice(db.Model):
    __tablename__ = 'user_choices'

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime)
    budget_min = db.Column(db.Float)
    budget_max = db.Column(db.Float)
    quantity = db.Column(db.Integer)
    bullion_type = db.Column(db.String(2))
    selected_coins = db.Column(db.JSON)  # Store selected coins as JSON

class PrecalculatedOffer(db.Model):  # Inherit from Item Base
    __tablename__ = 'precalculated_offer'
    id = db.Column(db.Integer, primary_key=True)  # Own primary key
    timestamp = db.Column(db.DateTime)
    budget_min = db.Column(db.Float)
    budget_max = db.Column(db.Float)
    quantity = db.Column(db.Integer)
    bullion_type = db.Column(db.String(2))
    name = db.Column(db.String(255))
    source = db.Column(db.String(1024))
    premium = db.Column(db.Float)  # Assuming premium is a single float value
    price_per_coin = db.Column(db.Float)
    delivery_fees = db.Column(db.Float)
    total_cost = db.Column(db.Float)

#### INSTANCE OF DASH APP ##############################################################################################

app = dash.Dash(__name__,
                server=server,
                title="Bullion Sniper",
                external_stylesheets=[dbc.themes.DARKLY,'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css'],
                suppress_callback_exceptions=True,
                assets_folder='assets',
                meta_tags=[
                    {"name": "language", "content": "fr"},
                    {"name": "title", "content": "Bullion Sniper"},
                    {"property": "og:title", "content": "Bullion Sniper"},  # For social media sharing
                    {"name": "description",
                     "content": "Trouver facilement les meilleurs offres de pièces d'investissement en ligne."},
                    {"property": "og:description",
                     "content": "Trouver facilement les meilleurs offres de pièces d'investissement en ligne."},
                    {"name": "keywords",
                     "content": "pièces d'investissement, or, argent, lingots, achat, vente, bullion, investissement, métaux précieux"},
                ]
            )

#### UTILS #############################################################################################################
# Your get_price function
def get_price(ranges, quantity):
    """
    Calculates the price based on the quantity and given ranges.

    Args:
    ranges: A string of ranges in the format '1-9-302.0;10-48-300.0;...'.
    quantity: The quantity of the item.

    Returns:
    The price as a float.
    """
    ranges = ranges.split(';')
    for r in ranges:
        try:
            lower, upper, price = map(float, r.split('-'))
        except ValueError as e:
            print(ranges)
            print(r, lower, upper, price)
            raise Exception
        if lower <= quantity < upper:
            return price
    return None

# Objective function (negative number of coins to minimize)
def objective_function(x):
    return -x[0]  # Access the first element of the array x

def constraint(x, budget, price_ranges, delivery_fee_ranges):

    price_per_coin_ = lambda x: get_price(price_ranges, x)
    delivery_fees_ = lambda x: get_price(delivery_fee_ranges, x * price_per_coin_(x))

    price = price_per_coin_(x[0])

    delivery_fee = delivery_fees_(x[0])  # Calculate delivery_fee only after checking price

    if delivery_fee is None:
        return 0  # Return 0 if delivery_fee is None

    return budget - (x[0] * price + delivery_fee)

# Function to find the maximum coins
def find_max_coins(max_quantity, max_budget, price_ranges, delivery_fee_ranges,minimum):
    # Initial guess for x (can be improved)
    x0 = pd.Series(max([1,minimum]))

    constraint_dict = [
        {'type': 'ineq', 'fun': lambda x: constraint(x, max_budget, price_ranges, delivery_fee_ranges)},
    ]
    # Perform numerical optimization using minimize
    result = minimize(
        objective_function,
        x0,
        bounds=[(minimum, max_quantity)],  # Set the lower bound to the minimum
        constraints=constraint_dict,
        method='SLSQP'
    )

    floor_max = floor(result.x[0])  # Access the solution from result.x[0]
    if result.x[0]-floor_max > 0.9:
        return int(round(result.x[0]))
    else:
        return floor_max

def get_country_flag_image(country_code):
    """
    Generates an HTML img tag for a country flag image from a 2-letter country code.
    Uses images from the provided URL with the format "https://hatscripts.github.io/circle-flags/flags/{code}.svg".
    """
    if len(country_code) == 2:
        return html.Img(
            src=f"/assets/{country_code.lower()}.svg",  # Use assets folder
            alt=country_code,
            style={'width': '20px', 'margin-right': '5px'}
        )
    else:
        return ""

#### NAVIGATION ########################################################################################################
# Define the navigation bar
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Tableau de bord", href="/", id="nav-home")),
        #dbc.NavItem(dbc.NavLink("FAQ", href="/faq", id="nav-faq")),
        dbc.DropdownMenu(
            label="Articles Métaux Précieux",
            children=[
                dbc.DropdownMenuItem("1. Fondamentaux", href="/articles/1-fondamentaux",id="nav-article1"),
                dbc.DropdownMenuItem("2. Compléments", href="/articles/2-complements",id="nav-article2"),
                dbc.DropdownMenuItem("3. Argent", href="/articles/3-argent",id="nav-article3"),
                dbc.DropdownMenuItem("4. Fiscalité", href="/articles/4-fiscalite",id="nav-article4"),
                dbc.DropdownMenuItem("5. Diversification", href="/articles/5-diversification",id="nav-article5"),
                dbc.DropdownMenuItem("6. Biais", href="/articles/6-biais",id="nav-article6"),
                dbc.DropdownMenuItem("7. Contrefaçons", href="/articles/7-contrefaçon",id="nav-article7"),
                dbc.DropdownMenuItem("8. Avenir Monnaie", href="/articles/8-avenir-monnaie",id="nav-article8"),
                dbc.DropdownMenuItem("9. Étude de cas", href="/articles/9-etude-de-cas",id="nav-article9"),
            ],
            nav=True,
            in_navbar=True,
            id="nav-article"
        ),

        #dbc.NavItem(dbc.NavLink("Analyse Prime Napoléon d'Or", href="/analyse-prime-napoleon-d-or", id="nav-analyse")),
        #dbc.NavItem(dbc.NavLink("Qui suis je ?", href="/qui-suis-je", id="nav-whoami")),
        # Add more navigation items as needed
    ],
    brand="",  # Your app's brand name
    brand_href="/",  # Link for the brand name
    color="dark",  # Background color
    dark=True,  # Use dark text color
    className="mb-4",  # Add margin-bottom for spacing
    style={"paddingTop": "0","paddingBottom": "0"},  # Add margin-bottom for spacing
)

header = dbc.Row([html.Img(src='/assets/logo-bullion-sniper.webp', style={'height': '150px', 'width': '450px'}),
             html.Div(  # Add the text here
                 "Votre comparateur de prix  pour l'investissement dans les métaux précieux.",
                 className='mb-4 mt-4', style={'textAlign': 'center', 'fontSize': '16px', 'font-weight' : 'bold','color': 'gold'}
             ),
             html.Div(  # Add the text here
                 "100% Indépendant, 0% Affiliation. Plus de 20 plateformes recensées chaque jour.",
                 className='mb-1 mt-1',style={'textAlign': 'center', 'fontSize': '16px', 'font-weight' : 'bold','color': 'gold'}
             ),], className="mb-4 mt-1",justify="center")
footer = html.Div([
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dbc.Card(
                            [
                                dbc.CardHeader(
                                    [
                                        html.I(className="fa-solid fa-circle-exclamation fa-beat-fade", style={'fontSize': '22px'}),
                                        "  Bullion-sniper.fr ne donne pas de conseils en investissement.",

                                    ],
                                ),
                                dbc.CardBody([
                                "Nous attachons un soin particulier à créer et entretenir le présent site et à veiller à l’exactitude et à l’actualité de son contenu.",html.Br(),html.Br(), "Néanmoins, les éléments présentés dans ce site sont susceptibles de modifications fréquentes sans préavis. Bullion-sniper.fr ne garantit pas l’exactitude et l’actualité du contenu du site. Les éléments présentés Bullion-sniper.fr sont mis à disposition des utilisateurs sans aucune garantie d’aucune sorte et ne peuvent donner lieu à un quelconque droit à dédommagement.",
                            ])], style={'textAlign': 'center'}
                            )
                        ],
                        width=12)
                ], className="mb-4 mt-4",justify="center"),

            html.Div([
                "2025 - Bullion-sniper.fr x ",
                html.A("Dash ",href="https://dash.plotly.com/"),
                html.I(className="fa-solid fa-heart fa-beat", style={'fontSize': '16px', 'color' : 'red'}),], className="text-center mb-2"),
        ], id="footer-content")

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    navbar,
    header,
    dbc.Container(id="page-content", fluid=False),
    dcc.Store(id='initial-load', data=True),
    html.Div(id='google-analytics-container'),
    dcc.Store(id='cookie-consent', storage_type='local'),  # Changed to local storage
    html.Div(
        id='cookie-banner',
        children=[
            html.Div(className="cookie-consent", children=[
                html.Div([
                    html.P("Salut les investisseurs ! 👋"),
                    html.P(
                        "Bullion-Sniper est un site 100% gratuit et sans pub, conçu par un passionné pour vous aider à trouver les meilleures offres. Pour que je puisse continuer à améliorer le site et vous offrir la meilleure expérience possible, j'ai besoin de collecter quelques données anonymes grâce aux cookies."),
                    html.P(
                        "C'est un petit coup de pouce de votre part qui m'aide énormément ! 😊 Acceptez-vous les cookies analytiques pour m'aider à faire grandir Bullion-Sniper ?")
                ],
                    className="cookie-message mb-3 text-center text-white",
                    style={"max-width": "400px", "margin": "0 auto"}
                ),
                dcc.Checklist(
                    id='cookie-checklist',
                    options=[
                        {'label': 'Cookies essentiels', 'value': 'essential'},
                        {'label': 'Cookies analytiques', 'value': 'analytics'}
                    ],
                    value=['essential', 'analytics'],
                    inline=False,
                    inputClassName="form-check-input",
                    labelClassName="form-check-label",
                    className="mb-3"
                ),
                html.Button("Enregistrer mes préférences", id='save-cookie-preferences', n_clicks=0,
                            className="btn btn-warning mt-3")
            ]),
        ],
        style={'display': 'none'}
    )
])

@app.callback(Output("page-content", "children"),
              [Input("url", "pathname"),
               Input("nav-home", "n_clicks"),
               Input("nav-article1", "n_clicks"),
               Input("nav-article2", "n_clicks"),
               Input("nav-article3", "n_clicks"),
               Input("nav-article4", "n_clicks"),
               Input("nav-article5", "n_clicks"),
               Input("nav-article6", "n_clicks"),
               Input("nav-article7", "n_clicks"),
               Input("nav-article8", "n_clicks"),
               Input("nav-article9", "n_clicks"),
               # Input("nav-faq", "n_clicks"),
               # Input("nav-analyse", "n_clicks"),
               # Input("nav-whoami", "n_clicks")
               ])
def render_page_content(pathname, n_clicks_home,
                        n_clicks_article1, n_clicks_article2, n_clicks_article3,
                        n_clicks_article4, n_clicks_article5, n_clicks_article6,
                        n_clicks_article7, n_clicks_article8, n_clicks_article9,
                        #n_clicks_faq, n_clicks_analyse,n_clicks_whoami
                        ):

    ctx = callback_context
    triggered_id, _ = ctx.triggered[0]['prop_id'].split('.')

    if triggered_id == "url" or triggered_id == "nav-home":
        return serve_dashboard()
    elif pathname.startswith("/articles/"):  # Check if the path starts with "/articles/"
        if triggered_id == "nav-article1" or pathname == "/articles/1-fondamentaux":
            return article1.layout()
        elif triggered_id == "nav-article2" or pathname == "/articles/2-complements":
            return article2.layout()
        elif triggered_id == "nav-article3" or pathname == "/articles/3-argent":
            return article3.layout()
        elif triggered_id == "nav-article4" or pathname == "/articles/4-fiscalite":
            return article4.layout()
        elif triggered_id == "nav-article5" or pathname == "/articles/5-diversification":
            return article5.layout()
        elif triggered_id == "nav-article6" or pathname == "/articles/6-biais":
            return article6.layout()
        elif triggered_id == "nav-article7" or pathname == "/articles/7-contrefaçon":
            return article7.layout()
        elif triggered_id == "nav-article8" or pathname == "/articles/8-avenir-monnaie":
            return article8.layout()
        elif triggered_id == "nav-article9" or pathname == "/articles/9-etude-de-cas":
            return article9.layout()
    # elif triggered_id == "nav-faq" or pathname == "/faq":
    #     return html.Div([
    #         html.H1("FAQ"),
    #         html.P("Voici les questions fréquemment posées :"),
    #         html.Ul([
    #             html.Li("Question 1 ? Réponse 1."),
    #             html.Li("Question 2 ? Réponse 2."),
    #             html.Li("Question 3 ? Réponse 3."),
    #             # ... add more FAQ items
    #         ])
    #     ])
    # elif triggered_id == "nav-analyse" or pathname == "/analyse-prime-napoleon-d-or":
    #     return serve_analysis()
    # elif triggered_id == "nav-whoami" or pathname == "/qui-suis-je":
    #     return html.Div([
    #         html.H1("Qui suis je ?"),
    #         html.P("Je suis un passionné de métaux précieux et j'ai créé ce site pour partager mes connaissances et mes analyses."),
    #         # ... add more information about yourself
    #     ])
    else:
        return html.Div([
            html.H1("404: Page non trouvée"),
            html.P("La page que vous recherchez n'existe pas."),
        ])

@server.route('/sitemap.xml')
def send_sitemap():
    return send_from_directory(server.root_path, "assets/sitemap.xml")

@server.route('/ads.txt')
def serve_ads_txt():
    return send_from_directory(server.root_path, 'assets/ads.txt')

#### DASHBOARD #########################################################################################################
def serve_dashboard():
    options = [{'label': f'{i}', 'value': i} for i in range(1, 150)]
    options.insert(0, {'label': 'Pas de limite', 'value': 9999999999})
    return (
        dbc.Container([
            dbc.Row([
                dbc.Col(
                    dbc.Card([
                        dbc.CardHeader([html.I(className="fa-solid fa-bullseye fa-bounce", style={'fontSize': '16px'}),"  Mon budget (€)",dbc.Tooltip("Le budget que je souhaite me fixer.", target="cardheader-budget")],style = {'textAlign': 'center'}),
                        dbc.CardBody([
                            dcc.RangeSlider(
                                id='budget-slider',
                                min=0,
                                max=20000,
                                step=100,
                                value=[0, 2000],  # Default range
                                marks={
                                    0: '0 €',
                                    20000: '20k €',
                                },
                                allowCross=False,
                                persistence=False,
                                tooltip={"placement": "bottom", "always_visible": True,"style": {"color": "gold", "fontSize": "14px"}},
                                updatemode='mouseup',# Show tooltip always
                            )
                        ],id="cardheader-budget"),
                    ]),
                    xs=12, sm=12, md=6, lg=6, xl=6,xxl=7, className="mb-4"  # Adjust width for larger screens
                ),
                dbc.Col(
                    dbc.Card([
                        dbc.CardHeader([html.I(className="fa-sharp fa-solid fa-coins fa-bounce", style={'fontSize': '16px'}),"  Quantité max.",dbc.Tooltip("Le nombre maximum de pièces que je souhaite acheter.", target="cardheader-quantity")],style = {'textAlign': 'center'}),
                        dbc.CardBody([
                            dcc.Dropdown(
                                id='quantity-value',
                                options=options,
                                multi=False,
                                value=9999999999,  # No default selection
                                clearable=False,  # Allow clearing the selection
                                style={'width': '100%', 'color': 'black', 'textAlign': 'center'}
                            ),
                        ],id="cardheader-quantity"),
                    ]),
                    xs=6, sm=6, md=3, lg=3, xl=3,xxl=3,className="mb-4"
                ),

                dbc.Col(
                    dbc.Card([
                        dbc.CardHeader([html.I(className="fa-solid fa-cube", style={'fontSize': '16px'}),"  Bullion", dbc.Tooltip("Source cours du métal : BullionVault.", target="cardheader-bullion")], style={'textAlign': 'center'}),
                        dbc.CardBody([
                            html.Div(
                                [
                                    html.Span("Argent", className="me-2"),
                                    dbc.Switch(
                                        id='bullion-type-switch',
                                        label="",
                                        value=True,
                                        className="gold-silver-switch larger-switch",
                                        persistence=False,
                                    ),
                                    html.Span("Or", className="ms-2"),
                                ],
                                className="d-flex align-items-center justify-content-between"  # No need for width: 100% here
                            )
                        ,html.Div(id='metal-price-output'),
                        ],id="cardheader-bullion")
                    ],                # The tooltip
                    ),  # Set a fixed width for the Card
                    xs=6, sm=6, md=3, lg=3, xl=2,xxl=2, className="mb-4"
                ),
                dbc.Col(
                    dbc.Card([
                        dbc.CardHeader([html.I(className="fa-solid fa-magnifying-glass", style={'fontSize': '16px'}), "  Effigie/Année", dbc.Tooltip("Je récupère les offres pour un ou plusieurs types de pièce.", target="cardheader-years")], style={'textAlign': 'center'}),  # New card for name selection
                        dbc.CardBody([
                            dcc.Dropdown(
                                id='piece-dropdown',
                                options=[],
                                multi=True,
                                value=None,  # No default selection
                                placeholder="Sélectionnez une pièce",  # Placeholder text
                                clearable=True,  # Allow clearing the selection
                                style={'width': '100%', 'color': 'black', 'textAlign': 'center'}
                            ),
                        ]),
                    ],id="cardheader-years"),
                    xs=12, sm=12, md=8, lg=6, xl=4, xxl=4, className="mb-4"
                ),
            ], className="mb-4 equal-height-cards"),  # Add margin-bottom to the row
            dbc.Spinner(id="loading-output", children=[
                html.Div(id='last-update-info', className="text-center mb-2"),  # Add a div to display the last update info

                dbc.Table([  # Create the table structure in the layout
                    html.Thead(
                        html.Tr([
                            html.Th([html.I(className="fa-solid fa-shop", style={'fontSize': '16px'}), "  Site marchand",
                                     html.Span(id='source-arrow', className="fa fa-sort ms-2")], style={'textAlign': 'center'},
                                    id='source-header', n_clicks=0),
                            html.Th([html.I(className="fa-solid fa-hashtag", style={'fontSize': '16px'}), "  Nom",
                                     html.Span(id='name-arrow', className="fa fa-sort ms-2")], style={'textAlign': 'center'},
                                    id='name-header', n_clicks=0),
                            html.Th(
                                [
                                    html.I(className="fa-solid fa-arrow-trend-down", style={'fontSize': '16px'}),
                                    "  Prime",
                                    html.Span(id='premium-arrow', className="fa fa-sort ms-2"),
                                    dbc.Tooltip(
                                        "La prime inclue les frais de port et le prix dégressif. Valable uniquement à l'horaire affichée ci-dessus.",
                                        target="premium-header")  # The tooltip
                                ],
                                id="premium-header",
                                style={'textAlign': 'center'}, n_clicks=0),
                            html.Th(
                                [
                                    html.I(className="fa-solid fa-circle-info", style={'fontSize': '16px'}),
                                    "  Prix Unitaire FDPI",
                                    html.Span(id='ppc-arrow', className="fa fa-sort ms-2"),
                                    dbc.Tooltip("Prix unitaire, frais de port inclus, d'une pièce du lot.", target="ppc-header")
                                ],
                                id="ppc-header",
                                style={'textAlign': 'center'}, n_clicks=0),
                            html.Th(
                                [
                                    html.I(className="fa-solid fa-chart-line", style={'fontSize': '16px'}),
                                    "  Quantité",
                                    html.Span(id='quantity-arrow', className="fa fa-sort ms-2"),
                                    dbc.Tooltip("Quantité minimum pour obtenir la prime affichée.", target="quantity-header")
                                ],
                                id="quantity-header",
                                style={'textAlign': 'center'}, n_clicks=0),
                            html.Th([html.I(className="fa-solid fa-tag", style={'fontSize': '16px'}), "  Total FDPI",
                                     html.Span(id='total_cost-arrow', className="fa fa-sort ms-2"), ],
                                    style={'textAlign': 'center'}, id='total_cost-header', n_clicks=0),

                            html.Th([html.I(className="fa-solid fa-truck fa-tag", style={'fontSize': '16px'}), "  FDP",
                                     html.Span(id='delivery-arrow', className="fa fa-sort ms-2"), ],
                                    style={'textAlign': 'center'}, id='delivery-header', n_clicks=0),

                        ])
                        , id='table-header'),  # Apply spinner only to the tbody
                    html.Tbody(id='cheapest-offer-table-body'),
                ], bordered=True, hover=True, responsive=True, striped=True, dark=True),


            dcc.Interval(
                id='interval-component',
                interval=30*60*1000,  # in milliseconds (30 minutes)
                n_intervals=0
            ),

            dcc.Loading(id="loading-1",type="default",children=html.Div(id="tawk-to-widget")),
            footer,
            ],  color="gold", type="border", spinner_style={"position": "absolute", "top": "3em"}),

            ]))

# #### DASHBOARD CALLBACKS ###############################################################################################
@app.callback(
    Output('cheapest-offer-table-body', 'children'),
    Output('last-update-info', 'children'),
    Output('source-arrow', 'className'),  # Output for the arrow icon's className
    Output('name-arrow', 'className'),  # Output for the arrow icon's className
    Output('premium-arrow', 'className'),  # Output for the arrow icon's className
    Output('quantity-arrow', 'className'),  # Output for the arrow icon's className
    Output('ppc-arrow', 'className'),  # Output for the arrow icon's className
    Output('total_cost-arrow', 'className'),
    Output('delivery-arrow', 'className'),
    Output('initial-load', 'data'),
    [Input('budget-slider', 'value'),
     Input('quantity-value', 'value'),
     Input('bullion-type-switch', 'value'),
     Input('piece-dropdown', 'value'),
     Input('interval-component', 'n_intervals'),
     Input('source-header', 'n_clicks'),  # Input for each header's n_clicks
     Input('name-header', 'n_clicks'),
     Input('premium-header', 'n_clicks'),
     Input('ppc-header', 'n_clicks'),
     Input('quantity-header', 'n_clicks'),
     Input('total_cost-header', 'n_clicks'),
     Input('delivery-header', 'n_clicks'),
     Input('initial-load', 'data')],  # Add the dcc.Store as input
    [State('cheapest-offer-table-body', 'children'),
     State('source-arrow', 'className'),  # Add states for the arrow class names
     State('name-arrow', 'className'),
     State('premium-arrow', 'className'),
     State('ppc-arrow', 'className'),
     State('quantity-arrow', 'className'),
     State('total_cost-arrow', 'className'),
     State('delivery-arrow', 'className')]
)
def update_and_sort_table(budget_range, quantity, bullion_type_switch, selected_coins, n,
                          source_clicks, name_clicks, premium_clicks, ppc_clicks, quantity_clicks, total_cost_clicks, delivery_clicks,
                          initial_load,current_table, source_arrow, name_arrow, premium_arrow, ppc_arrow,quantity_arrow, total_cost_arrow, delivery_arrow,
                          ):
    ctx = callback_context
    triggered_id, triggered_prop = ctx.triggered[0]['prop_id'].split('.')

    # Initialize arrow class names
    arrow_classNames = {
        'source-arrow': "fa fa-sort ms-2",
        'name-arrow': "fa fa-sort ms-2",
        'premium-arrow': "fa fa-sort ms-2",
        'ppc-arrow': "fa fa-sort ms-2",
        'quantity-arrow': "fa fa-sort ms-2",
        'total_cost-arrow': "fa fa-sort ms-2",
        'delivery-arrow': "fa fa-sort ms-2"
    }

    if initial_load:
        # 2. Fetch pre-calculated offers from the database

        bullion_type = 'or' if bullion_type_switch else 'ar'
        france_timezone = pytz.timezone('Europe/Paris')
        now_france = datetime.datetime.now(france_timezone)
        thirty_minutes_ago = now_france - datetime.timedelta(minutes=30)

        results = MetalPrice.get_previous_price(bullion_type)
        metal_prices_df = pd.DataFrame(results)

        metal_price = metal_prices_df['buy_price'].iloc[0]
        session_id = metal_prices_df['session_id'].iloc[0]
        latest_timestamp = metal_prices_df['timestamp'].iloc[0]
        formatted_timestamp = latest_timestamp.strftime('%d/%m/%Y à %Hh%M.')

        precalculated_offers = db.session.query(PrecalculatedOffer).all()

        # 3. Create table rows from pre-calculated offers
        table_rows = []
        for offer in precalculated_offers:
            table_rows.append(
                html.Tr([
                    html.Td(html.A(html.I(className="fas fa-external-link-alt", style={'color': 'gold'}),
                                   href=offer.source, target="_blank",
                                   style={'textDecoration': 'none', 'text_align': 'center'}),
                            style={'textAlign': 'center'}),
                    html.Td(offer.name[4:]),
                    html.Td(f"{offer.premium:.2f}",style={'textAlign': 'center'}),
                    html.Td(f"{offer.price_per_coin:.2f} €",style={'textAlign': 'center'}),
                    html.Td(offer.quantity,style={'textAlign': 'center'}),
                    html.Td(f"{offer.total_cost:.2f} €",style={'textAlign': 'center'}),
                    html.Td(f"{offer.delivery_fees:.2f} €",style={'textAlign': 'center'})
                ])
            )
        return (table_rows, html.P(f"Dernière mise à jour le {formatted_timestamp}", style={'fontSize': '0.8em'}),
                arrow_classNames['source-arrow'], arrow_classNames['name-arrow'],
                arrow_classNames['premium-arrow'], arrow_classNames['quantity-arrow'], arrow_classNames['ppc-arrow'],
                arrow_classNames['total_cost-arrow'],arrow_classNames['delivery-arrow'], False)

    if triggered_prop == 'n_clicks':
        # if triggered_id == 'source-header':
        #     column_index = 0
        #     sort_key = 'source'
        if triggered_id == 'name-header':
            column_index = 1
            sort_key = 'name'
        elif triggered_id == 'premium-header':
            column_index = 2
            sort_key = 'premium'
        elif triggered_id == 'ppc-header':
            column_index = 3
            sort_key = 'ppc'
        elif triggered_id == 'quantity-header':
            column_index = 4
            sort_key = 'quantity'
        elif triggered_id == 'total_cost-header':
            column_index = 5
            sort_key = 'total_cost'
        elif triggered_id == 'delivery-header':
            column_index = 6
            sort_key = 'delivery_fees'

        if sort_key == 'total_cost':
            # Extract numeric values from the 'Total FDPI (€)' column
            numeric_values = []
            for row in current_table:
                try:
                    value = row['props']['children'][column_index]['props']['children']
                    numeric_value = float(value.replace('€', '').replace(',', '').strip())
                    numeric_values.append(numeric_value)
                except (IndexError, KeyError, TypeError, ValueError):
                    numeric_values.append(None)  # Append None for invalid values

            # Create a temporary DataFrame for sorting
            df_temp = pd.DataFrame({'original_order': current_table, 'numeric_values': numeric_values})

            # Determine current sorting order for 'total_cost'
            ascending = True
            if df_temp.equals(df_temp.sort_values(by='numeric_values')):
                ascending = False

            df_temp.sort_values(by='numeric_values', ascending=ascending, inplace=True)

            # Update current_table with the sorted rows
            current_table = df_temp['original_order'].tolist()

        else :
            ascending = True
            current_order = sorted(current_table,
                                   key=lambda x: x['props']['children'][column_index]['props']['children'])
            if current_table == current_order:
                ascending = False

            current_table.sort(key=lambda x: x['props']['children'][column_index]['props']['children'], reverse=not ascending)

            # Update the arrow icon class
        arrow_icon_id = f'{sort_key}-arrow'  # Construct the arrow icon ID
        arrow_classNames[arrow_icon_id] = "fa fa-sort-down ms-2" if ascending else "fa fa-sort-up ms-2"

        return (current_table, dash.no_update, arrow_classNames['source-arrow'], arrow_classNames['name-arrow'],
                arrow_classNames['premium-arrow'], arrow_classNames['quantity-arrow'], arrow_classNames['ppc-arrow'],
                arrow_classNames['total_cost-arrow'],arrow_classNames['delivery-arrow'], False)
    else :

        bullion_type = 'or' if bullion_type_switch else 'ar'
        france_timezone = pytz.timezone('Europe/Paris')
        now_france = datetime.datetime.now(france_timezone)
        thirty_minutes_ago = now_france - datetime.timedelta(minutes=30)

        user_choice = UserChoice(
            timestamp=datetime.datetime.now(),
            budget_min=budget_range[0],
            budget_max=budget_range[1],
            quantity=quantity,
            bullion_type='or' if bullion_type_switch else 'ar',
            selected_coins=selected_coins if selected_coins else []
        )
        db.session.add(user_choice)
        db.session.commit()

        results = MetalPrice.get_previous_price(bullion_type)
        metal_prices_df = pd.DataFrame(results)

        metal_price = metal_prices_df['buy_price'].iloc[0]
        session_id = metal_prices_df['session_id'].iloc[0]
        latest_timestamp = metal_prices_df['timestamp'].iloc[0]
        formatted_timestamp = latest_timestamp.strftime('%d/%m/%Y à %Hh%M.')

        cheapest_offers = []
        seen_offers = set()
        table_rows = []

        # SQL query to fetch the latest complete session and its data from both tables
        results = Item.get_items_by_bullion_type_and_quantity(bullion_type,session_id,quantity)
        items_df = pd.DataFrame(results).copy()

        if selected_coins:
            filtered_df = pd.DataFrame()  # Create an empty DataFrame to store filtered rows
            for coin in selected_coins:
                pattern = coin.replace('(', r'\(').replace(')', r'\)')
                filtered_df = pd.concat([filtered_df, items_df[items_df['name'].str.contains(pattern, regex=True)]])
            items_df = filtered_df  # Update items_df with the filtered DataFrame

        # Pre-process the 'buy_premiums' column before the loops

        budget_min, budget_max = budget_range

        for i, row in items_df.iterrows():

            total_quantity = find_max_coins(quantity,budget_max, row['price_ranges'], row['delivery_fees'],row['minimum'])

            #obligé de retirer les offres inferieur a la quantité, le solveur doit pouvoir descendre en dessous du minimum de pièce pour calculer.
            # if total_quantity < row['minimum']:
            #     continue

            price_per_coin = get_price(row['price_ranges'],total_quantity) / row['quantity']
            delivery_cost = get_price(row['delivery_fees'],price_per_coin*total_quantity)
            ppc_ipc = price_per_coin + (delivery_cost/row['quantity'])
            spot_cost = weights[row['name']] * metal_price
            premium = ppc_ipc - spot_cost
            premium_percentage = (premium / spot_cost) * 100
            total_cost = ppc_ipc * total_quantity * row['quantity']
            if total_cost > budget_max * 1.1 or total_quantity * row['quantity'] > quantity :
                print(row['source'],row['name'])
                continue

            cheapest_offers.append({
                'name': row['name'].upper(),
                'source': row['source'],
                'premium':premium_percentage,
                'price_per_coin': ppc_ipc,
                'quantity': total_quantity if row['quantity'] == 1 else str(total_quantity) + ' x ' + str(row['quantity']) + ' ({total_quantity})'.format(total_quantity=str(total_quantity * row['quantity'])) ,
                'delivery_fees': 0 if get_price(row['delivery_fees'],total_cost) == 0.01 else get_price(row['delivery_fees'],total_cost),
                'total_cost': total_cost
            })

        # Sort offers by premium (lowest first)
        cheapest_offers.sort(key=lambda x: x['premium'])

        for offer in cheapest_offers[:40]:
            table_rows.append(
                html.Tr([
                    html.Td(
                        html.A(
                            html.I(className="fas fa-external-link-alt", style={'color': 'gold'}),  # External link icon
                            href=offer['source'],  # URL of the source
                            target="_blank",  # Open link in a new tab
                            style={'textDecoration': 'none', 'text_align':'center'}  # Remove underline from the link
                        ),
                        style={'textAlign': 'center'}
                    ),
                    html.Td(offer['name'][4:]),
                    html.Td(f"{offer['premium']:.2f}",style={'textAlign': 'center'}),
                    html.Td(f"{offer['price_per_coin']:.2f} €",style={'textAlign': 'center'}),
                    html.Td(offer['quantity'],style={'textAlign': 'center'}),
                    html.Td(f"{offer['total_cost']:.2f} €",style={'textAlign': 'center'}),
                    html.Td(f"{offer['delivery_fees']:.2f} €",style={'textAlign': 'center'})
                ])
            )

        if table_rows == []:
            DEBUG_icon = html.I(className="fas fa-triangle-exclamation", style={'color': 'orange', 'fontSize': '16px'})  # Adjust color and size as needed
            table_rows.append(
                html.Tr([
                    html.Td(DEBUG_icon, style={'textAlign': 'center'}),
                    html.Td("Veuillez augmenter votre budget pour voir les offres."),
                    html.Td(DEBUG_icon, style={'textAlign': 'center'}),
                    html.Td(DEBUG_icon, style={'textAlign': 'center'}),
                    html.Td(DEBUG_icon, style={'textAlign': 'center'}),
                    html.Td(DEBUG_icon, style={'textAlign': 'center'}),
                    html.Td(DEBUG_icon, style={'textAlign': 'center'})
                ])
            )

        return (table_rows,
                html.P(f"Dernière mise à jour le {formatted_timestamp}", style={'fontSize': '0.8em'}),
                arrow_classNames['source-arrow'],
                arrow_classNames['name-arrow'],
                arrow_classNames['premium-arrow'],
                arrow_classNames['quantity-arrow'],
                arrow_classNames['ppc-arrow'],
                arrow_classNames['total_cost-arrow'],
                arrow_classNames['delivery-arrow'],
                False,)

########################################################################################################################
@app.callback(
    Output('piece-dropdown', 'options'),
    Output('piece-dropdown', 'value'),
    [Input('bullion-type-switch', 'value')]
)
def update_piece_dropdown(bullion_type_switch):
    if bullion_type_switch :
        return or_options_quick_filter, None
    else :
        return ar_options_quick_filter, None

@app.callback(
    Output('metal-price-output', 'children'),
    [Input('bullion-type-switch', 'value'),
     Input('interval-component', 'n_intervals')]
)
def update_metal_price(bullion_type_switch, n):
    bullion_type = 'or' if bullion_type_switch else 'ar'

    results = MetalPrice.get_previous_price(bullion_type)
    metal_prices_df = pd.DataFrame(results)

    # Get buying gold and silver coin values
    metal_price = metal_prices_df['buy_price'].iloc[0]

    return html.Div(
        [
            html.Hr(style={'margin': '5px 0'}),  # Add a horizontal rule for separation
            html.P(f"{metal_price:.3f} €/g ", style={'fontSize': '0.8em', 'margin-bottom': '0','textAlign':'center'})
        ]
    )
    return current_table

########################################################################################################################

app.clientside_callback(
        """
        function(n_clicks) {
            setTimeout(function() {
                var s1=document.createElement("script");
                s1.async=true;
                s1.articles='https://embed.tawk.to/673851ed4304e3196ae37e76/1icq0025a';
                s1.charset='UTF-8';
                s1.setAttribute('crossorigin','*');
                document.body.appendChild(s1); // Append to the end of <body>

                document.getElementById("loading-1").style.display = "none"; 
            }, 100); // Adjust the delay as needed

            return "";
        }
        """,
    Output("tawk-to-widget", "children"),
    Input("tawk-to-widget", "n_clicks"),
)

# Clientside callback to manage cookie consent, banner visibility, and Google Analytics
app.clientside_callback(
    """
    function(href, saveClicks, checklistValues) {
        let essentialConsent = localStorage.getItem('essential-cookies');
        let analyticsConsent = localStorage.getItem('analytics-cookies');

        if (saveClicks > 0) {
            localStorage.setItem('essential-cookies', checklistValues.includes('essential'));
            localStorage.setItem('analytics-cookies', checklistValues.includes('analytics'));
            essentialConsent = checklistValues.includes('essential') ? 'true' : 'false';
            analyticsConsent = checklistValues.includes('analytics') ? 'true' : 'false';

            // Inject Google Analytics if consent is given
            if (analyticsConsent === 'true') {
                const scriptId = 'gtag-script';
                if (!document.getElementById(scriptId)) {
                    const script = document.createElement('script');
                    script.id = scriptId;
                    script.src = 'https://www.googletagmanager.com/gtag/js?id=G-DBDM228K9G';
                    document.head.appendChild(script);

                    window.dataLayer = window.dataLayer || [];
                    function gtag(){dataLayer.push(arguments);}
                    gtag('js', new Date());
                    gtag('config', 'G-DBDM228K9G');
                }
            }
        }

        if (essentialConsent === null || analyticsConsent === null) {
            document.getElementById('cookie-banner').style.display = 'block';
        } else {
            document.getElementById('cookie-banner').style.display = 'none';
        }
        return [
            essentialConsent === 'true', 
            analyticsConsent === 'true'
        ];
    }
    """,
    Output('cookie-consent', 'data'),
    Input('url', 'href'),
    Input('save-cookie-preferences', 'n_clicks'),
    Input('cookie-checklist', 'value')
)
########################################################################################################################

with app.server.app_context():
    results = MetalPrice.get_previous_price('or')
    metal_prices_df = pd.DataFrame(results)

    metal_price = metal_prices_df['buy_price'].iloc[0]
    session_id = metal_prices_df['session_id'].iloc[0]
    # SQL query to fetch the latest complete session and its data from both tables
    results = Item.get_items_by_bullion_type_and_quantity('or', session_id, 1)
    items_df = pd.DataFrame(results).copy()

    items_df.drop_duplicates(subset=['name'], inplace=True)
    items_df.sort_values(by='name', inplace=True)
    or_options_quick_filter = [
                                  {'label': html.Span(
                                      [get_country_flag_image('fr'), "Toutes les 20 francs Napoléon d'Or"]),
                                      'value': 'or - 20 francs fr *'},
                                  {'label': html.Span([get_country_flag_image('fr'), "Toutes les 5 francs"]),
                                   'value': 'or - 5 francs fr *'},
                                  {'label': html.Span([get_country_flag_image('fr'), "Toutes les 10 francs"]),
                                   'value': 'or - 10 francs fr *'},
                                  {'label': html.Span([get_country_flag_image('fr'), "Toutes les 40 francs"]),
                                   'value': 'or - 40 francs fr *'},
                                  {'label': html.Span([get_country_flag_image('fr'), "Toutes les 50 francs"]),
                                   'value': 'or - 50 francs fr *'},
                                  {'label': html.Span([get_country_flag_image('fr'), "Toutes les 100 francs"]),
                                   'value': 'or - 100 francs fr *'},
                                  {'label': html.Span([get_country_flag_image('ch'), "Toutes les 20 francs"]),
                                   'value': 'or - 20 francs sui *'},
                                  {'label': html.Span([get_country_flag_image('gb'), "Toutes les 1 souverain"]),
                                   'value': 'or - 1 souverain *'},
                                  {'label': html.Span([get_country_flag_image('gb'), "Toutes les 1/2 souverain"]),
                                   'value': 'or - 1/2 souverain *'},
                                  {'label': html.Span([get_country_flag_image('us'), "Toutes les 2.5 dollars"]),
                                   'value': 'or - 2.5 dollars *'},
                                  {'label': html.Span([get_country_flag_image('us'), "Toutes les 5 dollars"]),
                                   'value': 'or - 5 dollars *'},
                                  {'label': html.Span([get_country_flag_image('us'), "Toutes les 10 dollars"]),
                                   'value': 'or - 10 dollars *'},
                                  {'label': html.Span([get_country_flag_image('us'), "Toutes les 20 dollars"]),
                                   'value': 'or - 20 dollars *'},
                                  {'label': html.Span([get_country_flag_image('mx'), "Toutes les 50 pesos"]),
                                   'value': 'or - 50 pesos *'},
                                  {'label': html.Span([get_country_flag_image('it'), "Toutes les 20 lire"]),
                                   'value': 'or - 20 lire *'},
                                  {'label': html.Span([get_country_flag_image('de'), "Toutes les 20 mark"]),
                                   'value': 'or - 20 mark *'},
                                  {'label': "Toutes les 1 Oz", 'value': 'or - 1 oz*'},
                                  {'label': "Toutes les 1/2 Oz", 'value': 'or - 1/2 oz*'},
                                  {'label': "Toutes les 1/4 Oz", 'value': 'or - 1/4 oz*'},
                                  {'label': "Toutes les 1/10 Oz", 'value': 'or - 1/10 oz*'},
                                  {'label': "Toutes les 1/20 Oz", 'value': 'or - 1/20 oz*'},
                              ] + [{'label': html.Span(row['name'][4:].upper()), 'value': row['name']} for _, row in
                                   items_df.iterrows()]

    results = Item.get_items_by_bullion_type_and_quantity('ar', session_id, 1)
    items_df = pd.DataFrame(results).copy()

    items_df.drop_duplicates(subset=['name'], inplace=True)
    items_df.sort_values(by='name', inplace=True)
    ar_options_quick_filter = [
                                  {'label': html.Span([get_country_flag_image('fr'), "Toutes les 50 Cts francs"]),
                                   'value': 'ar - 50 centimes francs *'},
                                  {'label': html.Span([get_country_flag_image('fr'), "Toutes les 1 franc"]),
                                   'value': 'ar - 1 franc *'},
                                  {'label': html.Span([get_country_flag_image('fr'), "Toutes les 2 francs"]),
                                   'value': 'ar - 2 francs *'},
                                  {'label': html.Span([get_country_flag_image('fr'), "Toutes les 5 francs"]),
                                   'value': 'ar - 5 francs *'},
                                  {'label': html.Span([get_country_flag_image('fr'), "Toutes les 10 francs"]),
                                   'value': 'ar - 10 francs *'},
                                  {'label': html.Span([get_country_flag_image('fr'), "Toutes les 20 francs"]),
                                   'value': 'ar - 20 francs *'},
                                  {'label': html.Span([get_country_flag_image('fr'), "Toutes les 50 francs Hercule"]),
                                   'value': 'ar - 50 francs *'},
                                  {'label': html.Span([get_country_flag_image('fr'), "Toutes les 100 francs Hercule"]),
                                   'value': 'ar - 100 francs *'},
                                  {'label': "Toutes les 1 Oz", 'value': 'ar - 1 oz *'},
                              ] + [{'label': html.Span(row['name'][4:].upper()), 'value': row['name']} for _, row in
                                   items_df.iterrows()]


########################################################################################################################

def serve_analysis():

    return html.Div([
        dbc.Row([
            dbc.Col(
                dcc.Dropdown(
                    id='napoleon-type-dropdown',
                    options=[
                        {'label': "Tous les 20 Francs Or", 'value': 'all'},
                        # Add other specific 20 Francs Or types here
                        {'label': "Marianne Coq", 'value': 'Marianne Coq'},
                        # ...
                    ],
                    value='all',  # Default value
                    clearable=False,
                    style={'width': '100%', 'color': 'black', 'textAlign': 'center'}
                ),
                width=6,  # Adjust width as needed
            ),
        ]),

    ])

@app.callback(
    Output("cross-platform-analysis-graph", "figure"),
    [Input("url", "pathname"),
     Input("napoleon-type-dropdown", "value")]
)
def update_cross_platform_analysis(pathname, napoleon_type):
    if pathname == "/analyses":

        # 1. Construct the filter condition based on dropdown selection
        if napoleon_type == 'all':
            name_filter = Item.name.like('or - 20 francs fr%')
        else:
            name_filter = Item.name.like(f'or - 20 francs fr {napoleon_type}%')

        # 2. Fetch data using SQLAlchemy ORM with the filter
        results = (
            db.session.query(
                func.DATE_FORMAT(Item.timestamp, '%Y-%m').label('month'),
                Item.source,
                Item.buy_premiums
            )
            .filter(name_filter)
            .group_by('month', Item.source)
            .all()
        )

        df = pd.DataFrame(results, columns=['month', 'source', 'buy_premiums'])

        # 3. Pre-process the 'buy_premiums' column
        df['buy_premiums'] = df['buy_premiums'].apply(lambda x: [float(i) for i in x.split(';')][:5])

        # 4. Calculate the standard deviation for each stack size (1 to 5) without NumPy
        def calculate_std_dev_for_stacks(row):
            premiums_list = row['buy_premiums']
            std_devs = []
            for stack_size in range(1, 6):
                stack_premiums = premiums_list[:stack_size]
                mean = sum(stack_premiums) / len(stack_premiums)
                variance = sum([(x - mean) ** 2 for x in stack_premiums]) / len(stack_premiums)
                std_dev = variance ** 0.5
                std_devs.append(std_dev)
            return pd.Series(std_devs)

        df[[f'stack_{i}' for i in range(1, 6)]] = df.apply(calculate_std_dev_for_stacks, axis=1)

        # 5. Melt the DataFrame to long format for Dash
        df_melted = df.melt(
            id_vars=['month', 'source'],
            value_vars=[f'stack_{i}' for i in range(1, 6)],
            var_name='stack_size',
            value_name='std_dev'
        )
        df_melted['stack_size'] = df_melted['stack_size'].str.replace('stack_', '').astype(int)

        # 6. Create the chart using dash-core-components (dcc.Graph)
        fig = {
            'data': [
                {
                    'x': df_melted[df_melted['source'] == source]['stack_size'],
                    'y': df_melted[df_melted['source'] == source]['std_dev'],
                    'type': 'line',
                    'name': source,
                } for source in df_melted['source'].unique()
            ],
            'layout': {
                'title': "Cross-Platform Premium Deviation Analysis for 20 Francs Napoléon (First 5)",
                'xaxis': {'title': 'Stack Size'},
                'yaxis': {'title': 'Standard Deviation (%)'},
            },
            'frames': [
                {
                    'name': month,
                    'data': [
                        {
                            'x': df_melted[(df_melted['source'] == source) & (df_melted['month'] == month)]['stack_size'],
                            'y': df_melted[(df_melted['source'] == source) & (df_melted['month'] == month)]['std_dev'],
                        } for source in df_melted['source'].unique()
                    ]
                } for month in df_melted['month'].unique()
            ]
        }

        return fig

    else:
        return {}

@app.callback(
        Output("tax-comparison-graph", "figure"),
        [Input("total-amount", "value"),
         Input("annual-yield", "value")]
    )
def update_graph(total_amount, annual_yield):
    years = list(range(0, 23))  # Years 0 to 23
    initial_amount = total_amount
    amount_after_tax_11_5 = []
    amount_after_tax_36_2 = []

    for year in years:
        # Calculate amount after yield
        amount_with_yield = initial_amount * (1 + annual_yield / 100) ** year

        # Calculate amount after tax for 11.5% (remains the same)
        amount_after_tax_11_5.append(amount_with_yield * (1 - 0.115))

        # Calculate amount after tax for 36.2% with reduction and condition
        if amount_with_yield > initial_amount:  # Only apply tax if there's a profit
            if year <= 2:
                tax_36_2 = (amount_with_yield - initial_amount) * 0.362  # Tax on the profit only
            else:
                reduction = 0.05 * (year - 2)
                effective_tax_rate = 0.362 * (1 - reduction)
                tax_36_2 = (amount_with_yield - initial_amount) * effective_tax_rate
            amount_after_tax_36_2.append(amount_with_yield - tax_36_2)
        else:
            amount_after_tax_36_2.append(amount_with_yield)  # No tax if no profit

    fig = {
        'data': [
            {'x': str(years) + 'ans', 'y': amount_after_tax_36_2, 'type': 'line', 'name': "TPV 36.2%", 'hoverinfo': 'y'},
            {'x': str(years) + 'ans', 'y': amount_after_tax_11_5, 'type': 'line', 'name': "TMP 11.5%",'hoverinfo': 'y'},
        ],
        'layout': {
            'title': "Montant récupéré après impôt selon la période de détention",
            'xaxis': {'title': "Année de possession", 'dtick': 1,
                     'tickvals': years,  # Set tickvals to the years list
                     'ticktext': [f'{year} ans' if year > 1 else f'{year} an' for year in years ]},
            'yaxis': {'title': "Montant après impôts (€)", 'tickformat': '.2f','ticksuffix': ' €'},
            'hovermode': 'x unified'
        }
    }

    return fig

if __name__ == '__main__':

    app.run_server(debug=True)