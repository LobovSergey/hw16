import json


def load_data_users():
    with open('users.json', 'r', encoding='utf-8') as f:
        return json.load(f)


def load_data_offer():
    with open('offers.json', 'r', encoding='utf-8') as f:
        return json.load(f)


def load_data_order():
    with open('orders.json', 'r', encoding='utf-8') as f:
        return json.load(f)


def user_transformation(user):
    return {
        "id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "age": user.age,
        "email": user.email,
        "role": user.role,
        "phone": user.phone
    }


def order_transformation(order):
    return {
        "id": order.id,
        "name": order.name,
        "description": order.description,
        "start_date": order.start_date,
        "end_date": order.end_date,
        "address": order.address,
        "price": order.price,
        "customer_id": order.customer_id,
        "executor_id": order.executor_id
    }


def offer_transformation(offer):
    return {
        "id": offer.id,
        "order_id": offer.order_id,
        "executor_id": offer.executor_id
    }