from flask import Blueprint, request

from services.carga_horaria_service import (
    listar_cargas_horarias,
    buscar_carga_horaria,
    criar_carga_horaria,
    atualizar_carga_horaria,
    deletar_carga_horaria
)

carga_horaria_bp = Blueprint("carga_horaria", __name__)


@carga_horaria_bp.route("/cargas-horarias", methods=["GET"])
def listar():
    return listar_cargas_horarias()


@carga_horaria_bp.route("/cargas-horarias/<int:id>", methods=["GET"])
def buscar(id):
    return buscar_carga_horaria(id)


@carga_horaria_bp.route("/cargas-horarias", methods=["POST"])
def criar():
    return criar_carga_horaria(request.get_json())


@carga_horaria_bp.route("/cargas-horarias/<int:id>", methods=["PUT"])
def atualizar(id):
    return atualizar_carga_horaria(id, request.get_json())


@carga_horaria_bp.route("/cargas-horarias/<int:id>", methods=["DELETE"])
def deletar(id):
    return deletar_carga_horaria(id)