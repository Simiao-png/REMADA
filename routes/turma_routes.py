from flask import Blueprint
from models.db import db
from models.turma import Turma
from sqlalchemy import text

turma_bp = Blueprint("turma", __name__)


@turma_bp.route("/turmas")
def listar_turmas():
    lista = Turma.query.all()
    return f"Total de turmas: {len(lista)}"


@turma_bp.route("/criar-configuracao")
def criar_configuracao():
    db.session.execute(
        text("""
            INSERT INTO configuracao_horaria (
                escola_id,
                nome,
                aulas_por_dia,
                duracao_aula_minutos,
                duracao_intervalo_minutos
            )
            VALUES (
                1,
                'Manhã - 6 aulas',
                6,
                50,
                20
            )
        """)
    )

    db.session.commit()

    return "Configuração horária criada com sucesso!"


@turma_bp.route("/criar-turma")
def criar_turma():
    turma = Turma(
        escola_id=1,
        configuracao_horaria_id=1,
        nome="6A",
        serie="6º Ano",
        turno="Manhã"
    )

    db.session.add(turma)
    db.session.commit()

    return "Turma criada com sucesso!"