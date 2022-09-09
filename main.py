from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from utils import load_data_users, load_data_offer, load_data_order

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

if __name__ == '__main__':
    app.run(debug=True)
