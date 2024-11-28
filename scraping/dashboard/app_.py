from dotenv import load_dotenv
load_dotenv()

from scraping.dashboard.pieces import weights
from scraping.dashboard.database import db, MetalPrice, Item, UserChoice

import os
import pandas as pd
import sshtunnel
import pytz
import datetime

import dash
from dash import dcc, html, Input, Output, State, callback_context
import dash_bootstrap_components as dbc

from flask import Flask, request, session

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

def create_and_attach_session_throught_tunnel(db,tunnel):
    conn_str = os.getenv('SQLALCHEMY_DATABASE_URI').format(tunnel.local_bind_port)
    engine = db.create_engine(conn_str, echo=True)  # echo=False to disable logging SQL queries
    Session = db.scoped_session(db.sessionmaker(autocommit=False, autoflush=False, bind=engine))
    return Session()  # Set the db.session

tunnel = create_tunnel()
tunnel.start()

# Configuration using environment variables
server.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI').format(tunnel.local_bind_port)

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

# Create the database tables

def serve_layout():
    return dbc.Container([
        html.Div([

    dcc.Loading(id="loading-1",type="default",children=html.Div(id="tawk-to-widget")),
    # Rest of your Dash app layout
    ]),

    dbc.Row([html.Img(src='/assets/logo-bullion-sniper.webp', style={'height': '150px', 'width': 'auto'}),], className="mb-4 mt-4",justify="center"),

    dbc.Row([
        dbc.Col(
            dbc.Card([
                dbc.CardHeader([html.I(className="fa-solid fa-bullseye fa-bounce", style={'font-size': '16px'}),"  Mon budget (€)",dbc.Tooltip("Le budget que je souhaite me fixer.", target="cardheader-budget")],style = {'text-align': 'center'}),
                dbc.CardBody([
                    dcc.RangeSlider(
                        id='budget-slider',
                        min=0,
                        max=12500,
                        step=100,
                        value=[0, 1000],  # Default range
                        marks={
                            0: '0 €',
                            12500: '12k5 €',
                        },
                        allowCross=False,
                        persistence=True,
                        tooltip={"placement": "bottom", "always_visible": True,"style": {"color": "gold", "fontSize": "14px"}},  # Show tooltip always
                    )
                ],id="cardheader-budget"),
            ]),
            xs=12, sm=12, md=6, lg=6, xl=6,xxl=7, className="mb-4"  # Adjust width for larger screens
        ),
        dbc.Col(
            dbc.Card([
                dbc.CardHeader([html.I(className="fa-sharp fa-solid fa-coins fa-bounce", style={'font-size': '16px'}),"  Quantité max.",dbc.Tooltip("Le nombre maximum de pièces que je souhaite acheter.", target="cardheader-quantity")],style = {'text-align': 'center'}),
                dbc.CardBody([
                dcc.Dropdown(
                    id='quantity-dropdown',
                    options=[
                        {'label': '1', 'value': 1},
                        {'label': '2', 'value': 2},
                        {'label': '3', 'value': 3},
                        {'label': '4', 'value': 4},
                        {'label': '5', 'value': 5},
                        {'label': '6', 'value': 6},
                        {'label': '7', 'value': 7},
                        {'label': '8', 'value': 8},
                        {'label': '9', 'value': 9},
                        {'label': '10', 'value': 10},
                        {'label': '11', 'value': 11},
                        {'label': '12', 'value': 12},
                        {'label': '13', 'value': 13},
                        {'label': '14', 'value': 14},
                        {'label': '15', 'value': 15},
                        {'label': '25', 'value': 25},
                        {'label': '50', 'value': 50},
                        {'label': '75', 'value': 75},
                        {'label': '100', 'value': 100},
                        {'label': '125', 'value': 125},
                        {'label': '150', 'value': 150},

                        # Add more options as needed
                    ],
                    value=3,  # Default value
                    clearable=False,  # Prevent clearing the selection
                    persistence=True,
                    style={'width': '100%','color': 'black','text-align': 'center'}
                ),
                ],id="cardheader-quantity"),
            ]),
            xs=6, sm=6, md=3, lg=3, xl=3,xxl=3,className="mb-4"
        ),

        dbc.Col(
            dbc.Card([
                dbc.CardHeader([html.I(className="fa-solid fa-cube", style={'font-size': '16px'}),"  Bullion", dbc.Tooltip("Source cours du métal : BullionVault.", target="cardheader-bullion")], style={'text-align': 'center'}),
                dbc.CardBody([
                    html.Div(
                        [
                            html.Span("Argent", className="me-2"),
                            dbc.Switch(
                                id='bullion-type-switch',
                                label="",
                                value=True,
                                className="gold-silver-switch larger-switch",
                                persistence = True,
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
                dbc.CardHeader([html.I(className="fa-solid fa-magnifying-glass", style={'font-size': '16px'}), "  Effigie/Année", dbc.Tooltip("Je récupère les offres pour un ou plusieurs types de pièce.", target="cardheader-years")], style={'text-align': 'center'}),  # New card for name selection
                dbc.CardBody([
                    dcc.Dropdown(
                        id='piece-dropdown',
                        options=[],
                        multi=True,
                        value=None,  # No default selection
                        placeholder="Sélectionnez une pièce",  # Placeholder text
                        clearable=True,  # Allow clearing the selection
                        style={'width': '100%', 'color': 'black', 'text-align': 'center'}
                    ),
                ]),
            ],id="cardheader-years"),
            xs=12, sm=12, md=8, lg=6, xl=4, xxl=4, className="mb-4"
        ),
    ], className="mb-4 equal-height-cards"),  # Add margin-bottom to the row

    html.Div(id='last-update-info', className="text-center mb-2"),  # Add a div to display the last update info

    dbc.Spinner(id="loading-output", children=[
        dbc.Table([  # Create the table structure in the layout
            html.Thead(
                html.Tr([
                    html.Th([html.I(className="fa-solid fa-shop", style={'font-size': '16px'}), "  Site marchand",
                             html.Span(id='source-arrow', className="fa fa-sort ms-2")],style={'text-align': 'center'}, id='source-header',n_clicks=0),
                    html.Th([html.I(className="", style={'font-size': '16px'}),"  Nom",
                             html.Span(id='name-arrow', className="fa fa-sort ms-2")], style={'text-align': 'center'}, id='name-header', n_clicks=0),
                    html.Th(
                        [
                            html.I(className="fa-solid fa-arrow-trend-down", style={'font-size': '16px'}),
                            "  Prime (%)",
                            html.Span(id='premium-arrow', className="fa fa-sort ms-2"),
                            dbc.Tooltip("La prime inclue les frais de port et le prix dégressif. Valable uniquement à l'horaire affichée ci-dessus.",target="premium-header")  # The tooltip
                        ],
                        id="premium-header",
                        style={'text-align': 'center'},n_clicks=0),
                    html.Th(
                        [
                            html.I(className="fa-solid fa-chart-line", style={'font-size': '16px'}),
                            "  Quantité min. (U)",
                            html.Span(id='quantity-arrow', className="fa fa-sort ms-2"),
                            dbc.Tooltip("Quantité minimum pour obtenir la prime affichée.", target="quantity-header")
                        ],
                        id="quantity-header",
                        style={'text-align': 'center'}, n_clicks=0),
                    html.Th([html.I(className="fa-solid fa-tag", style={'font-size': '16px'}),"  Total FDPI",
                             html.Span(id='total_cost-arrow', className="fa fa-sort ms-2"),], style={'text-align': 'center'}, id='total_cost-header', n_clicks=0),

                    html.Th([html.I(className="fa-solid fa-truck fa-tag", style={'font-size': '16px'}), "  FDP",
                             html.Span(id='delivery-arrow', className="fa fa-sort ms-2"), ],
                            style={'text-align': 'center'}, id='delivery-header', n_clicks=0),

                ])
            , id='table-header'), # Apply spinner only to the tbody
                    html.Tbody(id='cheapest-offer-table-body'),
        ], bordered=True, hover=True, responsive=True, striped=True, dark=True),
    ],  color="gold", type="border", spinner_style={"position": "absolute", "top": "3em"}),

    dcc.Interval(
        id='interval-component',
        interval=30*60*1000,  # in milliseconds (30 minutes)
        n_intervals=0
    ),

    dbc.Row(
        [
            dbc.Col(
                [
                    dbc.Card(
                    [
                        dbc.CardHeader(
                            [
                                html.I(className="fa-solid fa-circle-exclamation fa-beat-fade", style={'font-size': '22px'}),
                                "  Bullion-sniper.fr ne donne pas de conseils en investissement.",

                            ],
                        ),
                        dbc.CardBody([
                        "Nous attachons un soin particulier à créer et entretenir le présent site et à veiller à l’exactitude et à l’actualité de son contenu.",html.Br(),html.Br(), "Néanmoins, les éléments présentés dans ce site sont susceptibles de modifications fréquentes sans préavis. Bullion-sniper.fr ne garantit pas l’exactitude et l’actualité du contenu du site. Les éléments présentés Bullion-sniper.fr sont mis à disposition des utilisateurs sans aucune garantie d’aucune sorte et ne peuvent donner lieu à un quelconque droit à dédommagement.",
                    ])], style={'text-align': 'center'}
                    )
                ],
                width=12)
        ], className="mb-4 equal-height-cards"),

    html.Div([
        "2025 - Bullion-sniper.fr x ",
        html.A("Dash ",href="https://dash.plotly.com/"),
        html.I(className="fa-solid fa-heart fa-beat", style={'font-size': '16px', 'color' : 'red'}),], className="text-center mb-2"),  # Add a div to display the last update info

    ])


@app.callback(
    Output('cheapest-offer-table-body', 'children'),
    Output('last-update-info', 'children'),
    Output('source-arrow', 'className'),  # Output for the arrow icon's className
    Output('name-arrow', 'className'),  # Output for the arrow icon's className
    Output('premium-arrow', 'className'),  # Output for the arrow icon's className
    Output('quantity-arrow', 'className'),  # Output for the arrow icon's className
    Output('total_cost-arrow', 'className'),
    Output('delivery-arrow', 'className'),
    [Input('budget-slider', 'value'),
     Input('quantity-dropdown', 'value'),
     Input('bullion-type-switch', 'value'),
     Input('piece-dropdown', 'value'),
     Input('interval-component', 'n_intervals'),
     Input('source-header', 'n_clicks'),  # Input for each header's n_clicks
     Input('name-header', 'n_clicks'),
     Input('premium-header', 'n_clicks'),
     Input('quantity-header', 'n_clicks'),
     Input('total_cost-header', 'n_clicks'),
     Input('delivery-header', 'n_clicks')],
    [State('cheapest-offer-table-body', 'children')]
)
def update_and_sort_table(budget_range, quantity, bullion_type_switch, selected_coins, n,
                          source_clicks, name_clicks, premium_clicks, quantity_clicks, total_cost_clicks,delivery_clicks,
                          current_table):
    ctx = callback_context
    triggered_id, triggered_prop = ctx.triggered[0]['prop_id'].split('.')

    # Initialize arrow class names
    arrow_classNames = {
        'source-arrow': "fa fa-sort ms-2",
        'name-arrow': "fa fa-sort ms-2",
        'premium-arrow': "fa fa-sort ms-2",
        'quantity-arrow': "fa fa-sort ms-2",
        'total_cost-arrow': "fa fa-sort ms-2",
        'delivery-arrow': "fa fa-sort ms-2"
    }

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
        elif triggered_id == 'quantity-header':
            column_index = 3
            sort_key = 'quantity'
        elif triggered_id == 'total_cost-header':
            column_index = 4
            sort_key = 'total_cost'
        elif triggered_id == 'delivery-header':
            column_index = 5
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
                arrow_classNames['premium-arrow'], arrow_classNames['quantity-arrow'],
                arrow_classNames['total_cost-arrow'],arrow_classNames['delivery-arrow'])
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


        results = MetalPrice.get_previous_price(db.session,bullion_type)
        metal_prices_df = pd.DataFrame(results)

        metal_price = metal_prices_df['buy_price'].iloc[0]
        session_id = metal_prices_df['session_id'].iloc[0]
        latest_timestamp = metal_prices_df['timestamp'].iloc[0]
        formatted_timestamp = latest_timestamp.strftime('%d/%m/%Y à %Hh%M.')

        cheapest_offers = []
        seen_offers = set()
        table_rows = []

        # SQL query to fetch the latest complete session and its data from both tables
        results = Item.get_items_by_bullion_type_and_quantity(db.session,bullion_type,session_id,quantity)
        items_df = pd.DataFrame(results).copy()

        if selected_coins:
            filtered_df = pd.DataFrame()  # Create an empty DataFrame to store filtered rows
            for coin in selected_coins:
                filtered_df = pd.concat([filtered_df, items_df[items_df['name'].str.contains(coin, regex=True)]])
            items_df = filtered_df  # Update items_df with the filtered DataFrame

        # Pre-process the 'buy_premiums' column before the loops
        items_df['buy_premiums'] = items_df['buy_premiums'].apply(lambda x: [float(i) for i in x.split(';')])

        budget_min, budget_max = budget_range

        for q_max in reversed(range(1,quantity+1)):
            df_copy = items_df.copy()

            df_copy.loc[:, ['buy_premiums', 'premium_index']] = df_copy['buy_premiums'].apply(
                lambda x: pd.Series({
                    'buy_premiums': min(x[:q_max]),
                    'premium_index': x.index(min(x[:q_max]))
                })
            )

            df_copy['price'] = df_copy.apply(lambda row: get_price(row['price_ranges'], row['premium_index']+1), axis=1)

            # Cheapest offer analysis and recommendations
            results = df_copy.sort_values(by='buy_premiums')

            for i, row in results.iterrows():
                try :
                    # Calculate total cost (using bullion_type)
                    spot_cost = weights[row['name']] * metal_price
                    total_cost = (spot_cost  + (row['buy_premiums']  / 100.0)*spot_cost) * (row['premium_index']+1) * float(row['quantity']) if row['minimum'] == row['quantity'] == 1 else (spot_cost  + (row['buy_premiums']  / 100.0)*spot_cost) * (row['premium_index']+1) * quantity

                    # Check if the offer meets the budget
                    if (row['name'], row['source']) not in seen_offers and budget_min <= total_cost <= budget_max and quantity >= row['minimum'] and quantity >= row['quantity'] :
                        cheapest_offers.append({
                            'name': row['name'].upper(),
                            'source': row['source'],
                            'premium': row['buy_premiums'] ,
                            'quantity': int(row['premium_index'] + 1) * row['quantity'] if row['minimum'] == row['quantity'] == 1 else quantity,
                            'delivery_fees': get_price(row['delivery_fees'],quantity),
                            'total_cost': total_cost
                        })
                        seen_offers.add((row['name'], row['source']))
                except IndexError as e :
                    print(e)  # Skip if the quantity index is out of range

    # Sort offers by premium (lowest first)
    cheapest_offers.sort(key=lambda x: x['premium'])

    for offer in cheapest_offers[:30]:
        table_rows.append(
            html.Tr([
                html.Td(
                    html.A(
                        html.I(className="fas fa-external-link-alt", style={'color': 'gold'}),  # External link icon
                        href=offer['source'],  # URL of the source
                        target="_blank",  # Open link in a new tab
                        style={'text-decoration': 'none', 'text_align':'center'}  # Remove underline from the link
                    ),
                    style={'text-align': 'center'}
                ),
                html.Td(offer['name'][4:]),
                html.Td(offer['premium'],style={'text-align': 'center'}),
                html.Td(offer['quantity'],style={'text-align': 'center'}),
                html.Td(f"{offer['total_cost']:.2f} €",style={'text-align': 'center'}),
                html.Td(f"{offer['delivery_fees']:.2f} €",style={'text-align': 'center'})
            ])
        )

    if table_rows == []:
        DEBUG_icon = html.I(className="fas fa-triangle-exclamation", style={'color': 'orange', 'font-size': '16px'})  # Adjust color and size as needed
        table_rows.append(
            html.Tr([
                html.Td(DEBUG_icon, style={'text-align': 'center'}),
                html.Td("Veuillez augmenter votre budget pour voir les offres."),
                html.Td(DEBUG_icon, style={'text-align': 'center'}),
                html.Td(DEBUG_icon, style={'text-align': 'center'}),
                html.Td(DEBUG_icon, style={'text-align': 'center'})
            ])
        )

    return (table_rows,
            html.P(f"Dernière mise à jour le {formatted_timestamp}", style={'font-size': '0.8em'}),
            arrow_classNames['source-arrow'],
            arrow_classNames['name-arrow'],
            arrow_classNames['premium-arrow'],
            arrow_classNames['quantity-arrow'],
            arrow_classNames['total_cost-arrow'],
            arrow_classNames['delivery-arrow'],
            )

@app.callback(
    Output('piece-dropdown', 'options'),
    [Input('bullion-type-switch', 'value')]
)
def update_piece_dropdown(bullion_type_switch):
    if bullion_type_switch :
        return or_options_quick_filter
    else :
        return ar_options_quick_filter

@app.callback(
    Output('quantity-dropdown', 'value'),
    [Input('bullion-type-switch', 'value'),
     State('quantity-dropdown', 'value')]
)
def update_quantity_dropdown(bullion_type_switch,quantity):
    if bullion_type_switch:
        return 3
    else:
        return quantity

@app.callback(
    Output('metal-price-output', 'children'),
    [Input('bullion-type-switch', 'value'),
     Input('interval-component', 'n_intervals')]
)
def update_metal_price(bullion_type_switch, n):
    bullion_type = 'or' if bullion_type_switch else 'ar'

    results = MetalPrice.get_previous_price(db.session,bullion_type)
    metal_prices_df = pd.DataFrame(results)

    print(metal_prices_df)
    # Get buying gold and silver coin values
    metal_price = metal_prices_df['buy_price'].iloc[0]

    return html.Div(
        [
            html.Hr(style={'margin': '5px 0'}),  # Add a horizontal rule for separation
            html.P(f"{metal_price:.3f} €/g ", style={'font-size': '0.8em', 'margin-bottom': '0','text-align':'center'})
        ]
    )

    return current_table

app.clientside_callback(
        """
        function(n_clicks) {
            setTimeout(function() {
                var s1=document.createElement("script");
                s1.async=true;
                s1.src='https://embed.tawk.to/673851ed4304e3196ae37e76/1icq0025a';
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

def get_price(ranges, quantity):
    """
    Calculates the price based on the quantity and given ranges.

    Args:
    ranges: A string of ranges in the format '1-9;10-48;49-98;99-9999999999.9'.
    quantity: The quantity of the item.

    Returns:
    The price as a float.
    """
    ranges = ranges.split(';')

    for r in ranges:
        lower, upper, price = map(float, r.split('-'))
        if lower <= quantity < upper:
            return price  # Return the price directly
        return None  # Or handle the case where quantity is outside all ranges

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




with app.server.app_context():
    db.init_app(server)
    db.create_all()

    # Simplified layout and callback
    app.layout = serve_layout()

    results = MetalPrice.get_previous_price(db.session, 'or')
    metal_prices_df = pd.DataFrame(results)

    metal_price = metal_prices_df['buy_price'].iloc[0]
    session_id = metal_prices_df['session_id'].iloc[0]
    # SQL query to fetch the latest complete session and its data from both tables
    results = Item.get_items_by_bullion_type_and_quantity(db.session, 'or', session_id, 150)
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

    results = Item.get_items_by_bullion_type_and_quantity(db.session, 'ar', session_id, 150)
    items_df = pd.DataFrame(results).copy()
    items_df.drop_duplicates(subset=['name'], inplace=True)
    items_df.sort_values(by='name', inplace=True)
    ar_options_quick_filter = [
                                  {'label': html.Span([get_country_flag_image('fr'), "Toutes les 50 Cts francs"]),
                                   'value': 'ar - 50 centimes francs fr *'},
                                  {'label': html.Span([get_country_flag_image('fr'), "Toutes les 1 franc"]),
                                   'value': 'ar - 1 franc fr *'},
                                  {'label': html.Span([get_country_flag_image('fr'), "Toutes les 2 francs"]),
                                   'value': 'ar - 2 francs fr *'},
                                  {'label': html.Span([get_country_flag_image('fr'), "Toutes les 5 francs"]),
                                   'value': 'ar - 5 francs fr *'},
                                  {'label': html.Span([get_country_flag_image('fr'), "Toutes les 10 francs"]),
                                   'value': 'ar - 10 francs fr *'},
                                  {'label': html.Span([get_country_flag_image('fr'), "Toutes les 20 francs"]),
                                   'value': 'ar - 20 francs fr *'},
                                  {'label': html.Span([get_country_flag_image('fr'), "Toutes les 50 francs Hercule"]),
                                   'value': 'ar - 50 francs fr *'},
                                  {'label': html.Span([get_country_flag_image('fr'), "Toutes les 100 francs Hercule"]),
                                   'value': 'ar - 100 francs fr *'},
                                  {'label': "Toutes les 1 Oz", 'value': 'ar - 1 oz *'},
                              ] + [{'label': html.Span(row['name'][4:].upper()), 'value': row['name']} for _, row in
                                   items_df.iterrows()]

if __name__ == '__main__':

    app.run_server(debug=True)