from flask import Blueprint, request, render_template
from models.professor import Professor
from models.disciplina import Disciplina
from services.professor_service import (
    listar_professores,
    buscar_professor,
    criar_professor,
    atualizar_professor,
    deletar_professor
)

professor_bp = Blueprint("professor", __name__)


@professor_bp.route("/professores/tela", methods=["GET"])
def tela_professores():
    professores = Professor.query.order_by(Professor.nome).all()
    disciplinas = Disciplina.query.order_by(Disciplina.nome).all()

    return render_template(
        "professores.html",
        professores=professores,
        disciplinas=disciplinas
    )


@professor_bp.route("/professores", methods=["GET"])
def listar():
    return listar_professores()


@professor_bp.route("/professores/<int:id>", methods=["GET"])
def buscar(id):
    return buscar_professor(id)


@professor_bp.route("/professores", methods=["POST"])
def criar():
    return criar_professor(request.get_json())


@professor_bp.route("/professores/<int:id>", methods=["PUT"])
def atualizar(id):
    return atualizar_professor(id, request.get_json())


@professor_bp.route("/professores/<int:id>", methods=["DELETE"])
def deletar(id):
    return deletar_professor(id)