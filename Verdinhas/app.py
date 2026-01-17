# app.py
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import sqlite3
import hashlib
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = 'verdinha$_secret_key_2024'


# Inicializar banco de dados
def init_db():
    import random

    conn = sqlite3.connect('../verdinha.db')
    c = conn.cursor()

    # Tabela de usuários (mantém os dados)
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT NOT NULL,
                  email TEXT UNIQUE NOT NULL,
                  password TEXT NOT NULL,
                  points INTEGER DEFAULT 0,
                  level INTEGER DEFAULT 1,
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')

    # Verificar se a tabela antiga existe e deletá-la (apenas collection_points)
    c.execute("DROP TABLE IF EXISTS collection_points")

    # Criar tabela de pontos de coleta com estrutura nova
    c.execute('''CREATE TABLE collection_points
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  lat REAL NOT NULL,
                  lng REAL NOT NULL,
                  name TEXT NOT NULL,
                  collected BOOLEAN DEFAULT 0,
                  collected_by INTEGER,
                  collected_at TIMESTAMP)''')

    # Tabela de desafios
    c.execute('''CREATE TABLE IF NOT EXISTS challenges
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  title TEXT NOT NULL,
                  reward INTEGER NOT NULL,
                  active BOOLEAN DEFAULT 1)''')

    # Tabela de coletas pendentes (aguardando foto)
    c.execute('''CREATE TABLE IF NOT EXISTS pending_collections
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  user_id INTEGER NOT NULL,
                  point_id INTEGER NOT NULL,
                  point_name TEXT NOT NULL,
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                  FOREIGN KEY (user_id) REFERENCES users(id),
                  FOREIGN KEY (point_id) REFERENCES collection_points(id))''')

    # Tabela de fotos de coleta
    c.execute('''CREATE TABLE IF NOT EXISTS collection_photos
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  pending_collection_id INTEGER NOT NULL,
                  user_id INTEGER NOT NULL,
                  point_id INTEGER NOT NULL,
                  photo_data TEXT NOT NULL,
                  uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                  FOREIGN KEY (user_id) REFERENCES users(id),
                  FOREIGN KEY (point_id) REFERENCES collection_points(id))''')

    # Pool de localizações possíveis em Brasília
    all_locations = [
        # Plano Piloto
        (-15.7942, -47.8822, 'Esplanada dos Ministérios'),
        (-15.7801, -47.9292, 'Parque da Cidade'),
        (-15.7989, -47.8919, 'Torre de TV'),
        (-15.7795, -47.8902, 'Eixo Monumental'),
        (-15.8097, -47.8953, 'Setor Comercial Sul'),
        (-15.7688, -47.8717, 'Setor de Embaixadas'),

        # Regiões Administrativas
        (-15.8331, -47.9194, 'Taguatinga Centro'),
        (-15.8152, -47.8919, 'Guará I'),
        (-15.8897, -48.0443, 'Ceilândia Norte'),
        (-15.8439, -47.9197, 'Águas Claras'),
        (-15.9403, -48.1353, 'Samambaia Sul'),
        (-15.8467, -47.8039, 'Gama Centro'),

        # Áreas Residenciais
        (-15.7217, -47.8775, 'Lago Norte'),
        (-15.8439, -47.9361, 'Lago Sul'),
        (-15.7556, -47.9769, 'Cruzeiro Novo'),
        (-15.7886, -47.9308, 'Park Way'),

        # Comércio e Serviços
        (-15.8367, -47.9231, 'Taguatinga Shopping'),
        (-15.8897, -48.0289, 'Ceilândia Centro'),
        (-15.8178, -47.8872, 'Shopping Conjunto Nacional'),
        (-15.7944, -47.8825, 'Congresso Nacional'),

        # Áreas Verdes
        (-15.7331, -47.8161, 'Jardim Botânico'),
        (-15.8947, -47.8203, 'Parque Nacional'),
        (-15.7525, -47.8736, 'Parque Burle Marx'),
        (-15.8269, -47.9344, 'Parque Saburo Onoyama')
    ]

    # Selecionar 6 localizações aleatórias
    selected_points = random.sample(all_locations, 6)

    c.executemany('INSERT INTO collection_points (lat, lng, name) VALUES (?, ?, ?)', selected_points)

    print("\n" + "=" * 60)
    print("🌱 VERDINHA$ - APP SUSTENTÁVEL")
    print("=" * 60)
    print("\n✅ Novos pontos de coleta gerados:")
    for i, point in enumerate(selected_points, 1):
        print(f"   {i}. 📍 {point[2]}")
    print("\n" + "=" * 60)

    # Inserir desafios iniciais se não existirem
    c.execute('SELECT COUNT(*) FROM challenges')
    if c.fetchone()[0] == 0:
        challenges = [
            ('Colete 5 pontos de reciclagem', 50),
            ('Compartilhe sua conquista', 20),
            ('Complete sua primeira coleta', 30)
        ]
        c.executemany('INSERT INTO challenges (title, reward) VALUES (?, ?)', challenges)

    conn.commit()
    conn.close()

    print("🌱 Verdinha$ iniciado com sucesso!\n")


# Rota principal
@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('map_view'))
    return render_template('welcome.html')


# Rota de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = hashlib.sha256(request.form['password'].encode()).hexdigest()

        conn = sqlite3.connect('../verdinha.db')
        c = conn.cursor()
        c.execute('SELECT * FROM users WHERE email = ? AND password = ?', (email, password))
        user = c.fetchone()
        conn.close()

        if user:
            session['user_id'] = user[0]
            session['user_name'] = user[1]
            return redirect(url_for('map_view'))
        else:
            return render_template('login.html', error='Email ou senha incorretos')

    return render_template('login.html')


# Rota de cadastro
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = hashlib.sha256(request.form['password'].encode()).hexdigest()

        conn = sqlite3.connect('../verdinha.db')
        c = conn.cursor()

        try:
            c.execute('INSERT INTO users (name, email, password) VALUES (?, ?, ?)',
                      (name, email, password))
            conn.commit()
            user_id = c.lastrowid
            session['user_id'] = user_id
            session['user_name'] = name
            conn.close()
            return redirect(url_for('map_view'))
        except sqlite3.IntegrityError:
            conn.close()
            return render_template('register.html', error='Email já cadastrado')

    return render_template('register.html')


# Rota do mapa
@app.route('/map')
def map_view():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = sqlite3.connect('../verdinha.db')
    c = conn.cursor()

    # Buscar dados do usuário
    c.execute('SELECT points, level FROM users WHERE id = ?', (session['user_id'],))
    user_data = c.fetchone()

    # Verificar se o usuário existe
    if user_data is None:
        # Usuário foi deletado, limpar sessão e redirecionar
        session.clear()
        conn.close()
        return redirect(url_for('login'))

    # Buscar pontos de coleta disponíveis
    c.execute('SELECT id, lat, lng, name FROM collection_points WHERE collected = 0')
    points = c.fetchall()

    # Buscar desafios ativos
    c.execute('SELECT title, reward FROM challenges WHERE active = 1')
    challenges = c.fetchall()

    # Buscar coleta pendente (aguardando foto)
    c.execute(
        'SELECT id, point_id, point_name FROM pending_collections WHERE user_id = ? ORDER BY created_at DESC LIMIT 1',
        (session['user_id'],))
    pending = c.fetchone()

    conn.close()

    return render_template('map.html',
                           user_points=user_data[0],
                           user_level=user_data[1],
                           points=points,
                           challenges=challenges,
                           pending=pending)


# Rota de ranking
@app.route('/ranking')
def ranking():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = sqlite3.connect('../verdinha.db')
    c = conn.cursor()

    c.execute('SELECT name, points FROM users ORDER BY points DESC LIMIT 10')
    ranking_data = c.fetchall()

    c.execute('SELECT points FROM users WHERE id = ?', (session['user_id'],))
    user_result = c.fetchone()

    # Verificar se o usuário existe
    if user_result is None:
        session.clear()
        conn.close()
        return redirect(url_for('login'))

    user_points = user_result[0]

    conn.close()

    return render_template('ranking.html',
                           ranking=ranking_data,
                           user_points=user_points)


# Rota de recompensas
@app.route('/rewards')
def rewards():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = sqlite3.connect('../verdinha.db')
    c = conn.cursor()
    c.execute('SELECT points FROM users WHERE id = ?', (session['user_id'],))
    user_result = c.fetchone()

    # Verificar se o usuário existe
    if user_result is None:
        session.clear()
        conn.close()
        return redirect(url_for('login'))

    user_points = user_result[0]
    conn.close()

    cashback = user_points * 0.1

    return render_template('rewards.html',
                           cashback=cashback,
                           user_points=user_points)


# API para iniciar coleta (criar pendente)
@app.route('/api/collect/<int:point_id>', methods=['POST'])
def collect_point(point_id):
    if 'user_id' not in session:
        return jsonify({'error': 'Não autenticado'}), 401

    conn = sqlite3.connect('../verdinha.db')
    c = conn.cursor()

    # Verificar se o ponto existe e não foi coletado
    c.execute('SELECT id, name FROM collection_points WHERE id = ? AND collected = 0', (point_id,))
    point = c.fetchone()

    if not point:
        conn.close()
        return jsonify({'error': 'Ponto inválido ou já coletado'}), 400

    # Verificar se já existe coleta pendente para este usuário
    c.execute('SELECT id FROM pending_collections WHERE user_id = ?', (session['user_id'],))
    if c.fetchone():
        conn.close()
        return jsonify({'error': 'Você já tem uma coleta pendente. Envie a foto primeiro!'}), 400

    # Criar coleta pendente
    c.execute('INSERT INTO pending_collections (user_id, point_id, point_name) VALUES (?, ?, ?)',
              (session['user_id'], point_id, point[1]))

    conn.commit()
    conn.close()

    return jsonify({
        'success': True,
        'message': 'Coleta iniciada! Agora envie a foto do descarte.',
        'point_name': point[1],
        'pending_id': point_id
    })


# API para confirmar coleta com foto
@app.route('/api/confirm_collection', methods=['POST'])
def confirm_collection():
    if 'user_id' not in session:
        return jsonify({'error': 'Não autenticado'}), 401

    # Receber dados da foto (base64)
    photo_data = request.json.get('photo')

    if not photo_data:
        return jsonify({'error': 'Foto não fornecida'}), 400

    conn = sqlite3.connect('../verdinha.db')
    c = conn.cursor()

    # Buscar coleta pendente
    c.execute(
        'SELECT id, point_id, point_name FROM pending_collections WHERE user_id = ? ORDER BY created_at DESC LIMIT 1',
        (session['user_id'],))
    pending = c.fetchone()

    if not pending:
        conn.close()
        return jsonify({'error': 'Nenhuma coleta pendente encontrada'}), 400

    pending_id, point_id, point_name = pending

    # Salvar foto
    c.execute(
        'INSERT INTO collection_photos (pending_collection_id, user_id, point_id, photo_data) VALUES (?, ?, ?, ?)',
        (pending_id, session['user_id'], point_id, photo_data))

    # Marcar ponto como coletado
    c.execute('UPDATE collection_points SET collected = 1, collected_by = ?, collected_at = ? WHERE id = ?',
              (session['user_id'], datetime.now(), point_id))

    # Adicionar pontos ao usuário
    c.execute('UPDATE users SET points = points + 10 WHERE id = ?', (session['user_id'],))

    # Atualizar nível
    c.execute('SELECT points FROM users WHERE id = ?', (session['user_id'],))
    points = c.fetchone()[0]
    level = points // 50 + 1
    c.execute('UPDATE users SET level = ? WHERE id = ?', (level, session['user_id'],))

    # Remover da lista de pendentes
    c.execute('DELETE FROM pending_collections WHERE id = ?', (pending_id,))

    conn.commit()
    conn.close()

    return jsonify({
        'success': True,
        'points': points,
        'level': level,
        'message': f'Coleta confirmada em {point_name}!'
    })


# Rota de logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


if __name__ == '__main__':
    init_db()
    app.run(debug=True)