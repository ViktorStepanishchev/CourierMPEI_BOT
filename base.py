import sqlite3

order_base = sqlite3.connect('orders_base.db')
ff = order_base.cursor()

ff.execute("""CREATE TABLE IF NOT EXISTS orders (
    num_iterat BIGINT,
    num TEXT,
    orderr TEXT, 
    id TEXT,
    state_orderr TEXT
)""")
ff.execute("DELETE FROM orders")
ff.execute(f"INSERT INTO orders VALUES (?, ?, ?, ?, ?)", (0, 0, 0, 0, 0))
order_base.commit()

def output_base():
    print("------UPDATE------")
    for value in order_base.execute("SELECT * FROM orders"):
             print(value)
    print("------------------")
    print(" ")

