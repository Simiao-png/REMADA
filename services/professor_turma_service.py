from flask import jsonify
from sqlalchemy.exc import IntegrityError

from models.db import db
from models.professor_turma import ProfessorTurma


def vinculo_para_dict(vinculo):
    return {
        "professor_id": vinculo.professor_id,
        "turma_id": vinculo.turma_id,
        "disciplina_id": vinculo.disciplina_id
    }


def listar_professor_turmas():
    vinculos = ProfessorTurma.query.order_by(
        ProfessorTurma.professor_id,
        ProfessorTurma.turma_id,
        ProfessorTurma.disciplina_id
    ).all()

    return jsonify([
        vinculo_para_dict(vinculo)
        for vinculo in vinculos
    ])


def buscar_professor_turma(
    professor_id,
    turma_id,
    disciplina_id
):
    vinculo = ProfessorTurma.query.get(
        (
            professor_id,
            turma_id,
            disciplina_id
        )
    )

    if not vinculo:
        return jsonify({
            "erro": "Vínculo não encontrado."
        }), 404

    return jsonify(vinculo_para_dict(vinculo))


def criar_professor_turma(dados):
    campos_obrigatorios = [
        "professor_id",
        "turma_id",
        "disciplina_id"
    ]

    for campo in campos_obrigatorios:
        if campo not in dados:
            return jsonify({
                "erro": f"O campo '{campo}' é obrigatório."
            }), 400

    professor_id = dados["professor_id"]
    turma_id = dados["turma_id"]
    disciplina_id = dados["disciplina_id"]

    vinculo_existente = ProfessorTurma.query.get(
        (
            professor_id,
            turma_id,
            disciplina_id
        )
    )

    if vinculo_existente:
        return jsonify({
            "erro": (
                "Este professor já está atribuído a essa "
                "disciplina nessa turma."
            )
        }), 409

    vinculo = ProfessorTurma(
        professor_id=professor_id,
        turma_id=turma_id,
        disciplina_id=disciplina_id
    )

    try:
        db.session.add(vinculo)
        db.session.commit()

        return jsonify({
            "mensagem": "Atribuição criada com sucesso!",
            "vinculo": vinculo_para_dict(vinculo)
        }), 201

    except IntegrityError:
        db.session.rollback()

        return jsonify({
            "erro": (
                "Não foi possível criar a atribuição. "
                "Verifique o professor, a turma e a disciplina."
            )
        }), 400


def deletar_professor_turma(
    professor_id,
    turma_id,
    disciplina_id
):
    vinculo = ProfessorTurma.query.get(
        (
            professor_id,
            turma_id,
            disciplina_id
        )
    )

    if not vinculo:
        return jsonify({
            "erro": "Vínculo não encontrado."
        }), 404

    db.session.delete(vinculo)
    db.session.commit()

    return jsonify({
        "mensagem": "Atribuição removida com sucesso!"
    })