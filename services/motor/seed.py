from models.db import db

from models.professor import Professor
from models.disciplina import Disciplina
from models.turma import Turma
from models.professor_disciplina import ProfessorDisciplina
from models.professor_turma import ProfessorTurma
from models.turma_disciplina import TurmaDisciplina
from models.disponibilidade_professor import (
    DisponibilidadeProfessor
)
from models.configuracao_horaria import (
    ConfiguracaoHoraria
)


def popular_banco():
    disciplina = Disciplina.query.first()
    turma = Turma.query.first()
    professor = Professor.query.first()

    if not disciplina or not turma or not professor:
        return {
            "erro": (
                "Cadastre pelo menos 1 professor, "
                "1 turma e 1 disciplina antes de "
                "popular o motor."
            )
        }

    quantidade_aulas_dia = obter_aulas_por_dia(
        turma
    )

    criar_disponibilidades(
        professor.id,
        ["segunda", "terca", "quarta"],
        quantidade_aulas_dia
    )

    criar_vinculos_motor(
        professor.id,
        turma.id,
        disciplina.id
    )

    db.session.commit()

    return {
        "mensagem": (
            "Dados mínimos do motor criados "
            "com sucesso."
        )
    }


def popular_duas_turmas():
    disciplina = Disciplina.query.first()
    professor = Professor.query.first()
    turma_1 = Turma.query.first()

    if not disciplina or not professor:
        return {
            "erro": (
                "Cadastre pelo menos 1 professor "
                "e 1 disciplina antes de popular "
                "o motor."
            )
        }

    if not turma_1:
        return {
            "erro": (
                "Cadastre pelo menos 1 turma "
                "antes de popular o motor."
            )
        }

    turma_2 = Turma.query.filter_by(
        nome="Turma Teste 2"
    ).first()

    if not turma_2:
        turma_2 = Turma(
            escola_id=turma_1.escola_id,
            configuracao_horaria_id=(
                turma_1.configuracao_horaria_id
            ),
            nome="Turma Teste 2",
            serie="Teste",
            turno=turma_1.turno,
            segmento=turma_1.segmento
        )

        db.session.add(turma_2)
        db.session.flush()

    quantidade_aulas_dia = obter_aulas_por_dia(
        turma_1
    )

    criar_disponibilidades(
        professor.id,
        ["segunda", "terca", "quarta"],
        quantidade_aulas_dia
    )

    criar_vinculos_motor(
        professor.id,
        turma_1.id,
        disciplina.id
    )

    criar_vinculos_motor(
        professor.id,
        turma_2.id,
        disciplina.id
    )

    db.session.commit()

    return {
        "mensagem": (
            "Cenário com duas turmas criado "
            "com sucesso."
        )
    }


def obter_aulas_por_dia(turma):
    configuracao = db.session.get(
        ConfiguracaoHoraria,
        turma.configuracao_horaria_id
    )

    if not configuracao:
        return 6

    return configuracao.aulas_por_dia


def criar_disponibilidades(
    professor_id,
    dias,
    quantidade_aulas_dia
):
    for dia in dias:
        for numero_aula in range(
            1,
            quantidade_aulas_dia + 1
        ):
            disponibilidade = (
                DisponibilidadeProfessor.query
                .filter_by(
                    professor_id=professor_id,
                    dia_semana=dia,
                    numero_aula=numero_aula
                )
                .first()
            )

            if disponibilidade:
                disponibilidade.disponivel = True
                continue

            db.session.add(
                DisponibilidadeProfessor(
                    professor_id=professor_id,
                    dia_semana=dia,
                    numero_aula=numero_aula,
                    disponivel=True
                )
            )


def criar_vinculos_motor(
    professor_id,
    turma_id,
    disciplina_id
):
    professor_disciplina = (
        ProfessorDisciplina.query.filter_by(
            professor_id=professor_id,
            disciplina_id=disciplina_id
        ).first()
    )

    if not professor_disciplina:
        db.session.add(
            ProfessorDisciplina(
                professor_id=professor_id,
                disciplina_id=disciplina_id
            )
        )

    professor_turma = (
        ProfessorTurma.query.filter_by(
            professor_id=professor_id,
            turma_id=turma_id,
            disciplina_id=disciplina_id
        ).first()
    )

    if not professor_turma:
        db.session.add(
            ProfessorTurma(
                professor_id=professor_id,
                turma_id=turma_id,
                disciplina_id=disciplina_id
            )
        )

    turma_disciplina = (
        TurmaDisciplina.query.filter_by(
            turma_id=turma_id,
            disciplina_id=disciplina_id
        ).first()
    )

    if not turma_disciplina:
        db.session.add(
            TurmaDisciplina(
                turma_id=turma_id,
                disciplina_id=disciplina_id,
                aulas_por_semana=5
            )
        )