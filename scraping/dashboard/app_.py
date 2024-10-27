import dash
import datetime
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import sqlite3
from models.model import poids_pieces

# Database file path
db_path = r'C:\Users\Guillaume Hérault\PycharmProjects\trackor\models\pieces_or.db'

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    html.H1("Cheapest Offer Analysis and Cross-Platform Selling"),

    dbc.Row([
        dbc.Col([
            dcc.Input(
                id='budget-input',
                type='number',
                placeholder='Budget (€)',
                value=1500  # Default budget
            ),
        ], width=2),
        dbc.Col([
            dcc.Input(
                id='quantity-input',
                type='number',
                placeholder='Quantity',
                value=5  # Default quantity
            ),
        ], width=2),
        dbc.Col([
            dcc.RadioItems(
                id='bullion-type-radio',
                options=[
                    {'label': 'Gold', 'value': 'or'},
                    {'label': 'Silver', 'value': 'ar'}
                ],
                value='or'  # Default value (gold)
            ),
        ], width=2),

    ]),

    html.Div(id='cheapest-offer-table'),  # Display cheapest offers

    dcc.Interval(
        id='interval-component',
        interval=30*60*1000,  # in milliseconds (30 minutes)
        n_intervals=0
    )
])


@app.callback(
    Output('cheapest-offer-table', 'children'),
    [Input('budget-input', 'value'),
     Input('quantity-input', 'value'),
     Input('bullion-type-radio', 'value'),
     Input('interval-component', 'n_intervals')]
)
def update_table(budget, quantity, bullion_type, n):
    # Calculate the timestamp 30 minutes ago
    thirty_minutes_ago = datetime.datetime.now() - datetime.timedelta(minutes=30)

    # SQL query to fetch the latest complete session and its data from both tables
    query_item = f"""
    SELECT * 
    FROM item 
    WHERE (minimum <= {quantity}) 
      AND bullion_type = '{bullion_type}'
      AND session_id = (
        SELECT session_id 
        FROM item 
        GROUP BY session_id 
        HAVING MAX(timestamp) < '{thirty_minutes_ago.strftime('%Y-%m-%d %H:%M:%S')}' 
        ORDER BY MAX(timestamp) DESC 
        LIMIT 1
      )
    """

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
    conn = sqlite3.connect(db_path)
    # Load data into Pandas DataFrames
    items_df = pd.read_sql_query(query_item, conn)
    metal_prices_df = pd.read_sql_query(query_metal_price, conn)
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
        if lower <= quantity <= upper:
          return price  # Return the price directly
      return None  # Or handle the case where quantity is outside all ranges

    items_df['price'] = items_df.apply(
        lambda row: get_price(row['ranges'], quantity), axis=1
    )

    # Cheapest offer analysis and recommendations
    cheapest_offers = []

    # Get buying gold and silver coin values
    metal_price = metal_prices_df['buy_price'].iloc[0]

    for i, row in items_df.iterrows():
        print(row['price'])
        try :
            # Get the premium for the specified quantity
            lowest_premium = row['buy_premiums']  # Adjust index for 0-based list
            # Calculate total cost
            # Calculate total cost (using bullion_type)

            total_cost = (row['price']  + (lowest_premium / 100)*row['price']) * quantity * row['quantity']

            # Check if the offer meets the budget
            if total_cost <= budget:
                cheapest_offers.append({
                    'source': row['source'],
                    'premium': lowest_premium,
                    'quantity': row['premium_index'] + 1,
                    'total_cost': total_cost
                })
        except IndexError as e :
            print(e)  # Skip if the quantity index is out of range

    # Sort offers by premium (lowest first)
    cheapest_offers.sort(key=lambda x: x['premium'])

    # Create the cheapest offer table
    table_rows = [
        html.Tr([html.Th("Source"), html.Th("Premium"), html.Th("Quantity"), html.Th("Total Cost")])
    ]
    for offer in cheapest_offers:
        table_rows.append(
            html.Tr([html.Td(offer['source']), html.Td(offer['premium']), html.Td(offer['quantity']), html.Td(f"{offer['total_cost']:.2f} €")])
        )
    cheapest_offer_table = dbc.Table(table_rows, bordered=True)

    return cheapest_offer_table

if __name__ == '__main__':
    app.run_server(debug=True)