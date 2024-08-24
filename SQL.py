import psycopg2

# Создание базы данных

def create_db(conn):
 
    cur = conn.connect('tinder_db')
    cur.cursor()
    cur.execute(''' CREATE TABLE clients 
    (id INTEGER PRIMARY KEY, name VARCHAR(20) NOT NULL, first_name VARCHAR(20) NOT NULL, 
    email VARCHAR(20) NOT NULL)
    ''')

    cur.execute(''' CREATE TABLE phones_number
    (id SERIAL PRIMARY KEY, client_id INT REFERENCES clients(id) , phones VARCHAR(15) NOT NULL)
    ''')

    conn.close()
    cur.close()

# Добавление нового клиента

def new_client(conn, first_name, name, email):

    cur = conn.cursor()
    cur.execute(
        "INSERT INTO clients (first_name, name, email) VALUES (%s, %s, %s)",
        (first_name, name, email)
    )

    cur.commit()
    cur.close()
    conn.close()

# Добавление номера телефона

def new_phones(conn, client_id, phones):

    cur = conn.cursor()
    cur.execute(
        "INSERT INTO phones_number (client_id, phones) VALUES (%s, %s)",
        (client_id, phones)
    )

    cur.commit()
    cur.close()
    conn.close()

# Изменение данных о клиенте

def customer_data_change(conn, client_id, name=None, first_name=None, email=None, phones=None):

    cur = conn.cursor()

    if email:
        cur.execute(
            " UPDATE clients SET email = %s WHERE id = %s ",
            (email, name, first_name)
        )

    if first_name:
        cur.execute(
            "UPDATE clients SET first_name = %s AND  client_id = %s ",
            (client_id,)
        )

    if phones:
        cur.execute(
            "DELETE FROM phones_number WHERE client_id = %s"
        )

        for phone in phones:
            cur.execute(
                "INSERT INTO phones_number (client_id, number) VALUES (%s, %s)",
                (client_id, phone)
            )

    conn.commit()
    cur.close()

# Удаление номера телефона для существующего клиента

def delete_number(conn, client_id, phones):

    cur = conn.cursor()

    if phones:
        for phone in phones:
            cur.execute(
                "DELETE FROM phones_number WHERE client_id = %s AND phone = %s ",
                (client_id, phone)
            )

    conn.commit()
    cur.close()

# Удаление существующего клиента

def delete_client(conn, client_id):

    cur = conn.cursor()

    if client_id:
        cur.execute(
            "DELETE FROM phones_number WHERE client_id = %s",
            (client_id,)
        )

        cur.execute(
            "DELETE FROM clients WHERE id = %s",
            (client_id,)
        )

    conn.commit()
    cur.close()

# Нахождение клиента по данным

def find_client(conn, first_name=None, last_name=None, email=None, phone=None):

    cur = conn.cursor()

    if first_name:
        cur.execute(
            "SELECT * FROM clients WHERE first_name LIKE %s ",
            (first_name,)
        )

    if last_name:
        cur.execute(
            "SELECT * FROM clients WHERE last_name LIKE %s ",
            (last_name,)
        )

    if email:
        cur.execute(
            "SELECT * FROM clients WHERE email LIKE %s ",
            (email,)
        )

    if phone:
        cur.execute(
            "SELECT * FROM clients WHERE first_name LIKE %s ",
            (phone,)
        )
        
    conn.commit()
    cur.close()

# Вызов результата

with psycopg2.connect(database='tinder_db', user='postgres', password='12345') as conn:

    cur = conn.cursor()
    cur.execute("SELECT * FROM clients;")
    result = cur.fetchall()

    for row in result:
        print(row)

    conn.close()



