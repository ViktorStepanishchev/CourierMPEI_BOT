import random

all_id_orders = []
def create_num_order():
    return random.randint(1000, 9999)

def prov(all_id_orders):
    a = create_num_order()
    if a not in all_id_orders:
        all_id_orders.append(a)
        return a
    else:
        prov(all_id_orders)
prov(all_id_orders)
