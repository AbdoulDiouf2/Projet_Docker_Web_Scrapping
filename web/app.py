from flask import Flask, render_template, jsonify, request
from models import Database
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

@app.route('/')
def index():
    db = Database()
    # Utilisation de get_all_products pour la vue par défaut
    products = db.get_all_products()
    return render_template('index.html', products=products)

@app.route('/search')
def search():
    search_term = request.args.get('term', '')
    if not search_term:
        return jsonify({
            'Boulanger': [],
            'CDiscount': [],
            'Darty': []
        })
    
    db = Database()
    products = db.search_products(search_term)
    return jsonify(products)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)