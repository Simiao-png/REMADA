from flask import jsonify
from models.db import db
from models.escola import Escola


def listar_escolas():
    escolas = Escola.query.all()

    return jsonify([
        {
            "id": escola.id,
            "nome": escola.nome,
            "cidade": escola.cidade,
            "estado": escola.estado
        }
        for escola in escolas
    ])


def buscar_escola(id):
    escola = Escola.query.get(id)

    if not escola:
        return jsonify({"erro": "Escola não encontrada"}), 404

    return jsonify({
        "id": escola.id,
        "nome": escola.nome,
        "cidade": escola.cidade,
        "estado": escola.estado
    })


def criar_escola(dados):
    escola = Escola(
        nome=dados["nome"],
        cidade=dados["cidade"],
        estado=dados["estado"]
    )

    db.session.add(escola)
    db.session.commit()

    return jsonify({"mensagem": "Escola criada com sucesso!"}), 201


def atualizar_escola(id, dados):
    escola = Escola.query.get(id)

    if not escola:
        return jsonify({"erro": "Escola não encontrada"}), 404

    escola.nome = dados["nome"]
    escola.cidade = dados["cidade"]
    escola.estado = dados["estado"]

    db.session.commit()

    return jsonify({"mensagem": "Escola atualizada com sucesso!"})


def deletar_escola(id):
    escola = Escola.query.get(id)

    if not escola:
        return jsonify({"erro": "Escola não encontrada"}), 404

    db.session.delete(escola)
    db.session.commit()

    return jsonify({"mensagem": "Escola deletada com sucesso!"})