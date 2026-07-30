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

    # 1. BUSCA O MÁXIMO DE AULAS POR DIA (Busca todos os segmentos da escola e pega o maior valor)
    configs = ConfiguracaoHoraria.query.filter_by(ativo=True).all()
    if escola_id:
        configs = [c for c in configs if getattr(c, 'escola_id', None) == escola_id]

    max_aulas = max([c.aulas_por_dia for c in configs]) if configs else 7
    if max_aulas < 7:
        max_aulas = 7  # Garante 7 aulas por padrão para o Ensino Médio

    numeros_aulas = list(range(1, max_aulas + 1))  # [1, 2, 3, 4, 5, 6, 7]

    # Dias da semana
    configuracao = configs[0] if configs else None
    if configuracao:
        dias_semana = []
        if getattr(configuracao, 'tem_aula_segunda', True):
            dias_semana.append({"valor": "segunda", "label": "Segunda"})
        if getattr(configuracao, 'tem_aula_terca', True):
            dias_semana.append({"valor": "terca", "label": "Terça"})
        if getattr(configuracao, 'tem_aula_quarta', True):
            dias_semana.append({"valor": "quarta", "label": "Quarta"})
        if getattr(configuracao, 'tem_aula_quinta', True):
            dias_semana.append({"valor": "quinta", "label": "Quinta"})
        if getattr(configuracao, 'tem_aula_sexta', True):
            dias_semana.append({"valor": "sexta", "label": "Sexta"})
        if getattr(configuracao, 'tem_aula_sabado', False):
            dias_semana.append({"valor": "sabado", "label": "Sábado"})
    else:
        dias_semana = [
            {"valor": "segunda", "label": "Segunda"},
            {"valor": "terca", "label": "Terça"},
            {"valor": "quarta", "label": "Quarta"},
            {"valor": "quinta", "label": "Quinta"},
            {"valor": "sexta", "label": "Sexta"}
        ]

    # 2. CONSULTAS COM FILTRO MULTI-ESCOLA
    query_professores = Professor.query.order_by(Professor.nome)
    query_turmas = Turma.query.filter_by(ativo=True).order_by(Turma.segmento, Turma.serie, Turma.nome)

    if escola_id:
        if hasattr(Professor, 'escola_id'):
            query_professores = query_professores.filter_by(escola_id=escola_id)
        if hasattr(Turma, 'escola_id'):
            query_turmas = query_turmas.filter_by(escola_id=escola_id)

    professores = query_professores.all()
    turmas = query_turmas.all()

    disponibilidades = DisponibilidadeProfessor.query.all()
    mapa_disponibilidades = {
        f"{d.professor_id}-{d.dia_semana}-{d.numero_aula}": True for d in disponibilidades
    }

    # 3. MONTAGEM DO JSON DOS PROFESSORES
    professores_json = []
    for professor in professores:
        disponibilidades_professor = []
        for dia in dias_semana:
            for numero_aula in numeros_aulas:
                chave = f"{professor.id}-{dia['valor']}-{numero_aula}"
                if mapa_disponibilidades.get(chave):
                    disponibilidades_professor.append({
                        "dia_semana": dia["valor"],
                        "numero_aula": numero_aula
                    })

        professores_json.append({
            "id": professor.id,
            "nome": professor.nome,
            "carga_horaria_semanal": getattr(professor, 'carga_horaria_semanal', 0) or getattr(professor, 'carga_horaria', 0) or 0,
            "segmentos": [
                s.segmento if hasattr(s, 'segmento') else str(s) for s in (professor.segmentos or [])
            ],
            "disciplinas": [
                {"id": d.id, "nome": d.nome} for d in (professor.disciplinas or [])
            ],
            "disponibilidades": disponibilidades_professor
        })

    # 4. MONTAGEM DO JSON DAS TURMAS E MATRIZES
    disciplinas = Disciplina.query.all()
    disciplinas_por_id = {d.id: d for d in disciplinas}
    matrizes = TurmaDisciplina.query.filter(TurmaDisciplina.aulas_por_semana > 0).all()

    matrizes_por_turma = {}
    for matriz in matrizes:
        disciplina = disciplinas_por_id.get(matriz.disciplina_id)
        if not disciplina:
            continue
        if matriz.turma_id not in matrizes_por_turma:
            matrizes_por_turma[matriz.turma_id] = []
        matrizes_por_turma[matriz.turma_id].append({
            "disciplina_id": matriz.disciplina_id,
            "disciplina_nome": disciplina.nome,
            "aulas_por_semana": matriz.aulas_por_semana
        })

    turmas_json = []
    for turma in turmas:
        turmas_json.append({
            "id": turma.id,
            "nome": turma.nome,
            "serie": getattr(turma, 'serie', ''),
            "segmento": turma.segmento,
            "turno": getattr(turma, 'turno', ''),
            "disciplinas": matrizes_por_turma.get(turma.id, [])
        })

    # 5. ATRIBUIÇÕES
    vinculos = ProfessorTurma.query.all()
    atribuicoes_json = [
        {
            "professor_id": v.professor_id,
            "turma_id": v.turma_id,
            "disciplina_id": v.disciplina_id
        } for v in vinculos
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


@disponibilidade_professor_bp.route("/disponibilidades", methods=["GET"])
def listar():
    return listar_disponibilidades()


@disponibilidade_professor_bp.route("/disponibilidades/<int:id>", methods=["GET"])
def buscar(id):
    return buscar_disponibilidade(id)


@disponibilidade_professor_bp.route("/disponibilidades", methods=["POST"])
def criar():
    return criar_disponibilidade(request.get_json())


@disponibilidade_professor_bp.route("/disponibilidades/professor/<int:professor_id>", methods=["POST"])
def salvar_por_professor(professor_id):
    return salvar_disponibilidade_professor(professor_id, request.get_json())


@disponibilidade_professor_bp.route("/disponibilidades/<int:id>", methods=["PUT"])
def atualizar(id):
    return atualizar_disponibilidade(id, request.get_json())


@disponibilidade_professor_bp.route("/disponibilidades/<int:id>", methods=["DELETE"])
def deletar(id):
    return deletar_disponibilidade(id)