import random
import base

all_id_orders = []
def create_num_order():
    return random.randint(10000, 99999)

def prov(all_id_orders):
    a = create_num_order()
    if a not in all_id_orders:
        all_id_orders.append(a)
        return a
    else:
        prov(all_id_orders)
prov(all_id_orders)

def last_string_bd():
    last_string = 0
    for value in base.order_base.execute("SELECT * FROM orders"):
        last_string = value
    return last_string