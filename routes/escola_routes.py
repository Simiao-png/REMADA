from flask import Blueprint, request

from services.escola_service import (
    listar_escolas,
    buscar_escola,
    criar_escola,
    atualizar_escola,
    deletar_escola
)

escola_bp = Blueprint("escola", __name__)


@escola_bp.route("/escolas", methods=["GET"])
def listar():
    return listar_escolas()


@escola_bp.route("/escolas/<int:id>", methods=["GET"])
def buscar(id):
    return buscar_escola(id)


@escola_bp.route("/escolas", methods=["POST"])
def criar():
    return criar_escola(request.get_json())


@escola_bp.route("/escolas/<int:id>", methods=["PUT"])
def atualizar(id):
    return atualizar_escola(id, request.get_json())


@escola_bp.route("/escolas/<int:id>", methods=["DELETE"])
def deletar(id):
    return deletar_escola(id)