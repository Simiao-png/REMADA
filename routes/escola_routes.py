from flask import Blueprint, request, jsonify
from models.db import db
from models.escola import Escola

escola_bp = Blueprint("escola", __name__)


@escola_bp.route("/escolas", methods=["GET"])
def listar_escolas():
    escolas = Escola.query.all()

    resultado = []

    for escola in escolas:
        resultado.append({
            "id": escola.id,
            "nome": escola.nome,
            "cidade": escola.cidade,
            "estado": escola.estado
        })

    return jsonify(resultado)


@escola_bp.route("/escolas/<int:id>", methods=["GET"])
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


@escola_bp.route("/escolas", methods=["POST"])
def criar_escola():
    dados = request.get_json()

    nova_escola = Escola(
        nome=dados["nome"],
        cidade=dados["cidade"],
        estado=dados["estado"]
    )

    db.session.add(nova_escola)
    db.session.commit()

    return jsonify({"mensagem": "Escola criada com sucesso!"}), 201


@escola_bp.route("/escolas/<int:id>", methods=["PUT"])
def atualizar_escola(id):
    escola = Escola.query.get(id)

    if not escola:
        return jsonify({"erro": "Escola não encontrada"}), 404

    dados = request.get_json()

    escola.nome = dados["nome"]
    escola.cidade = dados["cidade"]
    escola.estado = dados["estado"]

    db.session.commit()

    return jsonify({"mensagem": "Escola atualizada com sucesso!"})


@escola_bp.route("/escolas/<int:id>", methods=["DELETE"])
def deletar_escola(id):
    escola = Escola.query.get(id)

    if not escola:
        return jsonify({"erro": "Escola não encontrada"}), 404

    db.session.delete(escola)
    db.session.commit()

    return jsonify({"mensagem": "Escola deletada com sucesso!"})