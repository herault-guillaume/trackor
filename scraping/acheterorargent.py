import time
import requests
from bs4 import BeautifulSoup
from models.model import Item
from models.pieces import weights
import traceback
from price_parser import Price
import logging
from datetime import datetime
import pytz
# Get the logger
logger = logging.getLogger(__name__)

CMN = {
    '1 oz philharmonique': 'or - 1 oz philharmonique',
    '1/2 oz philharmonique': 'or - 1/2 oz philharmonique',
    '1/4 oz philharmonique': 'or - 1/4 oz philharmonique',
    '1/10 oz philharmonique': 'or - 1/10 oz philharmonique',
    '4 ducats or': 'or - 4 ducats',
    '1 ducat or': 'or - 1 ducat',
    '8 florins 20 francs or 1892 refrappe': 'or - 8 florins 20 francs franz joseph I refrappe',
    '4 florins 10 francs 1892 refrappe': 'or - 4 florins 10 francs 1892 refrappe',
    '5 florins or wilhelmina 1912': 'or - 5 florins wilhelmina',
    '100 couronnes or françois joseph I': 'or - 100 couronnes françois joseph I',
    '20 couronnes or françois joseph I': 'or - 20 couronnes françois joseph I',
    '10 couronnes or françois joseph I': 'or - 10 couronnes françois joseph I',
    '8 florins 20 francs or franz joseph I': 'or - 8 florins 20 francs franz joseph I',
    '20 francs or': 'or - 20 francs fr',
    'souverain or georges V': 'or - 1 souverain georges V',
    'souverain or victoria voilée': 'or - 1 souverain victoria voilée',
    'souverain or victoria jubilee': 'or - 1 souverain victoria jubilee',
    'souverain or victoria Australie': 'or - 1 souverain victoria Australie',
    'souverain or victoria jeune': 'or - 1 souverain victoria jeune',
    'souverain or victoria jeune armoiries': 'or - 1 souverain victoria jeune armoiries',
    'demi souverain or georges V': 'or - 1/2 souverain georges V',
    'demi souverain or elizabeth II': 'or - 1/2 souverain elizabeth II',
    'demi souverain or edouard VII': 'or - 1/2 souverain edouart VII',
    'demi souverain or victoria voilée': 'or - 1/2 souverain victoria voilée',
    'demi souverain or victoria jubilée armoiries.': 'or - 1/2 souverain victoria jubilee arm.',
    '20 francs or napoléon III': 'or - 20 francs fr napoléon III',
    '20 francs or coq marianne': 'or - 20 francs fr coq marianne',
    '20 francs or génie debout': 'or - 20 francs fr génie debout',
    '20 francs or cérès': 'or - 20 francs fr cérès',
    '20 francs or louis-napoléon bonaparte': 'or - 20 francs fr louis-napoléon bonaparte',
    '20 francs or louis XVIII buste nu': 'or - 20 francs fr louis XVIII buste nu',
    '20 francs or louis XVIII buste habillé': 'or - 20 francs fr louis XVIII buste habillé',
    '20 francs or louis philippe lauré': 'or - 20 francs fr louis philippe laurée',
    '20 francs or louis philippe I nu': 'or - 20 francs fr louis philippe I nu',
    '20 francs or napoléon empereur': 'or - 20 francs fr napoléon empereur',
    '20 francs or charles X': 'or - 20 francs fr charles X',
    '10 francs or napoléon III': 'or - 10 francs fr napoléon III',
    '10 francs or cérès 1850-1851': 'or - 10 francs fr cérès 1850-1851',
    '40 francs or charles X': 'or - 40 francs fr charles X',
    '40 francs or louis philippe': 'or - 40 francs fr louis philippe',
    '40 francs or louis XVIII': 'or - 40 francs fr louis XVIII',
    '40 francs or napoléon empereur lauré': 'or - 40 francs fr napoléon empereur laurée',
    '100 francs or napoléon III tête laurée': 'or - 100 francs fr napoléon III tête nue',
    '100 francs or napoléon III tête nue': 'or - 100 francs fr napoléon III tête laurée',
    '10 florins or wilhelmina': 'or - 10 florins wilhelmina',
    '10 florins or willem III': 'or - 10 florins willem III',
    '50 pesos mex or': 'or - 50 pesos mex',
    '20 pesos or': 'or - 20 pesos mex',
    '10 pesos or': 'or - 10 pesos mex',
    '5 pesos or': 'or - 5 pesos mex',
    '2,5 pesos or': 'or - 2.5 pesos mex',
    '1 oz maple leaf': 'or - 1 oz maple leaf',
    '1/4 oz maple leaf': 'or - 1/4 oz maple leaf',
    '1/10 oz maple leaf': 'or - 1/10 oz maple leaf',
    '1 oz american eagle': 'or - 1 oz american eagle',
    '1/2 oz american eagle': 'or - 1/2 oz american eagle',
    '1/4 oz american eagle': 'or - 1/4 oz american eagle',
    '1/10 oz american eagle': 'or - 1/10 oz american eagle',
    '1 oz krugerrand': 'or - 1 oz krugerrand',
    '1/2 oz krugerrand': 'or - 1/2 oz krugerrand',
    '1/4 oz krugerrand': 'or - 1/4 oz krugerrand',
    '1/10 oz krugerrand': 'or - 1/10 oz krugerrand',
    '2 rand': 'or - 2 rand sud-africains',
    '1 oz britannia années différentes': 'or - 1 oz britannia',
    '20 francs or vreneli croix suisse': 'or - 20 francs sui vreneli croix',
    '20 francs or vreneli croix suisse refrappe': 'or - 20 francs sui vreneli croix 1935L refrappe',
    '20 francs or helvetia suisse': 'or - 20 francs sui confederatio',
    '1/10 oz kangourou / nugget': 'or - 1/10 oz nugget / kangourou',
    '1/2 oz kangourou': 'or - 1/2 oz kangourou',
    '1/2 oz kangourou / nugget': 'or - 1/2 oz nugget / kangourou',
    '1/20 oz maple leaf': 'or - 1/20 oz maple leaf',
    '20 dollars or liberté': 'or - 20 dollars liberté longacre',
    '20 dollars or saint gaudens': 'or - 20 dollars liberté st gaudens',
    '1/4 oz kangourou / nugget': 'or - 1/4 oz nugget / kangourou',
    '20 francs 8 forint or franz joseph I': 'or - 8 florins 20 francs franz joseph I',
    '100 couronnes or hongrie': 'or - 100 couronnes hongrie',
    '20 couronnes or hongrie': 'or - 20 couronnes hongrie',
    '10 couronnes or hongrie': 'or - 10 couronnes hongrie',
    '10 dollars or indien': 'or - 10 dollars tête indien',
    '10 dollars or liberté': 'or - 10 dollars liberté',
    '10 florins or wilhelmina cheveux longs': 'or - 10 florins wilhelmina cheveux longs',
    '20 francs or tunisie': 'or - 20 francs tunisie',
    '10 francs or tunisie': 'or - 10 francs tunisie',
    '10 francs or vreneli croix suisse': 'or - 10 francs sui vreneli croix',
    '20 lire or italie': 'or - 20 lire',
    '20 lire or umberto I': 'or - 20 lire umberto I',
    '20 lire or vittorio emanuele II': 'or - 20 lire vittorio emanuele II',
    '20 lire or vittorio emanuele II ancien': 'or - 20 lire vittorio emanuele II ancien',
    '20 lire or carl albert': 'or - 20 lire carl albert',
    '20 lire or napoléon I': 'or - 20 lire carl albert',
    '40 lire or napoléon I': 'or - 40 lire napoléon I',
    '40 lire or maria luigia': 'or - 40 lire maria luigia',
    '10 lire or vittorio emanuele II': 'or - 10 lire vittorio emanuele II',
    '20 mark or wilhelm II': 'or - 20 mark wilhelm I',
    '20 mark or wilhelm I': 'or - 20 mark wilhelm II',
    '20 mark or ludwig II': 'or - 20 mark ludwig II',
    '10 mark or wilhelm II': 'or - 10 mark wilhelm II',
    '10 mark or wilhelm I': 'or - 10 mark wilhelm I',
    '100 pesos or liberté': 'or - 100 pesos liberté chili',
    '50 pesos or liberté': 'or - 50 pesos liberté chili',
    '50 pesos or mex': 'or - 50 pesos mex',
    '5 roubles nicolas II': 'or - 5 roubles nicolas II',
    '10 roubles nicolas II 2e choix': 'or - 10 roubles nicolas II',
    '10 roubles chervonetz': 'or - 10 roubles chervonetz',
    '500 yuan panda 2024 30g': 'or - 500 yuan panda',
    '200 yuan panda 2024 15g': 'or - 200 yuan panda',
    '100 yuan panda 2024 8g': 'or - 100 yuan panda',
    '50 yuan panda 2024 3g': 'or - 50 yuan panda',
    '10 yuan panda 2024 1g': 'or - 10 yuan panda',
    '500 yuan panda 2013 1 oz': 'or - 1 oz 500 yuan panda',
    '500 yuan panda 2008 1 oz': 'or - 1 oz 500 yuan panda',
    '200 yuan panda 2019 15g': 'or - 200 yuan panda',
    '50 yuan panda 2016 3g': 'or - 50 yuan panda',
    '20 francs or union latine léopold II': 'or - 20 francs bel leopold II',
    '20 francs or léopold I': 'or - 20 francs bel leopold I',
    '20 francs or albert I': 'or - 20 francs bel albert I',
    '50 écus or charles quint': 'or - 50 écus charles quint',
    '100 écus or': 'or - 100 écus',
    '100 francs or albert I': 'or - 100 francs bel albert I',
    '100 francs or charles III': 'or - 100 francs charles III',
    '100 lire or carl albert': 'or - 100 lires carl albert',
    '20 lire pie IX 1869 R': 'or - 20 lire pie IX 1869 R',
    '20 mark or Friedrich I (Baden)': 'or - 20 mark Friedrich I (Baden)',
    '20 mark or hambourg': 'or - 20 mark hambourg',
    '20 mark or wilhelm II uniforme': 'or - 20 mark wilhelm II uniforme',
    '20 mark or wilhelm II württemberg': 'or - 20 mark wilhelm II württemberg',
    '20 pesos or liberté': 'or - 20 pesos chili',
    '25 écus or': 'or - 25 écus or',
    '25 pesetas or alphonse XII': 'or - 25 pesetas or alphonse XII',
    '25 pesetas or alphonse XII rouflaq.': 'or - 25 pesetas or alphonse XII rouflaq.',
    '5 dollars or indien 2e choix': 'or - 5 dollars tête indien',
    '5 dollars or liberté': 'or - 5 dollars liberté',
    'souverain or': 'or - 1 souverain',

    'Monster box 500 philharmonique 1 oz': ('ar - 1 oz philharmonique',500),
    'Monster box 500 maple leaf 1 oz': ('ar - 1 oz maple leaf',500),
    'Monster box 500 silver eagle 1 oz': ('ar - 1 oz silver eagle',500),
    '1 dollar peace argent': 'ar - 1 dollar peace',
    '1 dollar morgan argent': 'ar - 1 dollar morgan',
    '1 dollar commémorative argent': 'ar - 1 dollar commémorative argent',
    'half dollar kennedy argent': 'ar - 0.5 dollar kennedy',
    'half dollar walking liberty argent': 'ar - 0.5 dollar walking liberty',
    'half dollar franklin argent': 'ar - 0.5 dollar franklin',
    'quarter dollar washington argent': 'ar - 0.25 dollar washington',
    'quarter dollar standing liberty argent': 'ar - 0.25 dollar standing liberty',
    'one dime roosevelt argent': 'ar - 1 dime roosevelt',
    'one dime mercury argent': 'ar - 1 dime mercury',
    'one dime barber argent': 'ar - 1 dime barber',
    '5 francs léopold II argent': 'ar - 5 francs léopold II',
    '5 francs léopold I tête laurée argent': 'ar - 5 francs léopold I tête laurée',
    '5 francs léopold I tête nue argent': 'ar - 5 francs léopold I tête nue',
    '2 francs belgique argent': 'ar - 2 francs belgique',
    '1 franc albert / léopold II': 'ar - 1 franc albert / léopold II',
    '50 cts helvetia Suisse': 'ar - 50 cts sui helvetia',
    '1 franc helvetia Suisse': 'ar - 1 franc sui helvetia',
    '250 francs baudouin roi des belges argent': 'ar - 250 francs baudouin roi des belges',
    '5 francs berger suisse': 'ar - 5 francs sui berger',
    '50 francs hercule': 'ar - 50 francs fr hercule (1974-1980)',
    '10 francs hercule': 'ar - 10 francs fr hercule (1965-1973)',
    '5 francs semeuse': 'ar - 5 francs fr semeuse (1959-1969)',
    '1 gulden juliana argent': 'ar - 1 gulden juliana',
    '5 francs semeuse x100': ('ar - 5 francs fr semeuse (1959-1969)',100),
    '5 francs semeuse x1000': ('ar - 5 francs fr semeuse (1959-1969)',1000),
    '100 francs commémorative': 'ar - 100 francs fr',
    '2 francs semeuse': 'ar - 2 francs fr semeuse',
    '1 franc semeuse': 'ar - 1 franc fr semeuse',
    '50 centimes semeuse': 'ar - 50 centimes francs fr semeuse',
    '5 francs cérès': 'ar - 5 francs fr cérès',
    '5 francs hercule': 'ar - 5 francs fr hercule',
    '5 francs louis philippe': 'ar - 5 francs fr louis philippe',
    '5 francs napoléon III tête laurée': 'ar - 5 francs fr napoléon III tête laurée',
    '5 mark wilhelm II argent': 'ar - 5 mark wilhelm II',
    '5 mark wilhelm I argent': 'ar - 5 mark wilhelm I',
    '10 francs turin': 'ar - 10 francs fr turin (1860-1928)',
    '100 francs 4 rois': 'ar - 100 francs fr',
    '20 francs mercure': 'ar - 20 francs bel mercure',
    '2 reich mark argent': 'ar - 2 reich mark',
    '2,5 gulden juliana argent': 'ar - 2,5 gulden juliana',
    '5 reich mark argent': 'ar - 5 reich mark',
    '20 francs turin': 'ar - 20 francs fr turin (1929-1939)',
    '5 deutsche mark argent': 'ar - 5 deutsche mark',
    '5 lire vittorio emanuele II argent': 'ar - 5 lire vittorio emanuele II',
}

def get_price_for(session_prod,session_staging,session_id,buy_price_gold,buy_price_silver):

    base_url = 'https://www.acheter-or-argent.fr/index2.php/categorie-produit/'
    urls = [base_url+'pieces-dor/page/{i}/'.format(i=i) for i in range(1,17)] + [base_url+'/pieces-dargent/page/{i}/'.format(i=i) for i in range(1,25)]
    logger.debug(f"Scraping started for {base_url}") # Example debug log
    delivery_ranges = [
      (0.0, 500.0, 18.0),
      (500.0, 1000.0, 15.0),
      (1000.0, 3000.0, 20.0),
      (3000.0, 10000.0, 30.0),
      (10000.0, 20000.0, 45.0),
      (20000.0, 50000.0, 90.0),
      (50000.0, 75000.0, 150.0),
      (75000.0, 100000.0, 180.0),
      (100000.0, 150000.0, 240.0),
      (150000.0, 9999999999.0, 0.0)  # Use float('inf') for infinity
  ]
    print(base_url)

    for url in urls :
        time.sleep(3
                   )
        try:
            response = requests.get(url)
            response.raise_for_status()
        except Exception as e:
            traceback.print_exc()
            continue
        soup = BeautifulSoup(response.content, 'html.parser')

        div_product= soup.find_all('li',class_='type-product')

        for product in div_product :
            try :

                product_name = product.find('h2',class_='woocommerce-loop-product__title').text
                source = product.find('a',class_='woocommerce-LoopProduct-link')['href']
                span_price = product.find('span',class_='price').find_all('span',class_='woocommerce-Price-amount')

                if len(span_price)>1:
                    price = Price.fromstring(span_price[1].text)
                else:
                    price = Price.fromstring(span_price[0].text)

                item_data = CMN[product_name]

                minimum = 1
                quantity = 1

                if isinstance(item_data, tuple):
                    name = item_data[0]
                    quantity = item_data[1]
                    bullion_type = item_data[0][:2]
                else:
                    name = item_data
                    bullion_type = item_data[:2]

                if bullion_type == 'or':
                    buy_price = buy_price_gold
                else:
                    buy_price = buy_price_silver

                print(price,name,source)

                def price_between(value, ranges):
                    """
                    Returns the price per unit for a given quantity.
                    """

                    for min_qty, max_qty, price in ranges:
                        if min_qty <= value <= max_qty:
                            if isinstance(price, Price):
                                return price.amount_float
                            else:
                                return price

                price_ranges = ([minimum, 999999999, price]),

                coin = Item(name=name,
                            price_ranges=';'.join(['{min_}-{max_}-{price}'.format(min_=r[0],max_=r[1],price=r[2].amount_float) for r in price_ranges]),
                            buy_premiums=';'.join(
                                ['{:.2f}'.format(((price_between(minimum,price_ranges)/quantity + price_between(price_between(minimum,price_ranges)*minimum,delivery_ranges)/(quantity*minimum)) - (buy_price * weights[name])) * 100.0 / (buy_price * weights[name])) for i in range(1, minimum)] +
                                ['{:.2f}'.format(((price_between(i,price_ranges)/quantity + price_between(price_between(i,price_ranges),delivery_ranges)/(quantity*i)) - (buy_price * weights[name])) * 100.0 / (buy_price * weights[name])) for i in range(minimum, 151)]
                            ),
                            delivery_fees=';'.join(['{min_}-{max_}-{price}'.format(min_=r[0],max_=r[1],price=r[2]) for r in delivery_ranges]),
                            source=source,
                            session_id=session_id,
                            bullion_type=bullion_type,
                            quantity=quantity,
                            minimum=minimum, timestamp=datetime.now(pytz.timezone('CET')).replace(second=0, microsecond=0)
)
                session_prod.add(coin)
                session_prod.commit()
                session_prod.expunge(coin)
                session_staging.add(coin)
                session_staging.commit()

            except KeyError as e:

                logger.error(f"KeyError: {product_name}")  # Log the product name

            except Exception as e:
                logger.error(f"An error occurred while processing: {e}")
                traceback.print_exc()