import dash
import datetime
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import sqlite3
from models.model import poids_pieces

# Database file path
db_path = r'C:\Users\Guillaume Hérault\PycharmProjects\trackor\models\pieces_or.db'

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

app.layout = dbc.Container([
    html.H1("Track'Or", className="text-light mb-4"),

    dbc.Row([
        dbc.Col(
            dbc.Card([
                dbc.CardHeader("Budget"),
                dbc.CardBody([
                dcc.Dropdown(
                    id='budget-dropdown',
                    options=[
                        {'label': '500 €', 'value': 500},
                        {'label': '1000 €', 'value': 1000},
                        {'label': '1500 €', 'value': 1500},
                        {'label': '2000 €', 'value': 2000},
                        {'label': '2500 €', 'value': 2500},
                        {'label': '3000 €', 'value': 3000},
                        {'label': '5000 €', 'value': 5000},
                        {'label': '10000 €', 'value': 10000},
                        {'label': '15000 €', 'value': 15000},
                        {'label': '25000 €', 'value': 25000},
                        # Add more options as needed
                    ],
                    value=3000,  # Default value
                    clearable=False,  # Prevent clearing the selection
                    style={'width': '100%','color': 'black'}
                ),
                ]),
            ]),
            width=4,
            lg=2,  # Adjust width for larger screens
        ),
        dbc.Col(
            dbc.Card([
                dbc.CardHeader("Quantité max."),
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
                    style={'width': '100%','color': 'black'}
                ),
                ]),
            ]),
            width=4,
            lg=2,
        ),
        dbc.Col(
            dbc.Card([
                dbc.CardHeader("Métal"),
                dbc.CardBody([
                    dbc.Switch(
                        id='bullion-type-switch',
                        label="Or",  # Label for the switch
                        value=True,
                        style={'width': '100%'} # Default to "Or" (True)
                    ),
                ]),
            ]),
            width=4,
            lg=2,
        ),
    ], className="mb-4"),  # Add margin-bottom to the row

    dbc.Table([  # Create the table structure in the layout
        html.Thead(
            html.Tr([
                html.Th("Nom", style={'text-align': 'center'}),
                html.Th("Source", style={'text-align': 'center'}),
                html.Th("Prime (%)", style={'text-align': 'center'}),
                html.Th("Quantitée min. (U)", style={'text-align': 'center'}),
                html.Th("Total FDPI (€)", style={'text-align': 'center'})
            ])
        ),
        html.Tbody(id='cheapest-offer-table-body')  # Update the tbody in the callback
    ], bordered=True, hover=True, responsive=True, striped=True, dark=True),


    dcc.Interval(
        id='interval-component',
        interval=30*60*1000,  # in milliseconds (30 minutes)
        n_intervals=0
    )
])


@app.callback(
    Output('cheapest-offer-table-body', 'children'),
    [Input('budget-dropdown', 'value'),
     Input('quantity-dropdown', 'value'),
     Input('bullion-type-switch', 'value'),
     Input('interval-component', 'n_intervals')]
)
def update_table(budget, quantity, bullion_type_switch, n):
    # Calculate the timestamp 30 minutes ago

    bullion_type = 'or' if bullion_type_switch else 'ar'

    thirty_minutes_ago = datetime.datetime.now() - datetime.timedelta(minutes=30)
    conn = sqlite3.connect(db_path)

    query_metal_price = f"""
    SELECT *
    FROM metal_price
    WHERE bullion_type = '{bullion_type}'
    AND session_id = (
        SELECT session_id 
        FROM metal_price
        GROUP BY session_id 
        HAVING MAX(timestamp) < '{thirty_minutes_ago.strftime('%Y-%m-%d %H:%M:%S')}' 
        ORDER BY MAX(timestamp) DESC 
        LIMIT 1
    )
    """

    metal_prices_df = pd.read_sql_query(query_metal_price, conn)
    # Get buying gold and silver coin values
    metal_price = metal_prices_df['buy_price'].iloc[0]
    session_id = metal_prices_df['session_id'].iloc[0]

    # SQL query to fetch the latest complete session and its data from both tables
    query_item = f"""
    SELECT * 
    FROM item 
    WHERE bullion_type = '{bullion_type}' AND session_id = '{session_id}'
    """
    # WHERE (minimum <= {quantity} OR quantity <= {quantity})

    # Load data into Pandas DataFrames
    items_df = pd.read_sql_query(query_item, conn)

    conn.close()


    # Use .loc to modify the DataFrame
    items_df.loc[:, ['buy_premiums', 'premium_index']] = items_df['buy_premiums'].apply(
        lambda x: pd.Series({
            'buy_premiums': min([float(i) for i in x.split(';')[:int(quantity)]]),
            'premium_index': [float(i) for i in x.split(';')[:int(quantity)]].index(
                min([float(i) for i in x.split(';')[:int(quantity)]])
            )
        })
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


    items_df['price'] = items_df.apply(
        lambda row: get_price(row['price_ranges'], quantity), axis=1
    )

    # Cheapest offer analysis and recommendations
    cheapest_offers = []

    for i, row in items_df.iterrows():

        try :
            # Get the premium for the specified quantity
            lowest_premium = row['buy_premiums']  # Adjust index for 0-based list
            # Calculate total cost
            # Calculate total cost (using bullion_type)
            spot_cost = poids_pieces[row['name']] * metal_price
            total_cost = (spot_cost  + (lowest_premium / 100.0)*spot_cost) * float(quantity) * float(row['quantity'])

            # Check if the offer meets the budget
            if total_cost <= budget:
                cheapest_offers.append({
                    'name': row['name'],
                    'source': row['source'],
                    'premium': lowest_premium,
                    'quantity': row['premium_index'] + 1,
                    'total_cost': total_cost
                })
        except IndexError as e :
            print(e)  # Skip if the quantity index is out of range

    # Sort offers by premium (lowest first)
    cheapest_offers.sort(key=lambda x: x['premium'])

    # table_rows = [
    #     html.Tr([
    #         html.Th("Nom"),
    #         html.Th("Source"),
    #         html.Th("Prime (%)"),
    #         html.Th("Quantitée min. (U)"),
    #         html.Th("Total FDPI (€)")
    #     ])
    # ]
    table_rows = []
    for offer in cheapest_offers:
        table_rows.append(
            html.Tr([
                html.Td(offer['name'][4:]),
                html.Td(offer['source']),
                html.Td(offer['premium'],style={'text-align': 'center'}),
                html.Td(offer['quantity'],style={'text-align': 'center'}),
                html.Td(f"{offer['total_cost']:.2f} €",style={'text-align': 'center'})
            ])
        )

    return table_rows

if __name__ == '__main__':
    app.run_server(debug=True)