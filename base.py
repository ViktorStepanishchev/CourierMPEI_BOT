import sqlite3

order_base = sqlite3.connect('orders_base.db')
ff = order_base.cursor()


def create_db():
    ff.execute("""CREATE TABLE IF NOT EXISTS orders (
        num_iterat INTEGER PRIMARY KEY,
        num TEXT,
        orderr TEXT, 
        id TEXT,
        state_orderr TEXT
    )""")
    order_base.commit()


def check_user_in_db(id):
    ff.execute(f"SELECT id FROM orders WHERE id = ?", (id,))
    if ff.fetchone() is None:
        return True


def delete_user(id):
    ff.execute("DELETE FROM orders WHERE id = (?)", (id,))
    order_base.commit()
    output_base()


def take_value_from_db(need, where, us_inf):
    return ff.execute(f"SELECT {need} FROM orders WHERE {where} = (?)", (us_inf,)).fetchone()[0]


def add_user(description, id, num_now_order):
    ff.execute(f"INSERT INTO orders VALUES (?, ?, ?, ?, ?)", (1, num_now_order, description, id, "СВОБОДЕН"))
    order_base.commit()


def output_base():
    print("------UPDATE------")
    for value in order_base.execute("SELECT * FROM orders"):
             print(value)
    print("------------------")
    print(" ")