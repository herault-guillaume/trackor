import dash
import datetime
from dash import dcc, html, Input, Output, State
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import pandas as pd
import sqlite3
from models.model import poids_pieces

# Database file path
db_path = r'C:\Users\Guillaume Hérault\PycharmProjects\trackor\models\pieces_or.db'

def get_country_flag_image(country_code):
    """
    Generates an HTML img tag for a country flag image from a 2-letter country code.
    Uses images from the provided URL with the format "https://hatscripts.github.io/circle-flags/flags/{code}.svg".
    """
    if len(country_code) == 2:
        return html.Img(
            src=f"https://hatscripts.github.io/circle-flags/flags/{country_code.lower()}.svg",
            alt=country_code,
            style={'width': '20px', 'margin-right': '5px'}
        )
    else:
        return ""

or_options_quick_filter = [
                {'label': html.Span([get_country_flag_image('fr'), "20 francs Napoléon d'Or"]), 'value': 'or - 20 francs fr *'},
                {'label': html.Span([get_country_flag_image('fr'), "5 francs"]), 'value': 'or - 5 francs fr *'},
                {'label': html.Span([get_country_flag_image('fr'), "10 francs"]), 'value': 'or - 10 francs fr *'},
                {'label': html.Span([get_country_flag_image('fr'), "40 francs"]), 'value': 'or - 40 francs fr *'},
                {'label': html.Span([get_country_flag_image('fr'), "50 francs"]), 'value': 'or - 50 francs fr *'},
                {'label': html.Span([get_country_flag_image('fr'), "100 francs"]), 'value': 'or - 100 francs fr *'},
                {'label': html.Span([get_country_flag_image('ch'), "20 francs"]), 'value': 'or - 20 francs sui *'},
                {'label': html.Span([get_country_flag_image('gb'), "1 souverain"]), 'value': 'or - 1 souverain *'},
                {'label': html.Span([get_country_flag_image('gb'), "1/2 souverain"]), 'value': 'or - 1/2 souverain *'},
                {'label': html.Span([get_country_flag_image('us'), "2.5 dollars"]), 'value': 'or - 2.5 dollars *'},
                {'label': html.Span([get_country_flag_image('us'), "5 dollars"]), 'value': 'or - 5 dollars *'},
                {'label': html.Span([get_country_flag_image('us'), "10 dollars"]), 'value': 'or - 10 dollars *'},
                {'label': html.Span([get_country_flag_image('us'), "20 dollars"]), 'value': 'or - 20 dollars *'},
                {'label': html.Span([get_country_flag_image('mx'), "50 pesos"]), 'value': 'or - 50 pesos *'},
                {'label': html.Span([get_country_flag_image('it'), "20 lire"]), 'value': 'or - 20 lire *'},
                {'label': html.Span([get_country_flag_image('de'), "20 mark"]), 'value': 'or - 20 mark *'},
                {'label': "1 Oz", 'value': 'or - 1 oz*'},
                {'label': "1/2 Oz", 'value': 'or - 1/2 oz*'},
                {'label': "1/4 Oz", 'value': 'or - 1/4 oz*'},
                {'label': "1/10 Oz", 'value': 'or - 1/10 oz*'},
                {'label': "1/20 Oz", 'value': 'or - 1/20 oz*'},
                        ]
ar_options_quick_filter = [
            {'label': html.Span([get_country_flag_image('fr'), "50 Cts francs"]), 'value': 'ar - 50 centimes francs fr *'},
            {'label': html.Span([get_country_flag_image('fr'), "1 franc"]), 'value': 'ar - 1 franc fr *'},
            {'label': html.Span([get_country_flag_image('fr'), "2 francs"]), 'value': 'ar - 2 francs fr *'},
            {'label': html.Span([get_country_flag_image('fr'), "5 francs"]), 'value': 'ar - 5 francs fr *'},
            {'label': html.Span([get_country_flag_image('fr'), "10 francs"]), 'value': 'ar - 10 francs fr *'},
            {'label': html.Span([get_country_flag_image('fr'), "20 francs"]), 'value': 'ar - 20 francs fr *'},
            {'label': html.Span([get_country_flag_image('fr'), "50 francs Hercule"]), 'value': 'ar - 50 francs fr *'},
            {'label': html.Span([get_country_flag_image('fr'), "100 francs Hercule"]), 'value': 'ar - 100 francs fr *'},
            {'label': "1 Oz", 'value': 'ar - 1 oz *'},
]



app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY,'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css'],assets_folder='assets')

app.layout = dbc.Container([
    html.H1("Track'Or", className="text-light mb-4"),

    dbc.Row([
        dbc.Col(
            dbc.Card([
                dbc.CardHeader([html.I(className="fa-solid fa-bullseye", style={'font-size': '16px'}),"  Mon budget (€)"],style = {'text-align': 'center'}),
                dbc.CardBody([
                    dcc.RangeSlider(
                        id='budget-slider',
                        min=0,
                        max=15000,
                        step=250,
                        value=[500, 3000],  # Default range
                        marks={
                            0: '0 €',
                            15000: '15k €',
                        },
                        allowCross=False,
                        persistence=True,
                        tooltip={"placement": "bottom", "always_visible": True,"style": {"color": "gold", "fontSize": "14px"}},  # Show tooltip always
                    )
                ]),
            ]),
            xs=12, sm=12, md=6, lg=6, xl=6,xxl=6, className="mb-4"  # Adjust width for larger screens
        ),
        dbc.Col(
            dbc.Card([
                dbc.CardHeader([html.I(className="fa-sharp fa-solid fa-coins", style={'font-size': '16px'}),"  Quantité max."],style = {'text-align': 'center'}),
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
                        {'label': '50', 'value': 50},
                        {'label': '100', 'value': 100},
                        {'label': '150', 'value': 150},

                        # Add more options as needed
                    ],
                    value=3,  # Default value
                    clearable=False,  # Prevent clearing the selection
                    persistence=True,
                    style={'width': '100%','color': 'black','text-align': 'center'}
                ),
                ]),
            ]),
            xs=6, sm=6, md=3, lg=3, xl=3,xxl=3,className="mb-4"
        ),

        dbc.Col(
            dbc.Card([
                dbc.CardHeader([html.I(className="fa-solid fa-cube", style={'font-size': '16px'}),"  Bullion"], style={'text-align': 'center'}),
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
                ,html.Div(id='metal-price-output')])
            ],),  # Set a fixed width for the Card
            xs=6, sm=6, md=3, lg=2, xl=2,xxl=2, className="mb-4"
        ),
        dbc.Col(
            dbc.Card([
                dbc.CardHeader([html.I(className="fa-solid fa-magnifying-glass", style={'font-size': '16px'}), "  Effigie/Année indifférenciées"], style={'text-align': 'center'}),  # New card for name selection
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
            ]),
            xs=12, sm=12, md=8, lg=6, xl=4, xxl=4, className="mb-4"
        ),
    ], className="mb-4 equal-height-cards"),  # Add margin-bottom to the row

    html.Div(id='last-update-info', className="text-center mb-2"),  # Add a div to display the last update info

    dbc.Spinner(id="loading-output", children=[
        dbc.Table([  # Create the table structure in the layout
            html.Thead(
                html.Tr([
                    html.Th([html.I(className="fa-brands fa-sourcetree", style={'font-size': '16px'}), "  Source"],style={'text-align': 'center'}),
                    html.Th([html.I(className="", style={'font-size': '16px'}),"  Nom"], style={'text-align': 'center'}),
                    html.Th(
                        [
                            html.I(className="fa-solid fa-arrow-trend-down", style={'font-size': '16px'}),
                            "  Prime (%)",  # The header text
                            dbc.Tooltip("La prime inclue les frais de port et le prix dégressif.", target="premium-header")  # The tooltip
                        ],
                        id="premium-header",
                        style={'text-align': 'center'}
                    ),
                    html.Th(
                        [
                            html.I(className="fa-solid fa-chart-line", style={'font-size': '16px'}),
                            "  Quantité min. (U)",
                            dbc.Tooltip("Quantité minimum pour obtenir le prix affiché.", target="quantite-header")
                        ],
                        id="quantite-header",
                        style={'text-align': 'center'}
                    ),
                    html.Th([html.I(className="fa-solid fa-tag", style={'font-size': '16px'}),"  Total FDPI (€)"], style={'text-align': 'center'})
                    ])
                ), # Apply spinner only to the tbody
                    html.Tbody(id='cheapest-offer-table-body')
                ,
                ], bordered=True, hover=True, responsive=True, striped=True, dark=True),
    ],  color="gold", type="border", spinner_style={"position": "absolute", "top": "3em"}),

    dcc.Interval(
        id='interval-component',
        interval=30*60*1000,  # in milliseconds (30 minutes)
        n_intervals=0
    )
])


@app.callback(
    Output('cheapest-offer-table-body', 'children'),
    Output('last-update-info', 'children'),
    [Input('budget-slider', 'value'),
     Input('quantity-dropdown', 'value'),
     Input('bullion-type-switch', 'value'),
     Input('piece-dropdown', 'value'),
     Input('interval-component', 'n_intervals')],
    [State('cheapest-offer-table-body', 'children')]
)

def update_table(budget_range, quantity, bullion_type_switch,selected_coins, current_table ,n):

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

    bullion_type = 'or' if bullion_type_switch else 'ar'

    thirty_minutes_ago = datetime.datetime.now() - datetime.timedelta(minutes=30)
    conn = sqlite3.connect(db_path)

    query_metal_price = """
    SELECT *
    FROM metal_price
    WHERE bullion_type = ?
    AND session_id = (
        SELECT session_id 
        FROM metal_price
        GROUP BY session_id 
        HAVING MAX(timestamp) < ?
        ORDER BY MAX(timestamp) DESC 
        LIMIT 1
    )
    """

    # Execute the query with parameters
    metal_prices_df = pd.read_sql_query(query_metal_price, conn,params=(bullion_type, thirty_minutes_ago.strftime('%Y-%m-%d %H:%M:%S')))

    # Get buying gold and silver coin values
    metal_price = metal_prices_df['buy_price'].iloc[0]
    session_id = metal_prices_df['session_id'].iloc[0]
    latest_timestamp = metal_prices_df['timestamp'].iloc[0]
    formatted_timestamp = datetime.datetime.strptime(latest_timestamp, '%Y-%m-%d %H:%M:%S.%f').strftime('%d/%m/%Y à %Hh%M.')

    cheapest_offers = []
    seen_offers = set()
    table_rows = []

    # SQL query to fetch the latest complete session and its data from both tables
    query_item = """
    SELECT * 
    FROM item 
    WHERE bullion_type = ? AND session_id = ?
    """
    # WHERE (minimum <= {quantity} OR quantity <= {quantity})

    # Load data into Pandas DataFrames
    items_df = pd.read_sql_query(query_item, conn, params=(bullion_type, session_id))

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

        # Use .loc to modify the DataFrame (without text parsing)

        df_copy.loc[:, ['buy_premiums', 'premium_index']] = df_copy['buy_premiums'].apply(
            lambda x: pd.Series({
                'buy_premiums': min(x[:q_max]),
                'premium_index': x.index(min(x[:q_max]))
            })
        )

        df_copy['price'] = df_copy.apply(lambda row: get_price(row['price_ranges'], row['premium_index']+1), axis=1)

        # Cheapest offer analysis and recommendations
        results = df_copy.sort_values(by='buy_premiums').head(40)

        for i, row in results.iterrows():
            try :
                # Calculate total cost (using bullion_type)
                spot_cost = poids_pieces[row['name']] * metal_price
                total_cost = (spot_cost  + (row['buy_premiums']  / 100.0)*spot_cost) * (row['premium_index']+1) * float(row['quantity'])

                # Check if the offer meets the budget
                if budget_min <= total_cost <= budget_max and (row['name'], row['source']) not in seen_offers:
                    cheapest_offers.append({
                        'name': row['name'],
                        'source': row['source'],
                        'premium': row['buy_premiums'] ,
                        'quantity': int(row['premium_index'] + 1),
                        'total_cost': total_cost
                    })
                    seen_offers.add((row['name'], row['source']))
            except IndexError as e :
                print(e)  # Skip if the quantity index is out of range

    # Sort offers by premium (lowest first)
    cheapest_offers.sort(key=lambda x: x['premium'])

    conn.close()

    for offer in cheapest_offers:
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
                html.Td(f"{offer['total_cost']:.2f} €",style={'text-align': 'center'})
            ])
        )

    if table_rows == []:
        warning_icon = html.I(className="fas fa-triangle-exclamation", style={'color': 'orange', 'font-size': '16px'})  # Adjust color and size as needed
        table_rows.append(
            html.Tr([
                html.Td(warning_icon, style={'text-align': 'center'}),
                html.Td("Veuillez augmenter votre budget pour voir les offres."),
                html.Td(warning_icon, style={'text-align': 'center'}),
                html.Td(warning_icon, style={'text-align': 'center'}),
                html.Td(warning_icon, style={'text-align': 'center'})
            ])
        )

    return table_rows, html.P(f"Dernière mise à jour le {formatted_timestamp}", style={'font-size': '0.8em'})


@app.callback(
    Output('piece-dropdown', 'options'),  # Output to update the dropdown options
    [Input('bullion-type-switch', 'value')]
)
def update_piece_dropdown(bullion_type_switch):
    if bullion_type_switch :
        return or_options_quick_filter
    else :
        return ar_options_quick_filter

@app.callback(
    Output('quantity-dropdown', 'value'),  # Output to update the quantity dropdown
    [Input('bullion-type-switch', 'value'),
     State('quantity-dropdown', 'value')]
)
def update_quantity_dropdown(bullion_type_switch,quantity):
    if bullion_type_switch:  # If the switch is on (gold)
        return 3  # Set quantity to 3
    else:
        return quantity
    # No need to return anything if the switch is off (silver)
    # The quantity dropdown will keep its current value

@app.callback(
    Output('metal-price-output', 'children'),  # Output to update the price display
    [Input('bullion-type-switch', 'value'),
     Input('interval-component', 'n_intervals')]
)
def update_metal_price(bullion_type_switch, n):
    bullion_type = 'or' if bullion_type_switch else 'ar'

    thirty_minutes_ago = datetime.datetime.now() - datetime.timedelta(minutes=30)
    conn = sqlite3.connect(db_path)

    query_metal_price = """
    SELECT *
    FROM metal_price
    WHERE bullion_type = ?
    AND session_id = (
        SELECT session_id 
        FROM metal_price
        GROUP BY session_id 
        HAVING MAX(timestamp) < ?
        ORDER BY MAX(timestamp) DESC 
        LIMIT 1
    )
    """

    # Execute the query with parameters
    metal_prices_df = pd.read_sql_query(query_metal_price, conn,params=(bullion_type, thirty_minutes_ago.strftime('%Y-%m-%d %H:%M:%S')))

    # Get buying gold and silver coin values
    metal_price = metal_prices_df['buy_price'].iloc[0]

    return html.Div(
        [
            html.Hr(style={'margin': '5px 0'}),  # Add a horizontal rule for separation
            html.P(f"{metal_price:.3f} €/g ", style={'font-size': '0.8em', 'margin-bottom': '0','text-align':'center'})
        ]
    )




if __name__ == '__main__':
    app.run_server(debug=True)