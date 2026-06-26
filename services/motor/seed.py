from models.db import db

from models.professor import Professor
from models.disciplina import Disciplina
from models.turma import Turma
from models.carga_horaria import CargaHoraria
from models.professor_disciplina import ProfessorDisciplina
from models.professor_turma import ProfessorTurma
from models.turma_disciplina import TurmaDisciplina
from models.disponibilidade_professor import DisponibilidadeProfessor


def popular_banco():

    disciplina = Disciplina.query.first()
    turma = Turma.query.first()
    professor = Professor.query.first()

    if not disciplina or not turma or not professor:
        return {
            "erro": "Cadastre pelo menos 1 professor, 1 turma e 1 disciplina antes de popular o motor."
        }

    criar_disponibilidades(professor.id, ["segunda", "terca", "quarta"])
    criar_vinculos_motor(professor.id, turma.id, disciplina.id)

    db.session.commit()

    return {
        "mensagem": "Dados mínimos do motor criados com sucesso."
    }


def popular_duas_turmas():

    disciplina = Disciplina.query.first()
    professor = Professor.query.first()

    if not disciplina or not professor:
        return {
            "erro": "Cadastre pelo menos 1 professor e 1 disciplina antes de popular o motor."
        }

    turma_1 = Turma.query.first()

    if not turma_1:
        return {
            "erro": "Cadastre pelo menos 1 turma antes de popular o motor."
        }

    turma_2 = Turma.query.filter_by(nome="Turma Teste 2").first()

    if not turma_2:
        turma_2 = Turma(
            escola_id=turma_1.escola_id,
            configuracao_horaria_id=turma_1.configuracao_horaria_id,
            nome="Turma Teste 2",
            serie="Teste",
            turno="Manhã"
        )

        db.session.add(turma_2)
        db.session.commit()

    criar_disponibilidades(professor.id, ["segunda", "terca", "quarta"])

    criar_vinculos_motor(professor.id, turma_1.id, disciplina.id)
    criar_vinculos_motor(professor.id, turma_2.id, disciplina.id)

    db.session.commit()

    return {
        "mensagem": "Cenário com duas turmas criado com sucesso."
    }


def criar_disponibilidades(professor_id, dias):

    for dia in dias:

        for numero_aula in range(1, 7):

            if not DisponibilidadeProfessor.query.filter_by(
                professor_id=professor_id,
                dia_semana=dia,
                numero_aula=numero_aula
            ).first():
                db.session.add(DisponibilidadeProfessor(
                    professor_id=professor_id,
                    dia_semana=dia,
                    numero_aula=numero_aula,
                    disponivel=True
                ))


def criar_vinculos_motor(professor_id, turma_id, disciplina_id):

    if not ProfessorDisciplina.query.filter_by(
        professor_id=professor_id,
        disciplina_id=disciplina_id
    ).first():
        db.session.add(ProfessorDisciplina(
            professor_id=professor_id,
            disciplina_id=disciplina_id
        ))

    if not ProfessorTurma.query.filter_by(
        professor_id=professor_id,
        turma_id=turma_id
    ).first():
        db.session.add(ProfessorTurma(
            professor_id=professor_id,
            turma_id=turma_id
        ))

    if not TurmaDisciplina.query.filter_by(
        turma_id=turma_id,
        disciplina_id=disciplina_id
    ).first():
        db.session.add(TurmaDisciplina(
            turma_id=turma_id,
            disciplina_id=disciplina_id
        ))

    if not CargaHoraria.query.filter_by(
        turma_id=turma_id,
        disciplina_id=disciplina_id
    ).first():
        db.session.add(CargaHoraria(
            turma_id=turma_id,
            disciplina_id=disciplina_id,
            quantidade_aulas_semana=5
        ))  