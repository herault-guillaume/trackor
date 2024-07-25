from flask import Flask, render_template
from scraping.scraper_offres import scrape_page

app = Flask(__name__)

@app.route('/')
def index():
    offres = scrape_page('https://www.exemple-site-pieces-or.com/')  # Remplacez par l'URL réelle
    return render_template('index.html', offres=offres)

if __name__ == '__main__':
    app.run(debug=True)