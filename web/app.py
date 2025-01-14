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
