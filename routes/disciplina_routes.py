from flask import Blueprint
from models.db import db
from models.disciplina import Disciplina

disciplina_bp = Blueprint("disciplina", __name__)


@disciplina_bp.route("/disciplinas")
def listar_disciplinas():
    lista = Disciplina.query.all()

    if not lista:
        return "Nenhuma disciplina cadastrada."

    resposta = "<h1>Disciplinas</h1>"

    for disciplina in lista:
        resposta += f"""
        <p>
            <strong>ID:</strong> {disciplina.id}<br>
            <strong>Nome:</strong> {disciplina.nome}<br>
            <strong>Ativo:</strong> {disciplina.ativo}
        </p>
        <hr>
        """

    return resposta


@disciplina_bp.route("/criar-disciplina")
def criar_disciplina():
    disciplina = Disciplina(
        escola_id=1,
        nome="Matemática"
    )

    db.session.add(disciplina)
    db.session.commit()

    return "Disciplina criada com sucesso!"