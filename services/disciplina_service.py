from flask import jsonify
from models.db import db
from models.disciplina import Disciplina
from models.escola import Escola


def disciplina_para_dict(disciplina):
    return {
        "id": disciplina.id,
        "escola_id": disciplina.escola_id,
        "nome": disciplina.nome,
        "ativo": disciplina.ativo
    }


def listar_disciplinas():
    disciplinas = db.session.query(Disciplina).all()

    return jsonify([
        disciplina_para_dict(d)
        for d in disciplinas
    ])


def buscar_disciplina(id):
    disciplina = db.session.get(Disciplina, id)

    if not disciplina:
        return jsonify({"erro": "Disciplina não encontrada"}), 404

    return jsonify(disciplina_para_dict(disciplina))


def criar_disciplina(dados):

    escola = db.session.query(Escola).first()

    if escola is None:
        return jsonify({
            "erro": "Cadastre uma escola antes de cadastrar disciplinas."
        }), 400

    disciplina = Disciplina(
        escola_id=escola.id,
        nome=dados["nome"],
        ativo=dados.get("ativo", True)
    )

    db.session.add(disciplina)
    db.session.commit()

    return jsonify({
        "mensagem": "Disciplina criada com sucesso!"
    }), 201


def atualizar_disciplina(id, dados):

    disciplina = db.session.get(Disciplina, id)

    if not disciplina:
        return jsonify({"erro": "Disciplina não encontrada"}), 404

    disciplina.nome = dados.get("nome", disciplina.nome)
    disciplina.ativo = dados.get("ativo", disciplina.ativo)

    db.session.commit()

    return jsonify({
        "mensagem": "Disciplina atualizada com sucesso!"
    })


def deletar_disciplina(id):

    disciplina = db.session.get(Disciplina, id)

    if not disciplina:
        return jsonify({"erro": "Disciplina não encontrada"}), 404

    db.session.delete(disciplina)
    db.session.commit()

    return jsonify({
        "mensagem": "Disciplina deletada com sucesso!"
    })

def alternar_status_disciplina(id):
    disciplina = db.session.get(Disciplina, id)

    if not disciplina:
        return jsonify({"erro": "Disciplina não encontrada"}), 404

    disciplina.ativo = not disciplina.ativo

    db.session.commit()

    return jsonify({
        "mensagem": "Status da disciplina atualizado com sucesso!",
        "ativo": disciplina.ativo
    })