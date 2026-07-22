from flask import jsonify
from models.db import db
from models.turma import Turma
from models.disciplina import Disciplina
from models.turma_disciplina import TurmaDisciplina


def vinculo_para_dict(vinculo):
    return {
        "turma_id": vinculo.turma_id,
        "disciplina_id": vinculo.disciplina_id,
        "aulas_por_semana": vinculo.aulas_por_semana
    }


def listar_turma_disciplinas():
    vinculos = TurmaDisciplina.query.all()

    return jsonify([
        vinculo_para_dict(vinculo)
        for vinculo in vinculos
    ])


def listar_matriz_da_turma(turma_id):
    turma = Turma.query.get(turma_id)

    if not turma:
        return jsonify({"erro": "Turma não encontrada."}), 404

    vinculos = TurmaDisciplina.query.filter_by(
        turma_id=turma_id
    ).all()

    return jsonify([
        vinculo_para_dict(vinculo)
        for vinculo in vinculos
    ])


def buscar_turma_disciplina(turma_id, disciplina_id):
    vinculo = TurmaDisciplina.query.get(
        (turma_id, disciplina_id)
    )

    if not vinculo:
        return jsonify({"erro": "Vínculo não encontrado."}), 404

    return jsonify(vinculo_para_dict(vinculo))


def criar_turma_disciplina(dados):
    turma_id = dados.get("turma_id")
    disciplina_id = dados.get("disciplina_id")
    aulas_por_semana = dados.get("aulas_por_semana", 0)

    if not turma_id or not disciplina_id:
        return jsonify({
            "erro": "Turma e disciplina são obrigatórias."
        }), 400

    if not isinstance(aulas_por_semana, int) or aulas_por_semana < 0:
        return jsonify({
            "erro": "A quantidade de aulas deve ser um número inteiro positivo."
        }), 400

    turma = Turma.query.get(turma_id)
    disciplina = Disciplina.query.get(disciplina_id)

    if not turma:
        return jsonify({"erro": "Turma não encontrada."}), 404

    if not disciplina:
        return jsonify({"erro": "Disciplina não encontrada."}), 404

    vinculo = TurmaDisciplina.query.get(
        (turma_id, disciplina_id)
    )

    if vinculo:
        vinculo.aulas_por_semana = aulas_por_semana
    else:
        vinculo = TurmaDisciplina(
            turma_id=turma_id,
            disciplina_id=disciplina_id,
            aulas_por_semana=aulas_por_semana
        )

        db.session.add(vinculo)

    db.session.commit()

    return jsonify({
        "mensagem": "Vínculo salvo com sucesso!",
        "vinculo": vinculo_para_dict(vinculo)
    }), 201


def salvar_matriz_curricular(turma_id, dados):
    turma = Turma.query.get(turma_id)

    if not turma:
        return jsonify({"erro": "Turma não encontrada."}), 404

    disciplinas = dados.get("disciplinas")

    if not isinstance(disciplinas, list):
        return jsonify({
            "erro": "Envie uma lista de disciplinas."
        }), 400

    try:
        TurmaDisciplina.query.filter_by(
            turma_id=turma_id
        ).delete(synchronize_session=False)

        for item in disciplinas:
            disciplina_id = item.get("disciplina_id")
            aulas_por_semana = item.get("aulas_por_semana", 0)

            if not disciplina_id:
                raise ValueError("Disciplina inválida.")

            if (
                not isinstance(aulas_por_semana, int)
                or aulas_por_semana < 0
            ):
                raise ValueError(
                    "A quantidade de aulas deve ser um número inteiro positivo."
                )

            disciplina = Disciplina.query.get(disciplina_id)

            if not disciplina:
                raise ValueError(
                    f"Disciplina {disciplina_id} não encontrada."
                )

            if aulas_por_semana == 0:
                continue

            vinculo = TurmaDisciplina(
                turma_id=turma_id,
                disciplina_id=disciplina_id,
                aulas_por_semana=aulas_por_semana
            )

            db.session.add(vinculo)

        db.session.commit()

    except ValueError as erro:
        db.session.rollback()
        return jsonify({"erro": str(erro)}), 400

    except Exception:
        db.session.rollback()
        return jsonify({
            "erro": "Não foi possível salvar a matriz curricular."
        }), 500

    return jsonify({
        "mensagem": "Matriz curricular salva com sucesso!"
    })


def deletar_turma_disciplina(turma_id, disciplina_id):
    vinculo = TurmaDisciplina.query.get(
        (turma_id, disciplina_id)
    )

    if not vinculo:
        return jsonify({"erro": "Vínculo não encontrado."}), 404

    db.session.delete(vinculo)
    db.session.commit()

    return jsonify({
        "mensagem": "Vínculo deletado com sucesso!"
    })