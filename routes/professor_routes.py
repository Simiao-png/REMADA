from flask import Blueprint
from models.db import db
from models.professor import Professor

professor_bp = Blueprint("professor", __name__)


@professor_bp.route("/professores")
def listar_professores():
    lista = Professor.query.all()
    return f"Total de professores: {len(lista)}"


@professor_bp.route("/criar-professor")
def criar_professor():
    professor = Professor(
        escola_id=1,
        nome="Professor Teste",
        email="teste@escola.com"
    )

    db.session.add(professor)
    db.session.commit()

    return "Professor criado com sucesso!"