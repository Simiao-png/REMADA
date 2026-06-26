from flask import Blueprint, request

from services.disciplina_service import (
    listar_disciplinas,
    buscar_disciplina,
    criar_disciplina,
    atualizar_disciplina,
    deletar_disciplina
)

disciplina_bp = Blueprint("disciplina", __name__)


@disciplina_bp.route("/disciplinas", methods=["GET"])
def listar():
    return listar_disciplinas()


@disciplina_bp.route("/disciplinas/<int:id>", methods=["GET"])
def buscar(id):
    return buscar_disciplina(id)


@disciplina_bp.route("/disciplinas", methods=["POST"])
def criar():
    return criar_disciplina(request.get_json())


@disciplina_bp.route("/disciplinas/<int:id>", methods=["PUT"])
def atualizar(id):
    return atualizar_disciplina(id, request.get_json())


@disciplina_bp.route("/disciplinas/<int:id>", methods=["DELETE"])
def deletar(id):
    return deletar_disciplina(id)