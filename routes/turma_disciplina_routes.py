from flask import Blueprint, request

from services.turma_disciplina_service import (
    listar_turma_disciplinas,
    listar_matriz_da_turma,
    buscar_turma_disciplina,
    criar_turma_disciplina,
    salvar_matriz_curricular,
    deletar_turma_disciplina
)

turma_disciplina_bp = Blueprint(
    "turma_disciplina",
    __name__
)


@turma_disciplina_bp.route(
    "/turma-disciplinas",
    methods=["GET"]
)
def listar():
    return listar_turma_disciplinas()


@turma_disciplina_bp.route(
    "/turmas/<int:turma_id>/matriz-curricular",
    methods=["GET"]
)
def listar_matriz(turma_id):
    return listar_matriz_da_turma(turma_id)


@turma_disciplina_bp.route(
    "/turmas/<int:turma_id>/matriz-curricular",
    methods=["PUT"]
)
def salvar_matriz(turma_id):
    return salvar_matriz_curricular(
        turma_id,
        request.get_json() or {}
    )


@turma_disciplina_bp.route(
    "/turma-disciplinas/<int:turma_id>/<int:disciplina_id>",
    methods=["GET"]
)
def buscar(turma_id, disciplina_id):
    return buscar_turma_disciplina(
        turma_id,
        disciplina_id
    )


@turma_disciplina_bp.route(
    "/turma-disciplinas",
    methods=["POST"]
)
def criar():
    return criar_turma_disciplina(
        request.get_json() or {}
    )


@turma_disciplina_bp.route(
    "/turma-disciplinas/<int:turma_id>/<int:disciplina_id>",
    methods=["DELETE"]
)
def deletar(turma_id, disciplina_id):
    return deletar_turma_disciplina(
        turma_id,
        disciplina_id
    )