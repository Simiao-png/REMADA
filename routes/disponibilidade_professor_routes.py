from flask import Blueprint, request, render_template
from models.professor import Professor
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

disponibilidade_professor_bp = Blueprint("disponibilidade_professor", __name__)


@disponibilidade_professor_bp.route("/planejamento/tela", methods=["GET"])
def tela_planejamento():
    configuracao = ConfiguracaoHoraria.query.filter_by(ativo=True).first()

    if configuracao:
        dias_semana = []

        if configuracao.tem_aula_segunda:
            dias_semana.append({"valor": "segunda", "label": "Segunda"})

        if configuracao.tem_aula_terca:
            dias_semana.append({"valor": "terca", "label": "Terça"})

        if configuracao.tem_aula_quarta:
            dias_semana.append({"valor": "quarta", "label": "Quarta"})

        if configuracao.tem_aula_quinta:
            dias_semana.append({"valor": "quinta", "label": "Quinta"})

        if configuracao.tem_aula_sexta:
            dias_semana.append({"valor": "sexta", "label": "Sexta"})

        if configuracao.tem_aula_sabado:
            dias_semana.append({"valor": "sabado", "label": "Sábado"})

        numeros_aulas = list(range(1, configuracao.aulas_por_dia + 1))

    else:
        dias_semana = [
            {"valor": "segunda", "label": "Segunda"},
            {"valor": "terca", "label": "Terça"},
            {"valor": "quarta", "label": "Quarta"},
            {"valor": "quinta", "label": "Quinta"},
            {"valor": "sexta", "label": "Sexta"}
        ]

        numeros_aulas = [1, 2, 3, 4, 5, 6]

    professores = Professor.query.order_by(Professor.nome).all()
    disponibilidades = DisponibilidadeProfessor.query.all()

    mapa_disponibilidades = {}

    for disponibilidade in disponibilidades:
        chave = (
            f"{disponibilidade.professor_id}-"
            f"{disponibilidade.dia_semana}-"
            f"{disponibilidade.numero_aula}"
        )

        mapa_disponibilidades[chave] = True

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
            "disciplinas": [
                disciplina.nome for disciplina in professor.disciplinas
            ] if professor.disciplinas else [],
            "disponibilidades": disponibilidades_professor
        })

    return render_template(
        "planejamento.html",
        professores=professores,
        professores_json=professores_json,
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