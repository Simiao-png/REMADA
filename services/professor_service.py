from flask import jsonify, session

from models.db import db
from models.professor import Professor
from models.escola import Escola
from models.disciplina import Disciplina
from models.professor_disciplina import ProfessorDisciplina
from models.professor_segmento import ProfessorSegmento
from models.professor_turma import ProfessorTurma
from models.disponibilidade_professor import DisponibilidadeProfessor


def obter_escola_id(dados=None):
    escola_id = session.get("escola_id")

    if escola_id:
        return int(escola_id)

    if isinstance(dados, dict):
        try:
            escola_id_dados = int(
                dados.get("escola_id")
            )
        except (TypeError, ValueError):
            escola_id_dados = None

        if escola_id_dados:
            return escola_id_dados

    escola = (
        db.session.query(Escola)
        .order_by(Escola.id)
        .first()
    )

    return escola.id if escola else None


def normalizar_inteiro_positivo(
    valor,
    permitir_none=True
):
    if valor in (None, ""):
        return None if permitir_none else 0

    try:
        valor_normalizado = int(valor)
    except (TypeError, ValueError):
        return None if permitir_none else 0

    if valor_normalizado <= 0:
        return None if permitir_none else 0

    return valor_normalizado


def buscar_disciplina_da_escola(
    disciplina_id,
    escola_id
):
    disciplina_id = normalizar_inteiro_positivo(
        disciplina_id
    )

    if not disciplina_id:
        return None

    return (
        Disciplina.query
        .filter_by(
            id=disciplina_id,
            escola_id=escola_id
        )
        .first()
    )


def professor_para_dict(professor):
    limite = professor.limite_aulas_semana

    disciplina_principal = getattr(
        professor,
        "disciplina_principal",
        None
    )

    disciplina_principal_id = getattr(
        professor,
        "disciplina_principal_id",
        None
    )

    return {
        "id": professor.id,
        "escola_id": professor.escola_id,
        "nome": professor.nome,
        "ativo": professor.ativo,
        "limite_aulas_semana": limite,
        "carga_horaria_semanal": limite or 0,
        "disciplina_principal_id": disciplina_principal_id,
        "disciplina_principal": (
            {
                "id": disciplina_principal.id,
                "nome": disciplina_principal.nome,
                "cor": getattr(
                    disciplina_principal,
                    "cor",
                    None
                ),
            }
            if disciplina_principal
            else None
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
        ],
    }


def listar_professores():
    escola_id = obter_escola_id()

    query = Professor.query

    if escola_id:
        query = query.filter_by(
            escola_id=escola_id
        )

    professores = (
        query
        .order_by(Professor.nome)
        .all()
    )

    return jsonify([
        professor_para_dict(professor)
        for professor in professores
    ])


def buscar_professor(id):
    escola_id = obter_escola_id()

    query = Professor.query.filter_by(
        id=id
    )

    if escola_id:
        query = query.filter_by(
            escola_id=escola_id
        )

    professor = query.first()

    if not professor:
        return jsonify({
            "erro": "Professor não encontrado."
        }), 404

    return jsonify(
        professor_para_dict(professor)
    )


def criar_professor(dados):
    dados = dados or {}

    escola_id = obter_escola_id(
        dados
    )

    if not escola_id:
        return jsonify({
            "erro": "Nenhuma escola selecionada."
        }), 400

    escola = db.session.get(
        Escola,
        escola_id
    )

    if not escola:
        return jsonify({
            "erro": "Escola não encontrada."
        }), 404

    nome = str(
        dados.get("nome", "")
    ).strip()

    if not nome:
        return jsonify({
            "erro": (
                "O nome do professor é obrigatório."
            )
        }), 400

    disciplina_principal_id = (
        normalizar_inteiro_positivo(
            dados.get(
                "disciplina_principal_id"
            )
        )
    )

    disciplina_principal = None

    if disciplina_principal_id:
        disciplina_principal = (
            buscar_disciplina_da_escola(
                disciplina_principal_id,
                escola.id
            )
        )

        if not disciplina_principal:
            return jsonify({
                "erro": (
                    "A disciplina principal selecionada "
                    "não pertence à escola atual."
                )
            }), 400

    limite_aulas_semana = (
        normalizar_inteiro_positivo(
            dados.get(
                "limite_aulas_semana"
            )
        )
    )

    professor = Professor(
        escola_id=escola.id,
        nome=nome,
        ativo=bool(
            dados.get(
                "ativo",
                True
            )
        ),
        disciplina_principal_id=(
            disciplina_principal.id
            if disciplina_principal
            else None
        ),
        limite_aulas_semana=(
            limite_aulas_semana
        ),
        trabalha_outra_escola=bool(
            dados.get(
                "trabalha_outra_escola",
                False
            )
        ),
        observacoes=dados.get(
            "observacoes"
        ),
    )

    try:
        db.session.add(
            professor
        )

        db.session.commit()

        db.session.refresh(
            professor
        )

        return jsonify({
            "mensagem": (
                "Professor criado com sucesso!"
            ),
            "professor": professor_para_dict(
                professor
            ),
        }), 201

    except Exception as erro:
        db.session.rollback()

        print(
            "Erro ao cadastrar professor:",
            erro
        )

        return jsonify({
            "erro": (
                "Não foi possível cadastrar "
                "o professor."
            )
        }), 500


def atualizar_professor(id, dados):
    dados = dados or {}

    escola_id = obter_escola_id(
        dados
    )

    query = Professor.query.filter_by(
        id=id
    )

    if escola_id:
        query = query.filter_by(
            escola_id=escola_id
        )

    professor = query.first()

    if not professor:
        return jsonify({
            "erro": "Professor não encontrado."
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

    disciplina_principal_id = (
        normalizar_inteiro_positivo(
            dados.get(
                "disciplina_principal_id",
                professor.disciplina_principal_id
            )
        )
    )

    disciplina_principal = None

    if disciplina_principal_id:
        disciplina_principal = (
            buscar_disciplina_da_escola(
                disciplina_principal_id,
                professor.escola_id
            )
        )

        if not disciplina_principal:
            return jsonify({
                "erro": (
                    "A disciplina principal selecionada "
                    "não pertence à escola atual."
                )
            }), 400

    limite_aulas_semana = (
        normalizar_inteiro_positivo(
            dados.get(
                "limite_aulas_semana",
                professor.limite_aulas_semana
            )
        )
    )

    professor.nome = nome

    professor.ativo = bool(
        dados.get(
            "ativo",
            professor.ativo
        )
    )

    professor.disciplina_principal_id = (
        disciplina_principal.id
        if disciplina_principal
        else None
    )

    professor.limite_aulas_semana = (
        limite_aulas_semana
    )

    professor.trabalha_outra_escola = bool(
        dados.get(
            "trabalha_outra_escola",
            professor.trabalha_outra_escola,
        )
    )

    professor.observacoes = dados.get(
        "observacoes",
        professor.observacoes,
    )

    try:
        db.session.commit()

        db.session.refresh(
            professor
        )

        return jsonify({
            "mensagem": (
                "Professor atualizado com sucesso!"
            ),
            "professor": professor_para_dict(
                professor
            ),
        })

    except Exception as erro:
        db.session.rollback()

        print(
            "Erro ao atualizar professor:",
            erro
        )

        return jsonify({
            "erro": (
                "Não foi possível atualizar "
                "o professor."
            )
        }), 500


def deletar_professor(id):
    escola_id = obter_escola_id()

    query = Professor.query.filter_by(
        id=id
    )

    if escola_id:
        query = query.filter_by(
            escola_id=escola_id
        )

    professor = query.first()

    if not professor:
        return jsonify({
            "erro": "Professor não encontrado."
        }), 404

    try:
        DisponibilidadeProfessor.query.filter_by(
            professor_id=professor.id
        ).delete(
            synchronize_session=False
        )

        ProfessorTurma.query.filter_by(
            professor_id=professor.id
        ).delete(
            synchronize_session=False
        )

        # Mantidos temporariamente para limpar vínculos antigos.
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

        db.session.delete(
            professor
        )

        db.session.commit()

        return jsonify({
            "mensagem": (
                "Professor deletado com sucesso!"
            )
        })

    except Exception as erro:
        db.session.rollback()

        print(
            "Erro ao deletar professor:",
            erro
        )

        return jsonify({
            "erro": (
                "Não foi possível deletar "
                "o professor."
            )
        }), 500