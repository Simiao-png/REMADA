from flask import Blueprint, request

from services.turma_service import (
    listar_turmas,
    buscar_turma,
    criar_turma,
    atualizar_turma,
    deletar_turma
)

turma_bp = Blueprint("turma", __name__)


@turma_bp.route("/turmas", methods=["GET"])
def listar():
    return listar_turmas()


@turma_bp.route("/turmas/<int:id>", methods=["GET"])
def buscar(id):
    return buscar_turma(id)


@turma_bp.route("/turmas", methods=["POST"])
def criar():
    return criar_turma(request.get_json())


@turma_bp.route("/turmas/<int:id>", methods=["PUT"])
def atualizar(id):
    return atualizar_turma(id, request.get_json())


@turma_bp.route("/turmas/<int:id>", methods=["DELETE"])
def deletar(id):
    return deletar_turma(id)