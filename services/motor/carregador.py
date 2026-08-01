from flask import has_request_context, session

from models.escola import Escola
from models.professor import Professor
from models.disciplina import Disciplina
from models.turma import Turma
from models.configuracao_horaria import ConfiguracaoHoraria
from models.disponibilidade_professor import DisponibilidadeProfessor
from models.professor_turma import ProfessorTurma
from models.turma_disciplina import TurmaDisciplina


def obter_escola_id_motor(escola_id=None):
    """
    Resolve a escola usada pelo motor.

    Prioridade:
    1. escola_id informado explicitamente;
    2. escola_id da sessão Flask;
    3. primeira escola cadastrada, apenas como compatibilidade
       para execução manual e diagnóstico local.
    """
    if escola_id:
        return int(escola_id)

    if has_request_context():
        escola_id_sessao = session.get("escola_id")

        if escola_id_sessao:
            return int(escola_id_sessao)

    escola = Escola.query.order_by(Escola.id).first()

    return escola.id if escola else None


def carregar_dados_motor(escola_id=None):
    escola_id = obter_escola_id_motor(escola_id)

    if not escola_id:
        return montar_retorno_vazio()

    escola = Escola.query.get(escola_id)

    if not escola:
        return montar_retorno_vazio()

    query_professores = Professor.query.filter_by(
        escola_id=escola_id
    )

    if hasattr(Professor, "ativo"):
        query_professores = query_professores.filter_by(
            ativo=True
        )

    professores_lista = (
        query_professores
        .order_by(Professor.nome)
        .all()
    )

    query_disciplinas = Disciplina.query.filter_by(
        escola_id=escola_id
    )

    if hasattr(Disciplina, "ativo"):
        query_disciplinas = query_disciplinas.filter_by(
            ativo=True
        )

    disciplinas_lista = (
        query_disciplinas
        .order_by(Disciplina.nome)
        .all()
    )

    query_turmas = Turma.query.filter_by(
        escola_id=escola_id
    )

    if hasattr(Turma, "ativo"):
        query_turmas = query_turmas.filter_by(
            ativo=True
        )

    turmas_lista = (
        query_turmas
        .order_by(
            Turma.segmento,
            Turma.serie,
            Turma.nome
        )
        .all()
    )

    configuracoes_lista = (
        ConfiguracaoHoraria.query
        .filter_by(
            escola_id=escola_id,
            ativo=True
        )
        .all()
    )

    professores_ids = [
        professor.id
        for professor in professores_lista
    ]

    disciplinas_ids = [
        disciplina.id
        for disciplina in disciplinas_lista
    ]

    turmas_ids = [
        turma.id
        for turma in turmas_lista
    ]

    disponibilidades_lista = (
        DisponibilidadeProfessor.query
        .filter(
            DisponibilidadeProfessor.professor_id.in_(
                professores_ids
            )
        )
        .all()
        if professores_ids
        else []
    )

    professor_turma_lista = (
        ProfessorTurma.query
        .filter(
            ProfessorTurma.professor_id.in_(
                professores_ids
            ),
            ProfessorTurma.turma_id.in_(
                turmas_ids
            ),
            ProfessorTurma.disciplina_id.in_(
                disciplinas_ids
            )
        )
        .all()
        if (
            professores_ids
            and turmas_ids
            and disciplinas_ids
        )
        else []
    )

    turma_disciplina_lista = (
        TurmaDisciplina.query
        .filter(
            TurmaDisciplina.turma_id.in_(
                turmas_ids
            ),
            TurmaDisciplina.disciplina_id.in_(
                disciplinas_ids
            ),
            TurmaDisciplina.aulas_por_semana > 0
        )
        .all()
        if turmas_ids and disciplinas_ids
        else []
    )

    dados = {
        "escolas": [escola],
        "professores": professores_lista,
        "disciplinas": disciplinas_lista,
        "turmas": turmas_lista,
        "configuracoes": configuracoes_lista,
        "disponibilidades": disponibilidades_lista,

        # ProfessorTurma já representa a atribuição completa:
        # professor + turma + disciplina.
        "professor_turma": professor_turma_lista,

        "turma_disciplina": turma_disciplina_lista
    }

    imprimir_diagnostico_motor(
        escola,
        dados
    )

    professores = {
        professor.id: professor
        for professor in professores_lista
    }

    turmas = {
        turma.id: turma
        for turma in turmas_lista
    }

    disciplinas = {
        disciplina.id: disciplina
        for disciplina in disciplinas_lista
    }

    configuracoes = {
        configuracao.id: configuracao
        for configuracao in configuracoes_lista
    }

    resumo = {
        "escola_id": escola.id,
        "total_escolas": 1,
        "total_professores": len(
            professores_lista
        ),
        "total_disciplinas": len(
            disciplinas_lista
        ),
        "total_turmas": len(
            turmas_lista
        ),
        "total_configuracoes": len(
            configuracoes_lista
        ),
        "total_disponibilidades": len(
            disponibilidades_lista
        ),
        "total_professor_turma": len(
            professor_turma_lista
        ),
        "total_turma_disciplina": len(
            turma_disciplina_lista
        )
    }

    return {
        "dados": dados,
        "professores": professores,
        "turmas": turmas,
        "disciplinas": disciplinas,
        "configuracoes": configuracoes,
        "resumo": resumo
    }


def carregar_dados(escola_id=None):
    """
    Alias mantido porque o diagnóstico incremental importa
    carregar_dados() diretamente.
    """
    return carregar_dados_motor(
        escola_id=escola_id
    )["dados"]


def imprimir_diagnostico_motor(
    escola,
    dados
):
    print(
        "\n========== DADOS DO MOTOR =========="
    )

    print(
        f"Escola..................: "
        f"{escola.nome} (ID {escola.id})"
    )

    print(
        f"Professores.............: "
        f"{len(dados['professores'])}"
    )

    print(
        f"Disciplinas.............: "
        f"{len(dados['disciplinas'])}"
    )

    print(
        f"Turmas..................: "
        f"{len(dados['turmas'])}"
    )

    print(
        f"Configurações ativas....: "
        f"{len(dados['configuracoes'])}"
    )

    print(
        f"Disponibilidades........: "
        f"{len(dados['disponibilidades'])}"
    )

    print(
        f"Atribuições professor...: "
        f"{len(dados['professor_turma'])}"
    )

    print(
        f"Matriz curricular.......: "
        f"{len(dados['turma_disciplina'])}"
    )

    print(
        "====================================\n"
    )


def montar_retorno_vazio():
    dados = {
        "escolas": [],
        "professores": [],
        "disciplinas": [],
        "turmas": [],
        "configuracoes": [],
        "disponibilidades": [],
        "professor_turma": [],
        "turma_disciplina": []
    }

    return {
        "dados": dados,
        "professores": {},
        "turmas": {},
        "disciplinas": {},
        "configuracoes": {},
        "resumo": {
            "escola_id": None,
            "total_escolas": 0,
            "total_professores": 0,
            "total_disciplinas": 0,
            "total_turmas": 0,
            "total_configuracoes": 0,
            "total_disponibilidades": 0,
            "total_professor_turma": 0,
            "total_turma_disciplina": 0
        }
    }