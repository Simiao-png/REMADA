from flask import Blueprint, request

from services.professor_disciplina_service import (
    listar_professor_disciplinas,
    buscar_professor_disciplina,
    criar_professor_disciplina,
    atualizar_professor_disciplina,
    deletar_professor_disciplina
)

professor_disciplina_bp = Blueprint(
    "professor_disciplina",
    __name__
)


@professor_disciplina_bp.route("/professor-disciplinas", methods=["GET"])
def listar():
    return listar_professor_disciplinas()


@professor_disciplina_bp.route("/professor-disciplinas/<int:id>", methods=["GET"])
def buscar(id):
    return buscar_professor_disciplina(id)


@professor_disciplina_bp.route("/professor-disciplinas", methods=["POST"])
def criar():
    return criar_professor_disciplina(request.get_json())


@professor_disciplina_bp.route("/professor-disciplinas/<int:id>", methods=["PUT"])
def atualizar(id):
    return atualizar_professor_disciplina(
        id,
        request.get_json()
    )


@professor_disciplina_bp.route("/professor-disciplinas/<int:id>", methods=["DELETE"])
def deletar(id):
    return deletar_professor_disciplina(id)