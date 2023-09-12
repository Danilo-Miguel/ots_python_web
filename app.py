from flask import Flask, render_template, g,  request, session, abort, flash, redirect, url_for
from posts import posts
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'pudim'

app.config.from_object(__name__)

DATABASE = "banco.bd"

def conectar():
    return sqlite3.connect(DATABASE)

@app.before_request
def before_request():
    g.bd = conectar()    

@app.teardown_request
def teardown_request(f):
    g.bd.close()        



@app.route('/')
def exibir_entradas():
    # entradas = posts[::-1] # Mock das postagens


    sql  = "SELECT titulo, texto, data_criacao FROM posts ORDER BY id DESC"
    resultado = g.bd.execute(sql)
    entrada = []

    for titulo, texto, data_criacao in resultado.fetchall():
        entrada.append({
        "titulo":titulo,
        "texto":texto,
        "data_criacao":data_criacao
        })

    return render_template('exibir_entradas.html', entradas=entrada)

@app.route('/login', methods=["GET", "POST"])
def login():
    erro = None
    if request.method == "POST":
        if request.form['username'] == "admin" and request.form['password'] == "admin":
            session['logado'] = True
            flash("Login efetuado com sucesso!")
            return redirect(url_for('exibir_entradas'))
        erro = "Usuário ou senha inválidos"        
    return render_template('login.html', erro=erro)

@app.route('/logout')
def logout():
    session.pop('logado')
    flash('Logout efetuado com sucesso!')
    return redirect(url_for('exibir_entradas'))

@app.route('/inserir', methods=["POST"])
def inserir_entradas():
    if not session['logado']:
        abort(401)
        
    titulo = request.form.get('titulo')  
    texto = request.form.get('texto')  
    sql = "INSERT INTO posts (titulo, texto) values(?,?) "
    g.bd.execute(sql,[titulo, texto])
    g.bd.commit()
    flash("Post criado com sucesso!")
    return redirect(url_for('exibir_entradas'))

# @app.route('/posts/<int:id>')
# def exibir_entrada(id):
#     try:
#         entrada = posts[id-1]
#         return render_template('exibir_entrada.html', entrada=entrada)
#     except Exception:
#         return abort(404)