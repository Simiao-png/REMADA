from flask import Blueprint, request

from services.configuracao_horaria_service import (
    listar_configuracoes,
    buscar_configuracao,
    criar_configuracao,
    atualizar_configuracao,
    salvar_parametros,
    deletar_configuracao
)

configuracao_horaria_bp = Blueprint("configuracao_horaria", __name__)


@configuracao_horaria_bp.route("/configuracoes-horarias", methods=["GET"])
def listar():
    return listar_configuracoes()


@configuracao_horaria_bp.route("/configuracoes-horarias/<int:id>", methods=["GET"])
def buscar(id):
    return buscar_configuracao(id)


@configuracao_horaria_bp.route("/configuracoes-horarias", methods=["POST"])
def criar():
    return criar_configuracao(request.get_json())


@configuracao_horaria_bp.route("/configuracoes-horarias/parametros", methods=["POST"])
def salvar():
    return salvar_parametros(request.get_json())


@configuracao_horaria_bp.route("/configuracoes-horarias/<int:id>", methods=["PUT"])
def atualizar(id):
    return atualizar_configuracao(id, request.get_json())


@configuracao_horaria_bp.route("/configuracoes-horarias/<int:id>", methods=["DELETE"])
def deletar(id):
    return deletar_configuracao(id)