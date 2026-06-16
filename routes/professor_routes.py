from flask import Blueprint
from models.db import db
from models.professor import Professor

professor_bp = Blueprint("professor", __name__)


@professor_bp.route("/professores")
def listar_professores():
    lista = Professor.query.all()

    if not lista:
        return "Nenhum professor cadastrado."

    resposta = "<h1>Professores</h1>"

    for professor in lista:
        resposta += f"""
        <p>
            <strong>ID:</strong> {professor.id}<br>
            <strong>Nome:</strong> {professor.nome}<br>
            <strong>E-mail:</strong> {professor.email}<br>
            <strong>Telefone:</strong> {professor.telefone}<br>
            <strong>Ativo:</strong> {professor.ativo}
        </p>
        <hr>
        """

    return resposta


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