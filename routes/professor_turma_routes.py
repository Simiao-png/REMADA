from flask import Blueprint, request

from services.professor_turma_service import (
    listar_professor_turmas,
    buscar_professor_turma,
    criar_professor_turma,
    deletar_professor_turma
)

professor_turma_bp = Blueprint("professor_turma", __name__)


@professor_turma_bp.route("/professor-turmas", methods=["GET"])
def listar():
    return listar_professor_turmas()


@professor_turma_bp.route(
    "/professor-turmas/<int:professor_id>/<int:turma_id>",
    methods=["GET"]
)
def buscar(professor_id, turma_id):
    return buscar_professor_turma(professor_id, turma_id)


@professor_turma_bp.route("/professor-turmas", methods=["POST"])
def criar():
    return criar_professor_turma(request.get_json())


@professor_turma_bp.route(
    "/professor-turmas/<int:professor_id>/<int:turma_id>",
    methods=["DELETE"]
)
def deletar(professor_id, turma_id):
    return deletar_professor_turma(professor_id, turma_id)