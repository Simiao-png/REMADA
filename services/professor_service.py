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


def normalizar_lista_ids(valores):
    if not isinstance(valores, list):
        return []

    ids_normalizados = []

    for valor in valores:
        valor_normalizado = normalizar_inteiro_positivo(
            valor
        )

        if (
            valor_normalizado
            and valor_normalizado not in ids_normalizados
        ):
            ids_normalizados.append(
                valor_normalizado
            )

    return ids_normalizados


def buscar_disciplinas_da_escola(
    disciplinas_ids,
    escola_id
):
    disciplinas_ids = normalizar_lista_ids(
        disciplinas_ids
    )

    if not disciplinas_ids:
        return []

    disciplinas = (
        Disciplina.query
        .filter(
            Disciplina.escola_id == escola_id,
            Disciplina.id.in_(disciplinas_ids)
        )
        .all()
    )

    disciplinas_por_id = {
        disciplina.id: disciplina
        for disciplina in disciplinas
    }

    return [
        disciplinas_por_id[disciplina_id]
        for disciplina_id in disciplinas_ids
        if disciplina_id in disciplinas_por_id
    ]


def sincronizar_disciplinas_professor(
    professor,
    disciplinas
):
    ProfessorDisciplina.query.filter_by(
        professor_id=professor.id
    ).delete(
        synchronize_session=False
    )

    for disciplina in disciplinas:
        db.session.add(
            ProfessorDisciplina(
                professor_id=professor.id,
                disciplina_id=disciplina.id
            )
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

    disciplinas_ordenadas = sorted(
        professor.disciplinas or [],
        key=lambda disciplina: disciplina.nome.lower()
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
        "disciplinas_ids": [
            disciplina.id
            for disciplina in disciplinas_ordenadas
        ],
        "disciplinas": [
            {
                "id": disciplina.id,
                "nome": disciplina.nome,
                "cor": getattr(
                    disciplina,
                    "cor",
                    None
                )
            }
            for disciplina in disciplinas_ordenadas
        ],
        "trabalha_outra_escola": (
            professor.trabalha_outra_escola
        ),
        "observacoes": professor.observacoes,
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

    disciplinas_ids = normalizar_lista_ids(
        dados.get(
            "disciplinas_ids",
            []
        )
    )

    disciplina_principal_id = (
        normalizar_inteiro_positivo(
            dados.get(
                "disciplina_principal_id"
            )
        )
    )

    if (
        disciplina_principal_id
        and disciplina_principal_id not in disciplinas_ids
    ):
        disciplinas_ids.insert(
            0,
            disciplina_principal_id
        )

    if not disciplinas_ids:
        return jsonify({
            "erro": (
                "Adicione pelo menos uma disciplina "
                "ao professor."
            )
        }), 400

    disciplinas = buscar_disciplinas_da_escola(
        disciplinas_ids,
        escola.id
    )

    if len(disciplinas) != len(disciplinas_ids):
        return jsonify({
            "erro": (
                "Uma ou mais disciplinas selecionadas "
                "não pertencem à escola atual."
            )
        }), 400

    disciplina_principal = disciplinas[0]

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

        db.session.flush()

        sincronizar_disciplinas_professor(
            professor,
            disciplinas
        )

        db.session.commit()

        professor = (
            Professor.query
            .filter_by(
                id=professor.id
            )
            .first()
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

    disciplinas_ids = normalizar_lista_ids(
        dados.get(
            "disciplinas_ids",
            [
                disciplina.id
                for disciplina in (
                    professor.disciplinas or []
                )
            ]
        )
    )

    disciplina_principal_id = (
        normalizar_inteiro_positivo(
            dados.get(
                "disciplina_principal_id",
                professor.disciplina_principal_id
            )
        )
    )

    if (
        disciplina_principal_id
        and disciplina_principal_id not in disciplinas_ids
    ):
        disciplinas_ids.insert(
            0,
            disciplina_principal_id
        )

    if not disciplinas_ids:
        return jsonify({
            "erro": (
                "Adicione pelo menos uma disciplina "
                "ao professor."
            )
        }), 400

    disciplinas = buscar_disciplinas_da_escola(
        disciplinas_ids,
        professor.escola_id
    )

    if len(disciplinas) != len(disciplinas_ids):
        return jsonify({
            "erro": (
                "Uma ou mais disciplinas selecionadas "
                "não pertencem à escola atual."
            )
        }), 400

    disciplina_principal = disciplinas[0]

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
        sincronizar_disciplinas_professor(
            professor,
            disciplinas
        )

        db.session.commit()

        professor = (
            Professor.query
            .filter_by(
                id=professor.id
            )
            .first()
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