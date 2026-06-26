from flask import Blueprint, request

from services.disponibilidade_professor_service import (
    listar_disponibilidades,
    buscar_disponibilidade,
    criar_disponibilidade,
    atualizar_disponibilidade,
    deletar_disponibilidade
)

disponibilidade_professor_bp = Blueprint("disponibilidade_professor", __name__)


@disponibilidade_professor_bp.route("/disponibilidades", methods=["GET"])
def listar():
    return listar_disponibilidades()


@disponibilidade_professor_bp.route("/disponibilidades/<int:id>", methods=["GET"])
def buscar(id):
    return buscar_disponibilidade(id)


@disponibilidade_professor_bp.route("/disponibilidades", methods=["POST"])
def criar():
    return criar_disponibilidade(request.get_json())


@disponibilidade_professor_bp.route("/disponibilidades/<int:id>", methods=["PUT"])
def atualizar(id):
    return atualizar_disponibilidade(id, request.get_json())


@disponibilidade_professor_bp.route("/disponibilidades/<int:id>", methods=["DELETE"])
def deletar(id):
    return deletar_disponibilidade(id)