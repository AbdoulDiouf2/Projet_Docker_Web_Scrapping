from flask import Flask, render_template, jsonify, request
from models import Database
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = Database()

@app.route('/')
def index():
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
    
    products = db.search_products(search_term)
    return jsonify(products)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)