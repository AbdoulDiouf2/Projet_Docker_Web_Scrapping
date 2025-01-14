from flask import Flask, render_template, jsonify, request
from models import Database
from config import Config
 
app = Flask(__name__)
app.config.from_object(Config)
 
db = Database()
 
@app.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    data = db.get_all_products(page=page)
    return render_template('index.html',
                         products=data['products'],
                         current_page=data['current_page'],
                         total_pages=data['pages'])
@app.route('/search')
def search():
    search_term = request.args.get('term', '')
    if not search_term:
        return jsonify({
            'Boulanger': [],
            'CDiscount': [],
            'eBay': []
        })
   
    products = db.search_products(search_term)
    return jsonify(products)
 
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)