from flask import Blueprint, render_template, session
from models.db import db
from models.professor import Professor
from models.disciplina import Disciplina
from models.turma import Turma
from models.escola import Escola


cadastro_bp = Blueprint("cadastro", __name__)


@cadastro_bp.route("/cadastros/tela", methods=["GET"])
def tela_cadastros():
    # 1. Pega a escola logada na sessão
    escola_id = session.get('escola_id')
    escola = None
    
    if escola_id:
        escola = db.session.query(Escola).get(escola_id)
    else:
        # Fallback para caso não haja sessão iniciada
        escola = db.session.query(Escola).order_by(Escola.id.desc()).first()
        if escola:
            escola_id = escola.id

    # 2. Busca APENAS os dados da escola logada
    if escola_id:
        professores = Professor.query.filter_by(escola_id=escola_id).order_by(Professor.nome).all()
        disciplinas = Disciplina.query.filter_by(escola_id=escola_id).order_by(Disciplina.nome).all()
        turmas = Turma.query.filter_by(escola_id=escola_id).order_by(Turma.nome).all()
    else:
        professores = []
        disciplinas = []
        turmas = []

    return render_template(
        "cadastros.html",
        escola=escola,
        professores=professores,
        disciplinas=disciplinas,
        turmas=turmas
    )