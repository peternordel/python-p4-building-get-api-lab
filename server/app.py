#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def bakeries():
    # GET /bakeries: returns an array of JSON objects for all bakeries in the database.
    
    bakeries = []
    for bakery in Bakery.query.all():
        bakery_dict = bakery.to_dict()
        bakeries.append(bakery_dict)

    response = make_response(
        jsonify(bakeries),
        200
    )

    return response

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    # GET /bakeries/<int:id>: returns a single bakery as JSON with its baked goods nested in an array. Use the id from the URL to look up the correct bakery.
    bakery = Bakery.query.filter(Bakery.id == id).first()

    bakery_dict = bakery.to_dict()

    response = make_response(
        jsonify(bakery_dict),
        200
    )

    response.headers["Content-Type"] = "application/json"

    return response

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    # GET /baked_goods/by_price: returns an array of baked goods as JSON, sorted by price in descending order. (HINT: how can you use SQLAlchemy to sort the baked goods in a particular order?)
    baked_goods = []
    for baked_good in BakedGood.query.order_by(-BakedGood.price).all():
        baked_good_dict = baked_good.to_dict()
        baked_goods.append(baked_good_dict)

    response = make_response(
        jsonify(baked_goods),
        200
    )

    return response

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    # GET /baked_goods/most_expensive: returns the single most expensive baked good as JSON. (HINT: how can you use SQLAlchemy to sort the baked goods in a particular order and limit the number of results?)
    baked_good = BakedGood.query.order_by(-BakedGood.price).first()

    baked_good_dict = baked_good.to_dict()

    response = make_response(
        jsonify(baked_good_dict),
        200
    )

    response.headers["Content-Type"] = "application/json"

    return response

if __name__ == '__main__':
    app.run(port=555, debug=True)
