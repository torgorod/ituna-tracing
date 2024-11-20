import uuid

from random_address import real_random_address_by_state

import random

ITUNA_MENU = [
    "ITUNA SOUP",
    "TUNA SALAD",
    "TUNA MAKI",
    "TUNA SASHIMI",
    "TUNA NIGIRI",
    "SPICY TUNA NIGIRI",
    "ITUNA ROLL",
    "SPICY ITUNA ROLL"
]


def make_random_address():
    """
    Generate a random address and return it as a string value
    :return: Generated random address (str)
    """
    random_address = real_random_address_by_state("CA")
    return f"{random_address['address1']} {random_address['address2']} {random_address['city']}"


def make_random_sushi_order():
    """
    Generate a random sushi bar order
    :return: A dictionary containing items in the order
    """
    order = {}
    items_ordered = random.randint(2, 5)

    while len(order) < items_ordered:
        item_id_to_add = random.randint(0, len(ITUNA_MENU) - 1)
        item_to_add = ITUNA_MENU[item_id_to_add]
        if item_to_add not in order:
            item_count = random.randint(1, 5)
            order[item_to_add] = item_count

    return order


def make_random_order(order_type):
    """
    Generates a sample order placed by an ITuna customer
    :return: Dict containing order details
    """
    order = {
        "order_id": str(uuid.uuid4()),
        "customer_id": str(uuid.uuid4()),
        "order_details": make_random_sushi_order()
    }

    if order_type == "on-site":
        table_id = random.randint(1, 15)
        order["table"] = table_id
    elif order_type == "website":
        order["address"] = make_random_address()
    return order
