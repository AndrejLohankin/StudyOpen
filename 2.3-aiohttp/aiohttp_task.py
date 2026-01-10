from aiohttp import web
import sqlite3
import hashlib
import secrets
import re
import json

DB_NAME = 'ads.db'

HTML_TEMPLATE = '''<!DOCTYPE html>
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
        <li><code>PUT /ads/&lt;id&gt;</code> - обновление объявления (требует токен владельца)</li>
        <li><code>DELETE /ads/&lt;id&gt;</code> - удаление объявления (требует токен владельца)</li>
    </ul>
</body>
</html>'''

routes = web.RouteTableDef()

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

def get_user_id_from_token(token):
    if token and token.startswith("dummy_token_"):
        try:
            return int(token.split("_")[-1])
        except ValueError:
            pass
    return None

async def read_json(request):
    try:
        data = await request.json()
        return data
    except Exception:
        raise web.HTTPBadRequest(text=json.dumps({'error': 'Invalid JSON'}), content_type='application/json')

@routes.get('/')
async def home(request):
    return web.Response(text=HTML_TEMPLATE, content_type='text/html')

@routes.post('/register')
async def register(request):
    data = await read_json(request)
    email = data.get('email')
    password = data.get('password')

    if not email or not password or not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        raise web.HTTPBadRequest(text=json.dumps({'error': 'Invalid input'}), content_type='application/json')

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
        return web.json_response({'id': user_id}, status=201)
    except sqlite3.IntegrityError:
        conn.close()
        raise web.HTTPBadRequest(text=json.dumps({'error': 'Email already exists'}), content_type='application/json')

@routes.post('/login')
async def login(request):
    data = await read_json(request)
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        raise web.HTTPBadRequest(text=json.dumps({'error': 'Invalid input'}), content_type='application/json')

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT id, password_hash, salt FROM users WHERE email = ?', (email,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        raise web.HTTPUnauthorized(text=json.dumps({'error': 'Invalid credentials'}), content_type='application/json')

    user_id, stored_hash, salt = row
    if hash_password(password, salt).hex() != stored_hash:
        raise web.HTTPUnauthorized(text=json.dumps({'error': 'Invalid credentials'}), content_type='application/json')

    return web.json_response({'token': f"dummy_token_{user_id}"})

@routes.post('/ads')
async def create_ad(request):
    auth_header = request.headers.get('Authorization')
    user_id = get_user_id_from_token(auth_header)
    if not user_id:
        raise web.HTTPUnauthorized(text=json.dumps({'error': 'Unauthorized'}), content_type='application/json')

    data = await read_json(request)
    title = data.get('title')
    description = data.get('description')

    if not title or not description:
        raise web.HTTPBadRequest(text=json.dumps({'error': 'Title and description required'}), content_type='application/json')

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO ads (title, description, owner_id) VALUES (?, ?, ?)',
                   (title, description, user_id))
    ad_id = cursor.lastrowid
    conn.commit()
    conn.close()

    return web.json_response({'id': ad_id}, status=201)

@routes.get('/ads/{ad_id}')
async def get_ad(request):
    try:
        ad_id = int(request.match_info['ad_id'])
    except ValueError:
        raise web.HTTPBadRequest(text=json.dumps({'error': 'Invalid ad ID'}), content_type='application/json')

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, title, description, created_at, owner_id
        FROM ads WHERE id = ?
    ''', (ad_id,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        raise web.HTTPNotFound(text=json.dumps({'error': 'Ad not found'}), content_type='application/json')

    return web.json_response({
        'id': row[0],
        'title': row[1],
        'description': row[2],
        'created_at': row[3],
        'owner_id': row[4]
    })

@routes.get('/ads')
async def get_all_ads(request):
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

    return web.json_response(ads)

@routes.put('/ads/{ad_id}')
async def update_ad(request):
    try:
        ad_id = int(request.match_info['ad_id'])
    except ValueError:
        raise web.HTTPBadRequest(text=json.dumps({'error': 'Invalid ad ID'}), content_type='application/json')

    auth_header = request.headers.get('Authorization')
    user_id = get_user_id_from_token(auth_header)
    if not user_id:
        raise web.HTTPUnauthorized(text=json.dumps({'error': 'Unauthorized'}), content_type='application/json')

    data = await read_json(request)
    title = data.get('title')
    description = data.get('description')

    if not title and not description:
        raise web.HTTPBadRequest(text=json.dumps({'error': 'Title or description required'}), content_type='application/json')

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT owner_id FROM ads WHERE id = ?', (ad_id,))
    row = cursor.fetchone()

    if not row:
        conn.close()
        raise web.HTTPNotFound(text=json.dumps({'error': 'Ad not found'}), content_type='application/json')

    if row[0] != user_id:
        conn.close()
        raise web.HTTPForbidden(text=json.dumps({'error': 'Forbidden'}), content_type='application/json')

    if title:
        cursor.execute('UPDATE ads SET title = ? WHERE id = ?', (title, ad_id))
    if description:
        cursor.execute('UPDATE ads SET description = ? WHERE id = ?', (description, ad_id))

    conn.commit()
    conn.close()

    return web.json_response({'message': 'Ad updated'})

@routes.delete('/ads/{ad_id}')
async def delete_ad(request):
    try:
        ad_id = int(request.match_info['ad_id'])
    except ValueError:
        raise web.HTTPBadRequest(text=json.dumps({'error': 'Invalid ad ID'}), content_type='application/json')

    auth_header = request.headers.get('Authorization')
    user_id = get_user_id_from_token(auth_header)
    if not user_id:
        raise web.HTTPUnauthorized(text=json.dumps({'error': 'Unauthorized'}), content_type='application/json')

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT owner_id FROM ads WHERE id = ?', (ad_id,))
    row = cursor.fetchone()

    if not row:
        conn.close()
        raise web.HTTPNotFound(text=json.dumps({'error': 'Ad not found'}), content_type='application/json')

    if row[0] != user_id:
        conn.close()
        raise web.HTTPForbidden(text=json.dumps({'error': 'Forbidden'}), content_type='application/json')

    cursor.execute('DELETE FROM ads WHERE id = ?', (ad_id,))
    conn.commit()
    conn.close()

    return web.json_response({'message': 'Ad deleted'})

def main():
    init_db()
    app = web.Application()
    app.add_routes(routes)
    web.run_app(app, host='127.0.0.2', port=5000)

if __name__ == '__main__':
    main()