import psycopg2

def create_db():
            # создание таблиц
    with conn.cursor() as cur:
        cur.execute("""
        CREATE TABLE IF NOT EXISTS client(
            client_id SERIAL PRIMARY KEY,
            first_name VARCHAR(40) NOT NULL,
            last_name VARCHAR(40) NOT NULL,
            email VARCHAR(40) NOT NULL
        );
        """)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS phone(
            phone_id SERIAL PRIMARY KEY,
            number INTEGER NOT NULL,
            client_id INTEGER NOT NULL REFERENCES client(client_id)
            ON DELETE CASCADE
        );
        """)
        conn.commit()  # фиксируем в БД
        print ("БД успешно созданы.")

def add_client(first_name, last_name, email):
    with conn.cursor() as cur:
        cur.execute("""
        INSERT INTO client(first_name, last_name, email) VALUES(%s, %s, %s) RETURNING first_name, last_name, email;
        """,(first_name, last_name, email));
        print('Client added:', cur.fetchall())

def del_db ():
    with conn.cursor() as cur:
        cur.execute("""
        DROP TABLE phone;
        DROP TABLE client;
        """)
        conn.commit()  # фиксируем в БД
        print ("БД удалены.")

def add_phone(number, client_id):
    with conn.cursor() as cur:
        cur.execute("""
        INSERT INTO phone(number, client_id) VALUES(%s, %s) RETURNING number, client_id;
        """,(number, client_id));
        print('Phone added:', cur.fetchall())

def update_client (first_name, last_name, email, client_id):
    # обновление данных (U из CRUD)
    with conn.cursor() as cur:
        cur.execute("""
        UPDATE client SET first_name=%s, last_name=%s, email=%s WHERE client_id=%s 
        RETURNING first_name, last_name, email, client_id;
        """, (first_name, last_name, email, client_id))
        print('Данные обновлены:', cur.fetchone())  # запрос данных автоматически зафиксирует изменения

def del_phone (number, client_id):
    # удаление данных (D из CRUD)
    with conn.cursor() as cur:
        cur.execute("""
        DELETE FROM phone WHERE number=%s and client_id=%s
        RETURNING number, client_id;
        """, (number, client_id))
        print('Данные удалены:',cur.fetchall())  # запрос данных автоматически зафиксирует изменения

def del_client(client_id):
    with conn.cursor() as cur:
        cur.execute("""
        DELETE FROM client WHERE client_id=%s
        RETURNING client_id, first_name, last_name, email;
        """, (client_id,))
        print('Данные удалены:',cur.fetchall())  # запрос данных автоматически зафиксирует изменения

def find_client (first_name=None, last_name=None, email=None, number=None):
    with conn.cursor() as cur:
        if number==None:
            cur.execute("""
            SELECT client_id, first_name, last_name, email FROM client
            WHERE first_name=%s and last_name=%s and email=%s;
            """, (first_name,last_name,email))
            print("Найден клиент:", cur.fetchall())
        if number!=None:
            cur.execute("""
            SELECT client.client_id, first_name, last_name, email FROM client
            JOIN phone ON client.client_ID = phone.client_ID
            WHERE phone.number=%s;
            """, (number,))
            print("Найден клиент:", cur.fetchall())




with psycopg2.connect(database="pythondb2", user="postgres",
              password="98199819") as conn:
    del_db()
    create_db()
    add_client('David', 'Werver', '123@.com')
    add_client('Anna', 'Sabre', '321@.com')
    add_phone(444444, 1)
    add_phone(444433, 1)
    add_phone(442222, 2)
    update_client('David', 'Werver', '124@.com', 1)
    del_phone(444433, 1)
    del_client(1)
    find_client('Anna', 'Sabre', '321@.com')
    find_client(number=442222)

conn.close()
