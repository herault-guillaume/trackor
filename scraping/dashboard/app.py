import dash
from datetime import datetime
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import sqlite3

# Connect to your SQLite database
db_path = r'C:\Users\Guillaume Hérault\PycharmProjects\trackor\models\pieces_or.db'

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    html.H1("Buy Premiums by Name"),

    dcc.Dropdown(
        id='name-dropdown',
        # We will update the options in a callback
    ),

    dcc.Graph(id='premiums-graph'),

    dcc.Interval(
        id='interval-component',
        interval=30*60*1000,  # in milliseconds (30 minutes)
        n_intervals=0
    )
])

@app.callback(
    Output('name-dropdown', 'options'),
    [Input('interval-component', 'n_intervals')]
)
def update_dropdown_options(n):
    conn = sqlite3.connect(db_path)
    # Calculate the timestamp 30 minutes ago
    thirty_minutes_ago = datetime.datetime.now() - datetime.timedelta(minutes=30)

    # SQL query to fetch the latest complete session and its data
    query = f"""
    SELECT DISTINCT name
    FROM item 
    WHERE session_id = (
        SELECT session_id 
        FROM item 
        GROUP BY session_id 
        HAVING MAX(timestamp) < '{thirty_minutes_ago.strftime('%Y-%m-%d %H:%M:%S')}' 
        ORDER BY MAX(timestamp) DESC 
        LIMIT 1
    )
    """

    # Load data into a Pandas DataFrame using the optimized query
    df = pd.read_sql_query(query, conn)
    conn.close()

    return [{'label': i, 'value': i} for i in df['name'].unique()]


@app.callback(
    Output('premiums-graph', 'figure'),
    [Input('name-dropdown', 'value'), Input('interval-component', 'n_intervals')],
    [State('name-dropdown', 'options')]
)
def update_graph(selected_name, n, dropdown_options):
    # Calculate the timestamp 30 minutes ago
    thirty_minutes_ago = datetime.datetime.now() - datetime.timedelta(minutes=30)

    # SQL query to fetch the latest complete session and its data
    query = f"""
    SELECT * 
    FROM item 
    WHERE session_id = (
        SELECT session_id 
        FROM item 
        GROUP BY session_id 
        HAVING MAX(timestamp) < '{thirty_minutes_ago.strftime('%Y-%m-%d %H:%M:%S')}' 
        ORDER BY MAX(timestamp) DESC 
        LIMIT 1
    )
    """
    conn = sqlite3.connect(db_path)
    # Load data into a Pandas DataFrame using the optimized query
    filtered_df = pd.read_sql_query(query, conn)
    conn.close()
    # Use .loc to modify the DataFrame
    filtered_df.loc[:, 'buy_premiums'] = filtered_df['buy_premiums'].apply(
        lambda x: [float(i) for i in x.split(';')[:-1]]
    )

    if selected_name is None:
        # Set a default value if nothing is selected yet
        selected_name = dropdown_options[0]['value'] if dropdown_options else None

    # Create the figure with separate lines and colors
    fig = px.line(title=f"Prime pour {selected_name}")

    if selected_name:
        filtered_df = filtered_df[filtered_df['name'] == selected_name].copy()
        # Add a separate line for each row with x-axis representing number of coins
        for i, row in filtered_df.iterrows():
            num_coins = 150  # Or calculate from row['buy_premiums'] if needed
            x_values = list(range(1, num_coins + 1))
            fig.add_scatter(x=x_values,
                            y=row['buy_premiums'],
                            name=f"{row['source']}",
                            hovertemplate=f"<b>Source: {row['source']}</b><br>Prime: %{{y}}<br>Pièces: %{{x}}<extra></extra>")

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)