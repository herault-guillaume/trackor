import pandas as pd
from sqlalchemy import create_engine
import pandas as pd
import numpy as np
from scipy import signal
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from urllib.parse import urlparse
from model import poids_pieces_or

from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.stattools import adfuller
from sklearn.metrics import mean_squared_error


# Configuration de la base de données
# Permanently changes the pandas settings
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

Base = declarative_base()
engine = create_engine(r'sqlite:///C:\Users\Guillaume Hérault\PycharmProjects\trackor\models\pieces_or.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

# 2. Write your SQL query
gp = "SELECT * FROM gold_price"  # Replace with your actual table name and desired columns
cp = "SELECT * FROM coin_price"  # Replace with your actual table name and desired columns

# 3. Execute the query and fetch the results into a DataFrame

cp_df = pd.read_sql_query(cp, engine)
gp_df = pd.read_sql_query(gp, engine)

# Récupérer les noms uniques de pièces et les sources uniques
unique_coins =  ['or - 20 francs coq marianne',
                 'or - 20 francs napoléon III',
                 'or - 20 dollars liberté longacre',
                 'or - 20 francs confederatio suisse',
                 'or - 20 francs union latine',
                 'or - 10 dollars liberté',
                 'or - 10 dollars tête indien',
                 ]

unique_sources = cp_df['source'].apply(lambda x: urlparse(x).netloc).unique()

results = []

# Itérer sur chaque combinaison unique de nom de pièce et de source

for coin_name in unique_coins:
    for source in unique_sources:
        # Filtrer les données pour la pièce et la source actuelles
        # Filtrer les données pour la pièce, la source (domaine) actuelles
        current_coin_data = cp_df[(cp_df['nom'] == coin_name) &
                                      (cp_df['source'].apply(lambda x: urlparse(x).netloc) == source)].copy()
        if current_coin_data.empty:
            continue  # Passer à la combinaison suivante si aucune donnée n'est trouvée

        # Get gold weight for the current coin
        gold_weight = poids_pieces_or.get(coin_name)
        if gold_weight is None:
            print(f"Warning: Gold weight not found for coin '{coin_name}'. Skipping...")
            continue

        gp_df['timestamp_'] = pd.to_datetime(gp_df['timestamp'])
        gp_df.set_index('timestamp_', inplace=True)

        current_coin_data = current_coin_data.resample('D').last()
        gp_df = gp_df.resample('D').last()
        # Calculate price per gram for the coin
        current_coin_data['price_per_gram'] = current_coin_data['j_achete'] / gold_weight

        current_coin_data['premium'] = current_coin_data['j_achete'] - current_coin_data['price_per_gram']
        # Préparation des données
        current_coin_data['timestamp'] = pd.to_datetime(current_coin_data['timestamp'])
        current_coin_data.set_index('timestamp', inplace=True)



        gp_df['gold_price_change'] = gp_df['sell_price'].pct_change()
        print(gp_df)
        print(current_coin_data)
        result = adfuller(current_coin_data['premium'])
        print('ADF Statistic: %f' % result[0])
        print('p-value: %f' % result[1])
        print('Critical Values:')
        for key, value in result[4].items():
            print('\t%s: %.3f' % (key, value))
        print(coin_name,source)
        break
 # Or use .diff() for absolute difference

        # Fit the main time series model to predict the premium
        model = ARIMA(current_coin_data['premium'], exog=gp_df['gold_price_change'], order=(p, d, q))
        model_fit = model.fit()

        # Check if there's enough data after resampling
        if len(current_coin_data) < 2 or len(gp_df) < 2:
            print(f"Warning: Not enough data for '{coin_name}' from '{source}'. Skipping...")
            continue

        # Split data into training and validation sets
        train_size = int(len(current_coin_data) * 0.8)  # 80% for training, 20% for validation
        train_data, val_data = current_coin_data[:train_size], current_coin_data[train_size:]
        train_gold, val_gold = gp_df[:train_size], gp_df[train_size:]

        # Calculate gold price changes for both training and validation sets
        train_gold['gold_price_change'] = train_gold['sell_price'].pct_change()
        val_gold['gold_price_change'] = val_gold['sell_price'].pct_change()

        best_model = None
        best_mse = float('inf')

        # Iterate over different p, d, q combinations
        for p in range(0, 3):  # Adjust the range as needed
            for d in range(0, 2):
                for q in range(0, 3):
                    try:
                        # Fit the ARIMA model on the training set
                        model = ARIMA(train_data['premium'], exog=train_gold['gold_price_change'], order=(p, d, q))
                        model_fit = model.fit()

                        # Make predictions on the validation set
                        predictions = model_fit.predict(start=val_data.index[0], end=val_data.index[-1],
                                                        exog=val_gold['gold_price_change'])

                        # Calculate MSE on the validation set
                        mse = mean_squared_error(val_data['premium'], predictions)

                        if mse < best_mse:
                            best_mse = mse
                            best_model = model_fit
                            best_params = (p, d, q)

                    except Exception as e:
                        print(f"Error fitting ARIMA({p}, {d}, {q}) model for '{coin_name}' from '{source}': {e}")

        if best_model:
            results.append({'Coin': coin_name, 'Source': source, 'Lag (Jours)': lag,
                            'Best ARIMA Params': best_params, 'Best MSE': best_mse,
                            'ARIMA Model': best_model})

    # Create the final DataFrame from the results
    results_df = pd.DataFrame(results)
    print(results_df)

    # Créer le DataFrame final à partir des résultats
print(pd.DataFrame(results))