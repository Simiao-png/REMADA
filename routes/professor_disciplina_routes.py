from flask import Blueprint
from models.db import db
from models.professor_disciplina import ProfessorDisciplina

professor_disciplina_bp = Blueprint("professor_disciplina", __name__)


@professor_disciplina_bp.route("/professor-disciplinas")
def listar_professor_disciplinas():
    lista = ProfessorDisciplina.query.all()

    if not lista:
        return "Nenhum vínculo cadastrado."

    resposta = "<h1>Professor x Disciplina</h1>"

    for item in lista:
        resposta += f"""
        <p>
            Professor ID: {item.professor_id}<br>
            Disciplina ID: {item.disciplina_id}
        </p>
        <hr>
        """

    return resposta


@professor_disciplina_bp.route("/criar-professor-disciplina")
def criar_professor_disciplina():
    vinculo = ProfessorDisciplina(
        professor_id=2,
        disciplina_id=1
    )

    db.session.add(vinculo)
    db.session.commit()

    return "Vínculo criado com sucesso!"