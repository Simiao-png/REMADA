from flask import jsonify
from models.db import db
from models.disciplina import Disciplina


def disciplina_para_dict(disciplina):
    return {
        "id": disciplina.id,
        "escola_id": disciplina.escola_id,
        "nome": disciplina.nome,
        "ativo": disciplina.ativo
    }


def listar_disciplinas():
    disciplinas = Disciplina.query.all()
    return jsonify([disciplina_para_dict(disciplina) for disciplina in disciplinas])


def buscar_disciplina(id):
    disciplina = Disciplina.query.get(id)

    if not disciplina:
        return jsonify({"erro": "Disciplina não encontrada"}), 404

    return jsonify(disciplina_para_dict(disciplina))


def criar_disciplina(dados):
    disciplina = Disciplina(
        escola_id=dados["escola_id"],
        nome=dados["nome"],
        ativo=dados.get("ativo", True)
    )

    db.session.add(disciplina)
    db.session.commit()

    return jsonify({"mensagem": "Disciplina criada com sucesso!"}), 201


def atualizar_disciplina(id, dados):
    disciplina = Disciplina.query.get(id)

    if not disciplina:
        return jsonify({"erro": "Disciplina não encontrada"}), 404

    disciplina.escola_id = dados.get("escola_id", disciplina.escola_id)
    disciplina.nome = dados.get("nome", disciplina.nome)
    disciplina.ativo = dados.get("ativo", disciplina.ativo)

    db.session.commit()

    return jsonify({"mensagem": "Disciplina atualizada com sucesso!"})


def deletar_disciplina(id):
    disciplina = Disciplina.query.get(id)

    if not disciplina:
        return jsonify({"erro": "Disciplina não encontrada"}), 404

    db.session.delete(disciplina)
    db.session.commit()

    return jsonify({"mensagem": "Disciplina deletada com sucesso!"})