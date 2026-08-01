from flask import Blueprint, request, render_template, session

from models.professor import Professor
from models.disciplina import Disciplina
from models.turma import Turma
from models.turma_disciplina import TurmaDisciplina
from models.professor_turma import ProfessorTurma
from models.disponibilidade_professor import DisponibilidadeProfessor
from models.configuracao_horaria import ConfiguracaoHoraria

from services.disponibilidade_professor_service import (
    listar_disponibilidades,
    buscar_disponibilidade,
    criar_disponibilidade,
    atualizar_disponibilidade,
    salvar_disponibilidade_professor,
    deletar_disponibilidade
)


disponibilidade_professor_bp = Blueprint(
    "disponibilidade_professor",
    __name__
)


@disponibilidade_professor_bp.route(
    "/planejamento/tela",
    methods=["GET"]
)
def tela_planejamento():
    escola_id = session.get("escola_id")

    # CONFIGURAÇÕES DOS SEGMENTOS DA ESCOLA
    query_configs = ConfiguracaoHoraria.query.filter_by(
        ativo=True
    )

    if escola_id:
        query_configs = query_configs.filter_by(
            escola_id=escola_id
        )

    configs = query_configs.all()

    max_aulas = max(
        [
            configuracao.aulas_por_dia
            for configuracao in configs
        ],
        default=7
    )

    if max_aulas < 7:
        max_aulas = 7

    numeros_aulas = list(
        range(1, max_aulas + 1)
    )

    # DIAS DA SEMANA
    configuracao = configs[0] if configs else None

    if configuracao:
        dias_semana = []

        if getattr(
            configuracao,
            "tem_aula_segunda",
            True
        ):
            dias_semana.append({
                "valor": "segunda",
                "label": "Segunda"
            })

        if getattr(
            configuracao,
            "tem_aula_terca",
            True
        ):
            dias_semana.append({
                "valor": "terca",
                "label": "Terça"
            })

        if getattr(
            configuracao,
            "tem_aula_quarta",
            True
        ):
            dias_semana.append({
                "valor": "quarta",
                "label": "Quarta"
            })

        if getattr(
            configuracao,
            "tem_aula_quinta",
            True
        ):
            dias_semana.append({
                "valor": "quinta",
                "label": "Quinta"
            })

        if getattr(
            configuracao,
            "tem_aula_sexta",
            True
        ):
            dias_semana.append({
                "valor": "sexta",
                "label": "Sexta"
            })

        if getattr(
            configuracao,
            "tem_aula_sabado",
            False
        ):
            dias_semana.append({
                "valor": "sabado",
                "label": "Sábado"
            })

    else:
        dias_semana = [
            {
                "valor": "segunda",
                "label": "Segunda"
            },
            {
                "valor": "terca",
                "label": "Terça"
            },
            {
                "valor": "quarta",
                "label": "Quarta"
            },
            {
                "valor": "quinta",
                "label": "Quinta"
            },
            {
                "valor": "sexta",
                "label": "Sexta"
            }
        ]

    # PROFESSORES
    query_professores = Professor.query.order_by(
        Professor.nome
    )

    if escola_id:
        query_professores = query_professores.filter_by(
            escola_id=escola_id
        )

    professores = query_professores.all()

    ids_professores = [
        professor.id
        for professor in professores
    ]

    # TURMAS
    query_turmas = (
        Turma.query
        .filter_by(ativo=True)
        .order_by(
            Turma.segmento,
            Turma.serie,
            Turma.nome
        )
    )

    if escola_id:
        query_turmas = query_turmas.filter_by(
            escola_id=escola_id
        )

    turmas = query_turmas.all()

    ids_turmas = [
        turma.id
        for turma in turmas
    ]

    # DISPONIBILIDADES DOS PROFESSORES DA ESCOLA
    if ids_professores:
        disponibilidades = (
            DisponibilidadeProfessor.query
            .filter(
                DisponibilidadeProfessor.professor_id.in_(
                    ids_professores
                )
            )
            .all()
        )
    else:
        disponibilidades = []

    mapa_disponibilidades = {
        (
            disponibilidade.professor_id,
            disponibilidade.dia_semana,
            disponibilidade.numero_aula
        ): True
        for disponibilidade in disponibilidades
        if disponibilidade.disponivel
    }

    # JSON DOS PROFESSORES
    professores_json = []

    for professor in professores:
        disponibilidades_professor = []

        for dia in dias_semana:
            for numero_aula in numeros_aulas:
                chave = (
                    professor.id,
                    dia["valor"],
                    numero_aula
                )

                if mapa_disponibilidades.get(chave):
                    disponibilidades_professor.append({
                        "dia_semana": dia["valor"],
                        "numero_aula": numero_aula
                    })

        limite_aulas = (
            professor.limite_aulas_semana
            if professor.limite_aulas_semana is not None
            else 0
        )

        professores_json.append({
            "id": professor.id,
            "nome": professor.nome,

            "limite_aulas_semana": limite_aulas,

            # Compatibilidade temporária com o HTML atual.
            "carga_horaria_semanal": limite_aulas,

            "segmentos": [
                segmento.segmento
                if hasattr(segmento, "segmento")
                else str(segmento)
                for segmento in (
                    professor.segmentos or []
                )
            ],

            "disciplinas": [
                {
                    "id": disciplina.id,
                    "nome": disciplina.nome
                }
                for disciplina in (
                    professor.disciplinas or []
                )
            ],

            "disponibilidades": (
                disponibilidades_professor
            )
        })

    # DISCIPLINAS DA ESCOLA
    query_disciplinas = Disciplina.query

    if escola_id:
        query_disciplinas = query_disciplinas.filter_by(
            escola_id=escola_id
        )

    disciplinas = query_disciplinas.all()

    disciplinas_por_id = {
        disciplina.id: disciplina
        for disciplina in disciplinas
    }

    # MATRIZES CURRICULARES DAS TURMAS DA ESCOLA
    if ids_turmas:
        matrizes = (
            TurmaDisciplina.query
            .filter(
                TurmaDisciplina.turma_id.in_(
                    ids_turmas
                ),
                TurmaDisciplina.aulas_por_semana > 0
            )
            .all()
        )
    else:
        matrizes = []

    matrizes_por_turma = {}

    for matriz in matrizes:
        disciplina = disciplinas_por_id.get(
            matriz.disciplina_id
        )

        if not disciplina:
            continue

        if matriz.turma_id not in matrizes_por_turma:
            matrizes_por_turma[
                matriz.turma_id
            ] = []

        matrizes_por_turma[
            matriz.turma_id
        ].append({
            "disciplina_id": matriz.disciplina_id,
            "disciplina_nome": disciplina.nome,
            "aulas_por_semana": (
                matriz.aulas_por_semana
            )
        })

    # JSON DAS TURMAS
    turmas_json = []

    for turma in turmas:
        turmas_json.append({
            "id": turma.id,
            "nome": turma.nome,
            "serie": getattr(
                turma,
                "serie",
                ""
            ),
            "segmento": turma.segmento,
            "turno": getattr(
                turma,
                "turno",
                ""
            ),
            "disciplinas": matrizes_por_turma.get(
                turma.id,
                []
            )
        })

    # ATRIBUIÇÕES DOS PROFESSORES DA ESCOLA
    if ids_professores:
        vinculos = (
            ProfessorTurma.query
            .filter(
                ProfessorTurma.professor_id.in_(
                    ids_professores
                )
            )
            .all()
        )
    else:
        vinculos = []

    atribuicoes_json = [
        {
            "professor_id": vinculo.professor_id,
            "turma_id": vinculo.turma_id,
            "disciplina_id": vinculo.disciplina_id
        }
        for vinculo in vinculos
    ]

    return render_template(
        "planejamento.html",
        professores=professores,
        professores_json=professores_json,
        turmas_json=turmas_json,
        atribuicoes_json=atribuicoes_json,
        dias_semana=dias_semana,
        numeros_aulas=numeros_aulas
    )


@disponibilidade_professor_bp.route(
    "/disponibilidades",
    methods=["GET"]
)
def listar():
    return listar_disponibilidades()


@disponibilidade_professor_bp.route(
    "/disponibilidades/<int:id>",
    methods=["GET"]
)
def buscar(id):
    return buscar_disponibilidade(id)


@disponibilidade_professor_bp.route(
    "/disponibilidades",
    methods=["POST"]
)
def criar():
    dados = request.get_json() or {}
    return criar_disponibilidade(dados)


@disponibilidade_professor_bp.route(
    "/disponibilidades/professor/<int:professor_id>",
    methods=["POST"]
)
def salvar_por_professor(professor_id):
    dados = request.get_json() or {}

    return salvar_disponibilidade_professor(
        professor_id,
        dados
    )


@disponibilidade_professor_bp.route(
    "/disponibilidades/<int:id>",
    methods=["PUT"]
)
def atualizar(id):
    dados = request.get_json() or {}

    return atualizar_disponibilidade(
        id,
        dados
    )


@disponibilidade_professor_bp.route(
    "/disponibilidades/<int:id>",
    methods=["DELETE"]
)
def deletar(id):
    return deletar_disponibilidade(id)