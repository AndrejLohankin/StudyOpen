from flask import Flask, request, jsonify, render_template_string
import sqlite3
import hashlib
import secrets
import re

app = Flask(__name__)
DB_NAME = 'ads.db'

# --- Страница приветствия ---
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>API для объявлений</title>
</head>
<body>
    <h1>Добро пожаловать в API для объявлений!</h1>
    <p>Доступные эндпоинты:</p>
    <ul>
        <li><code>POST /register</code> - регистрация пользователя</li>
        <li><code>POST /login</code> - вход и получение токена</li>
        <li><code>POST /ads</code> - создание объявления (требует токен)</li>
        <li><code>GET /ads/&lt;id&gt;</code> - получение объявления</li>
        <li><code>GET /ads</code> - получение всех объявлений</li>
        <li><code>DELETE /ads/&lt;id&gt;</code> - удаление объявления (требует токен владельца)</li>
    </ul>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            salt TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            owner_id INTEGER NOT NULL,
            FOREIGN KEY (owner_id) REFERENCES users (id)
        )
    ''')
    conn.commit()
    conn.close()

def hash_password(password, salt):
    return hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)

def generate_salt():
    return secrets.token_hex(16)

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not email or not password or not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return jsonify({'error': 'Invalid input'}), 400

    salt = generate_salt()
    password_hash = hash_password(password, salt)

    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (email, password_hash, salt) VALUES (?, ?, ?)',
                       (email, password_hash.hex(), salt))
        conn.commit()
        user_id = cursor.lastrowid
        conn.close()
        return jsonify({'id': user_id}), 201
    except sqlite3.IntegrityError:
        return jsonify({'error': 'Email already exists'}), 400

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Invalid input'}), 400

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT id, password_hash, salt FROM users WHERE email = ?', (email,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        return jsonify({'error': 'Invalid credentials'}), 401

    user_id, stored_hash, salt = row
    if hash_password(password, salt).hex() != stored_hash:
        return jsonify({'error': 'Invalid credentials'}), 401

    return jsonify({'token': f"dummy_token_{user_id}"}), 200

def get_user_id_from_token(token):
    if token and token.startswith("dummy_token_"):
        try:
            return int(token.split("_")[-1])
        except ValueError:
            pass
    return None

@app.route('/ads', methods=['POST'])
def create_ad():
    token = request.headers.get('Authorization')
    user_id = get_user_id_from_token(token)
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401

    data = request.json
    title = data.get('title')
    description = data.get('description')

    if not title or not description:
        return jsonify({'error': 'Title and description required'}), 400

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO ads (title, description, owner_id) VALUES (?, ?, ?)',
                   (title, description, user_id))
    ad_id = cursor.lastrowid
    conn.commit()
    conn.close()

    return jsonify({'id': ad_id}), 201

@app.route('/ads/<int:ad_id>', methods=['GET'])
def get_ad(ad_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, title, description, created_at, owner_id
        FROM ads WHERE id = ?
    ''', (ad_id,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        return jsonify({'error': 'Ad not found'}), 404

    return jsonify({
        'id': row[0],
        'title': row[1],
        'description': row[2],
        'created_at': row[3],
        'owner_id': row[4]
    })

@app.route('/ads', methods=['GET'])
def get_all_ads():
    import sqlite3
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, title, description, created_at, owner_id
        FROM ads
    ''')
    rows = cursor.fetchall()
    conn.close()

    ads = []
    for row in rows:
        ads.append({
            'id': row[0],
            'title': row[1],
            'description': row[2],
            'created_at': row[3],
            'owner_id': row[4]
        })

    return jsonify(ads)

@app.route('/ads/<int:ad_id>', methods=['PUT'])
def update_ad(ad_id):
    token = request.headers.get('Authorization')
    user_id = get_user_id_from_token(token)
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401

    data = request.json
    title = data.get('title')
    description = data.get('description')

    if not title and not description:
        return jsonify({'error': 'Title or description required'}), 400

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT owner_id FROM ads WHERE id = ?', (ad_id,))
    row = cursor.fetchone()

    if not row:
        conn.close()
        return jsonify({'error': 'Ad not found'}), 404

    if row[0] != user_id:
        conn.close()
        return jsonify({'error': 'Forbidden'}), 403

    if title:
        cursor.execute('UPDATE ads SET title = ? WHERE id = ?', (title, ad_id))
    if description:
        cursor.execute('UPDATE ads SET description = ? WHERE id = ?', (description, ad_id))

    conn.commit()
    conn.close()

    return jsonify({'message': 'Ad updated'})


@app.route('/ads/<int:ad_id>', methods=['DELETE'])
def delete_ad(ad_id):
    token = request.headers.get('Authorization')
    user_id = get_user_id_from_token(token)
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT owner_id FROM ads WHERE id = ?', (ad_id,))
    row = cursor.fetchone()

    if not row:
        conn.close()
        return jsonify({'error': 'Ad not found'}), 404

    if row[0] != user_id:
        conn.close()
        return jsonify({'error': 'Forbidden'}), 403

    cursor.execute('DELETE FROM ads WHERE id = ?', (ad_id,))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Ad deleted'})

if __name__ == '__main__':
    init_db()
    app.run(debug=True)