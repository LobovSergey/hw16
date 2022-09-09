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
