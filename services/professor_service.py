from flask import jsonify

from models.db import db
from models.professor import Professor
from models.escola import Escola
from models.professor_disciplina import ProfessorDisciplina
from models.professor_segmento import ProfessorSegmento


SEGMENTOS_VALIDOS = {
    "fundamental_i",
    "fundamental_ii",
    "ensino_medio",
    "cursinho"
}


def normalizar_segmentos(segmentos):
    if not isinstance(segmentos, list):
        return []

    segmentos_normalizados = []

    for segmento in segmentos:
        if not isinstance(segmento, str):
            continue

        segmento = segmento.strip().lower()

        if (
            segmento in SEGMENTOS_VALIDOS
            and segmento not in segmentos_normalizados
        ):
            segmentos_normalizados.append(segmento)

    return segmentos_normalizados


def normalizar_carga_horaria(valor):
    try:
        carga_horaria = int(valor)
    except (TypeError, ValueError):
        carga_horaria = 0

    if carga_horaria < 0:
        carga_horaria = 0

    return carga_horaria


def professor_para_dict(professor):
    return {
        "id": professor.id,
        "escola_id": professor.escola_id,
        "nome": professor.nome,
        "ativo": professor.ativo,
        "carga_horaria_semanal": (
            professor.carga_horaria_semanal or 0
        ),
        "trabalha_outra_escola": (
            professor.trabalha_outra_escola
        ),
        "observacoes": professor.observacoes,
        "disciplinas_ids": [
            disciplina.id
            for disciplina in professor.disciplinas
        ],
        "segmentos": [
            vinculo.segmento
            for vinculo in professor.segmentos
        ]
    }


def listar_professores():
    professores = (
        db.session.query(Professor)
        .order_by(Professor.nome)
        .all()
    )

    return jsonify([
        professor_para_dict(professor)
        for professor in professores
    ])


def buscar_professor(id):
    professor = db.session.get(Professor, id)

    if not professor:
        return jsonify({
            "erro": "Professor não encontrado"
        }), 404

    return jsonify(
        professor_para_dict(professor)
    )


def criar_professor(dados):
    escola = db.session.query(Escola).first()

    if not escola:
        return jsonify({
            "erro": "Nenhuma escola cadastrada."
        }), 400

    nome = str(
        dados.get("nome", "")
    ).strip()

    if not nome:
        return jsonify({
            "erro": "O nome do professor é obrigatório."
        }), 400

    segmentos = normalizar_segmentos(
        dados.get("segmentos", [])
    )

    if not segmentos:
        return jsonify({
            "erro": (
                "Selecione pelo menos um segmento "
                "de atuação."
            )
        }), 400

    carga_horaria_semanal = normalizar_carga_horaria(
        dados.get("carga_horaria_semanal", 0)
    )

    professor = Professor(
        escola_id=escola.id,
        nome=nome,
        ativo=dados.get("ativo", True),
        carga_horaria_semanal=carga_horaria_semanal,
        trabalha_outra_escola=dados.get(
            "trabalha_outra_escola",
            False
        ),
        observacoes=dados.get("observacoes")
    )

    try:
        db.session.add(professor)
        db.session.flush()

        disciplinas = dados.get(
            "disciplinas_ids",
            []
        )

        for disciplina_id in disciplinas:
            vinculo = ProfessorDisciplina(
                professor_id=professor.id,
                disciplina_id=disciplina_id
            )

            db.session.add(vinculo)

        for segmento in segmentos:
            vinculo_segmento = ProfessorSegmento(
                professor_id=professor.id,
                segmento=segmento
            )

            db.session.add(vinculo_segmento)

        db.session.commit()

        return jsonify({
            "mensagem": (
                "Professor criado com sucesso!"
            ),
            "professor": professor_para_dict(
                professor
            )
        }), 201

    except Exception:
        db.session.rollback()

        return jsonify({
            "erro": (
                "Não foi possível cadastrar "
                "o professor."
            )
        }), 500


def atualizar_professor(id, dados):
    professor = db.session.get(
        Professor,
        id
    )

    if not professor:
        return jsonify({
            "erro": "Professor não encontrado"
        }), 404

    nome = str(
        dados.get(
            "nome",
            professor.nome
        )
    ).strip()

    if not nome:
        return jsonify({
            "erro": (
                "O nome do professor é obrigatório."
            )
        }), 400

    segmentos = normalizar_segmentos(
        dados.get(
            "segmentos",
            [
                vinculo.segmento
                for vinculo in professor.segmentos
            ]
        )
    )

    if not segmentos:
        return jsonify({
            "erro": (
                "Selecione pelo menos um segmento "
                "de atuação."
            )
        }), 400

    carga_horaria_semanal = (
        normalizar_carga_horaria(
            dados.get(
                "carga_horaria_semanal",
                professor.carga_horaria_semanal
            )
        )
    )

    professor.nome = nome

    professor.ativo = dados.get(
        "ativo",
        professor.ativo
    )

    professor.carga_horaria_semanal = (
        carga_horaria_semanal
    )

    professor.trabalha_outra_escola = (
        dados.get(
            "trabalha_outra_escola",
            professor.trabalha_outra_escola
        )
    )

    professor.observacoes = dados.get(
        "observacoes",
        professor.observacoes
    )

    try:
        ProfessorDisciplina.query.filter_by(
            professor_id=professor.id
        ).delete(
            synchronize_session=False
        )

        disciplinas = dados.get(
            "disciplinas_ids",
            []
        )

        for disciplina_id in disciplinas:
            vinculo = ProfessorDisciplina(
                professor_id=professor.id,
                disciplina_id=disciplina_id
            )

            db.session.add(vinculo)

        ProfessorSegmento.query.filter_by(
            professor_id=professor.id
        ).delete(
            synchronize_session=False
        )

        for segmento in segmentos:
            vinculo_segmento = ProfessorSegmento(
                professor_id=professor.id,
                segmento=segmento
            )

            db.session.add(vinculo_segmento)

        db.session.commit()

        professor = db.session.get(
            Professor,
            id
        )

        return jsonify({
            "mensagem": (
                "Professor atualizado com sucesso!"
            ),
            "professor": professor_para_dict(
                professor
            )
        })

    except Exception:
        db.session.rollback()

        return jsonify({
            "erro": (
                "Não foi possível atualizar "
                "o professor."
            )
        }), 500


def deletar_professor(id):
    professor = db.session.get(
        Professor,
        id
    )

    if not professor:
        return jsonify({
            "erro": "Professor não encontrado"
        }), 404

    try:
        ProfessorDisciplina.query.filter_by(
            professor_id=professor.id
        ).delete(
            synchronize_session=False
        )

        ProfessorSegmento.query.filter_by(
            professor_id=professor.id
        ).delete(
            synchronize_session=False
        )

        db.session.delete(professor)
        db.session.commit()

        return jsonify({
            "mensagem": (
                "Professor deletado com sucesso!"
            )
        })

    except Exception:
        db.session.rollback()

        return jsonify({
            "erro": (
                "Não foi possível deletar "
                "o professor."
            )
        }), 500