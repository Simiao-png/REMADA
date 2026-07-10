from flask import Blueprint, render_template
from models.professor import Professor
from models.disciplina import Disciplina
from models.turma import Turma


cadastro_bp = Blueprint("cadastro", __name__)


@cadastro_bp.route("/cadastros/tela", methods=["GET"])
def tela_cadastros():
    professores = Professor.query.order_by(Professor.nome).all()
    disciplinas = Disciplina.query.order_by(Disciplina.nome).all()
    turmas = Turma.query.order_by(Turma.nome).all()

    return render_template(
        "cadastros.html",
        professores=professores,
        disciplinas=disciplinas,
        turmas=turmas
    )