from flask import Blueprint
from models.db import db
from models.escola import Escola

escola_bp = Blueprint("escola", __name__)


@escola_bp.route("/escolas")
def listar_escolas():
    lista = Escola.query.all()

    if not lista:
        return "Nenhuma escola cadastrada."

    resposta = "<h1>Escolas</h1>"

    for escola in lista:
        resposta += f"""
        <p>
            <strong>ID:</strong> {escola.id}<br>
            <strong>Nome:</strong> {escola.nome}<br>
            <strong>Cidade:</strong> {escola.cidade}<br>
            <strong>Estado:</strong> {escola.estado}
        </p>
        <hr>
        """

    return resposta


@escola_bp.route("/criar-escola")
def criar_escola():
    escola = Escola(
        nome="Escola Teste",
        cidade="São Paulo",
        estado="SP"
    )

    db.session.add(escola)
    db.session.commit()

    return "Escola criada com sucesso!"