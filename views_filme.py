from flask import render_template, request, redirect, session, flash, url_for, send_from_directory, Response
from main import app, db
from models import filmes
from helpers import recupera_imagem, deleta_arquivo, Formulariofilme
import time
import json


@app.route('/')
def index():
    lista = filmes.query.order_by(filmes.id)
    return render_template('lista.html', titulo='Lista de Filmes', filmes=lista)

@app.route('/novo')
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('novo')))
    form = Formulariofilme()
    return render_template('novo.html', titulo='Novo filme', form=form)

@app.route('/criar', methods=['POST',])
def criar():
    form = Formulariofilme(request.form)

    if not form.validate_on_submit():
        return redirect(url_for('novo'))

    nome = form.nome.data
    categoria = form.categoria.data
    avaliacao = form.avaliacao.data

    filme = filmes.query.filter_by(nome=nome).first()

    if filme:
        flash('filme já existente!')
        return redirect(url_for('index'))

    novo_filme = filmes(nome=nome, categoria=categoria, avaliacao=avaliacao)
    db.session.add(novo_filme)
    db.session.commit()

    arquivo = request.files['arquivo']
    upload_path = app.config['UPLOAD_PATH']
    timestamp = time.time()
    arquivo.save(f'{upload_path}/capa{novo_filme.id}-{timestamp}.jpg')

    return redirect(url_for('index'))

@app.route('/editar/<int:id>')
def editar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('editar', id=id)))
    filme = filmes.query.filter_by(id=id).first()
    form = Formulariofilme()
    form.nome.data = filme.nome
    form.categoria.data = filme.categoria
    form.avaliacao.data = filme.avaliacao
    capa_filme = recupera_imagem(id)
    return render_template('editar.html', titulo='Editando filme', id=id, capa_filme=capa_filme, form=form)

@app.route('/atualizar', methods=['POST',])
def atualizar():
    form = Formulariofilme(request.form)

    if form.validate_on_submit():
        filme = filmes.query.filter_by(id=request.form['id']).first()
        filme.nome = form.nome.data
        filme.categoria = form.categoria.data
        filme.avaliacao = form.avaliacao.data

        db.session.add(filme)
        db.session.commit()

        arquivo = request.files['arquivo']
        upload_path = app.config['UPLOAD_PATH']
        timestamp = time.time()
        deleta_arquivo(id)
        arquivo.save(f'{upload_path}/capa{filme.id}-{timestamp}.jpg')

    return redirect(url_for('index'))

@app.route('/deletar/<int:id>')
def deletar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login'))

    filmes.query.filter_by(id=id).delete()
    db.session.commit()
    flash('filme deletado com sucesso!')

    return redirect(url_for('index'))

@app.route('/uploads/<nome_arquivo>')
def imagem(nome_arquivo):
    return send_from_directory('uploads', nome_arquivo)




## API ##

# Resposta
def gera_response(status, nome_do_conteudo, conteudo, mensagem=False):
    body = {}
    body[nome_do_conteudo] = conteudo

    if(mensagem):
        body["mensagem"] = mensagem
    return Response(json.dumps(body), status=status, mimetype='application/json')


# GETALL
@app.route('/api', methods = ['GET'])
def api():
    filmes_obj = filmes.query.order_by(filmes.id)
    filmes_json = [filme.to_json() for filme in filmes_obj]
    print(filmes_json)
    return gera_response(200,"filmes", filmes_json)
    #return Response(json.dumps(filmes_json))

# GET
@app.route('/api/<id>', methods = ['GET'])
def select_filme(id):
    filmes_obj = filmes.query.filter_by(id=id).first()
    filmes_json = filmes_obj.to_json()
    return gera_response(200,"filmes", filmes_json)


# POST
@app.route('/api', methods = ['POST'])
def cadastrar_filme():
    body = request.get_json()

    try:
        filme = filmes(nome=body['nome'], categoria=body['categoria'], avaliacao=body['avaliacao'])
        db.session.add(filme)
        db.session.commit()
        return gera_response(201,"filmes", filme.to_json(), "Criado com sucesso")
    except Exception as erro:
        print(erro)
        return gera_response(400,'Filme', {}, "Erro no cadastro")




# PUT
@app.route('/api/<id>', methods = ['PUT'])
def editar_filme(id):
    filmes_obj = filmes.query.filter_by(id=id).first()
    body = request.get_json()

    try:
        if ('nome' in body):
            filmes_obj.nome = body['nome']
        if ('categoria' in body):
            filmes_obj.categoria = body['categoria']
        if ('avaliacao' in body):
            filmes_obj.avaliacao = body['avaliacao']
        db.session.add(filmes_obj)
        db.session.commit()
        return gera_response(200,"filmes", filmes_obj.to_json(), "Atualizado com sucesso")
    except Exception as erro:
        print(erro)
        return gera_response(400,'filmes', {}, "Erro no atualizar")


# DELETE
@app.route('/api/<id>', methods = ['DELETE'])
def deleta_filme (id):
    filmes_obj = filmes.query.filter_by(id=id).first()
    try:
        db.session.delete(filmes_obj)
        db.session.commit()
        return gera_response(200,"filmes", filmes_obj.to_json(), "Filme deletado")
    except Exception as erro:
        print(erro)
        return gera_response(400,'filmes', {}, "Erro no deletar")
