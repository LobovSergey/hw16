import json

from flask_sqlalchemy import SQLAlchemy
from flask import Flask, jsonify, request
from utils import load_data_users, load_data_offer, load_data_order, user_transformation, order_transformation, \
    offer_transformation

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///sqlite3.db'
app.config['JSON_AS_ASCII'] = False
db = SQLAlchemy(app)


class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    description = db.Column(db.String(300))
    start_date = db.Column(db.Text)
    end_date = db.Column(db.Text)
    address = db.Column(db.String(200))
    price = db.Column(db.Integer)
    customer_id = db.Column(db.Integer)
    executor_id = db.Column(db.Integer)


class Offer(db.Model):
    __tablename__ = 'offer'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    order = db.relationship('Order')
    executor_id = db.Column(db.Integer)


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String)
    age = db.Column(db.Integer)
    email = db.Column(db.String(100))
    role = db.Column(db.String(100))
    phone = db.Column(db.String(100))
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    order = db.relationship('Order')
    offer_id = db.Column(db.Integer, db.ForeignKey('offer.id'))
    offer = db.relationship('Offer')


db.drop_all()
db.create_all()

data_users = load_data_users()
data_orders = load_data_order()
data_offer = load_data_offer()

for user in data_users:
    user_one = User(
        id=user['id'],
        first_name=user['first_name'],
        last_name=user['last_name'],
        age=user['age'],
        email=user['email'],
        role=user['role'],
        phone=user['phone']
    )
    db.session.add(user_one)
    db.session.commit()

for offer in data_offer:
    offer_one = Offer(
        id=offer['id'],
        order_id=offer['order_id'],
        executor_id=offer['executor_id'],
    )
    db.session.add(offer_one)
    db.session.commit()

for order in data_orders:
    order_one = Order(
        id=order['id'],
        name=order['name'],
        description=order['description'],
        start_date=order['start_date'],
        end_date=order['end_date'],
        address=order['address'],
        price=order['price'],
        customer_id=order['customer_id'],
        executor_id=order['executor_id'],
    )
    db.session.add(order_one)
    db.session.commit()


@app.route('/')
@app.route('/users', methods=['GET', 'POST'])
def all_users():
    if request.method == 'GET':
        response = db.session.query(User).all()
        response_json = [user_transformation(line) for line in response]
        return jsonify(response_json)
    elif request.method == 'POST':
        data_json = request.json
        new_user = User(data_json)
        db.session.add(new_user)
        db.session.commit()
        return f'{new_user.first_name} added'
    else:
        return 'Wrong response'


@app.route('/users/<int:pk>', methods=['GET', 'PUT', 'DELETE'])
def unique_users(pk):
    response = db.session.query(User).get(pk)
    if request.method == 'GET':
        response_json = user_transformation(response)
        return jsonify(response_json)
    elif request.method == 'PUT':
        data = request.json
        response.id = data['id']
        response.first_name = data['first_name'],
        response.last_name = data['last_name'],
        response.age = data['age'],
        response.email = data['email'],
        response.role = data['role'],
        response.phone = data['phone']
        db.session.add(response)
        db.session.commit()
        return f'User {pk} edited'
    elif request.method == 'DELETE':
        db.session.filter(User.id == pk).delete()
        db.session.commit()
        return f'{pk} deleted'
    else:
        return 'Wrong response'


@app.route('/orders', methods=['GET', 'POST'])
def all_orders():
    if request.method == 'GET':
        response = db.session.query(Order).all()
        response_json = [order_transformation(line) for line in response]
        return jsonify(response_json)
    elif request.method == 'POST':
        data_json = request.json
        new_order = Order(data_json)
        db.session.add(new_order)
        db.session.commit()
        return f'Order №{new_order.id} added'
    else:
        return 'Wrong response'


@app.route('/orders/<int:pk>', methods=['GET', 'PUT', 'DELETE'])
def unique_orders(pk):
    response = db.session.query(Order).get(pk)
    if request.method == 'GET':
        response_json = order_transformation(response)
        return jsonify(response_json)
    elif request.method == 'PUT':
        data = request.json
        response.id = data['id'],
        response.name = data['name'],
        response.description = data['description'],
        response.start_date = data['start_date'],
        response.end_date = data['end_date'],
        response.address = data['address'],
        response.price = data['price'],
        response.customer_id = data['customer_id'],
        response.executor_id = data['executor_id'],
        db.session.add(response)
        db.session.commit()
        return f'Order {pk} edited'
    elif request.method == 'DELETE':
        db.session.filter(Order.id == pk).delete()
        db.session.commit()
        return f'{pk} deleted'
    else:
        return 'Wrong response'


@app.route('/offers', methods=['GET', 'POST'])
def all_offers():
    if request.method == 'GET':
        response = db.session.query(Offer).all()
        response_json = [offer_transformation(line) for line in response]
        return jsonify(response_json)
    elif request.method == 'POST':
        data_json = request.json
        new_offer = Offer(data_json)
        db.session.add(new_offer)
        db.session.commit()
        return f'Offer №{new_offer.id} added'
    else:
        return 'Wrong response'


@app.route('/offers/<int:pk>', methods=['GET', 'PUT', 'DELETE'])
def unique_offer(pk):
    response = db.session.query(Offer).get(pk)
    if request.method == 'GET':
        response_json = offer_transformation(response)
        return jsonify(response_json)
    elif request.method == 'PUT':
        data = request.json
        response.id = data['id'],
        response.order_id = data['order_id'],
        response.executor_id = data['executor_id']
        db.session.add(response)
        db.session.commit()
        return f'Offer {pk} edited'
    elif request.method == 'DELETE':
        db.session.filter(Offer.id == pk).delete()
        db.session.commit()
        return f'{pk} deleted'
    else:
        return 'Wrong response'


if __name__ == '__main__':
    app.run(debug=True)
