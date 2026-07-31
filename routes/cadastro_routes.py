from flask import Blueprint, render_template, session

from models.db import db
from models.professor import Professor
from models.disciplina import Disciplina
from models.turma import Turma
from models.escola import Escola
from models.configuracao_horaria import ConfiguracaoHoraria


cadastro_bp = Blueprint("cadastro", __name__)


SEGMENTOS = {
    "fundamental_1": {
        "nome": "Fundamental I",
        "classe_cor": "badge-fundamental-1",
        "aulas_por_dia": 5,
        "duracao_aula": 50,
        "duracao_intervalo": 15,
        "tem_aula_sabado": False,
    },
    "fundamental_2": {
        "nome": "Fundamental II",
        "classe_cor": "badge-fundamental-2",
        "aulas_por_dia": 6,
        "duracao_aula": 50,
        "duracao_intervalo": 15,
        "tem_aula_sabado": False,
    },
    "ensino_medio": {
        "nome": "Ensino Médio",
        "classe_cor": "badge-ensino-medio",
        "aulas_por_dia": 7,
        "duracao_aula": 50,
        "duracao_intervalo": 15,
        "tem_aula_sabado": False,
    },
    "cursinho": {
        "nome": "Cursinho",
        "classe_cor": "badge-cursinho",
        "aulas_por_dia": 6,
        "duracao_aula": 50,
        "duracao_intervalo": 15,
        "tem_aula_sabado": False,
    },
}


def _valor_configuracao(configuracao, campo, padrao):
    """Lê o valor da configuração sem quebrar caso o registro ainda não exista."""
    if configuracao is None:
        return padrao

    valor = getattr(configuracao, campo, None)
    return padrao if valor is None else valor


@cadastro_bp.route("/cadastros/tela", methods=["GET"])
def tela_cadastros():
    escola_id = session.get("escola_id")

    escola = db.session.get(Escola, escola_id) if escola_id else None

    if escola:
        professores = (
            Professor.query
            .filter_by(escola_id=escola.id)
            .order_by(Professor.nome)
            .all()
        )

        disciplinas = (
            Disciplina.query
            .filter_by(escola_id=escola.id)
            .order_by(Disciplina.nome)
            .all()
        )

        turmas = (
            Turma.query
            .filter_by(escola_id=escola.id)
            .order_by(Turma.nome)
            .all()
        )

        configuracoes = (
            ConfiguracaoHoraria.query
            .filter_by(escola_id=escola.id)
            .all()
        )
    else:
        professores = []
        disciplinas = []
        turmas = []
        configuracoes = []

    configuracoes_por_segmento = {
        configuracao.segmento: configuracao
        for configuracao in configuracoes
        if configuracao.segmento in SEGMENTOS
    }

    parametros_segmentos = {}
    segmentos_ativos = []
    segmentos_inativos = []

    for codigo, padrao in SEGMENTOS.items():
        configuracao = configuracoes_por_segmento.get(codigo)

        ativo = bool(
            configuracao is not None
            and getattr(configuracao, "ativo", False)
        )

        dados_js = {
            "ativo": ativo,
            "aulas_por_dia": _valor_configuracao(
                configuracao,
                "aulas_por_dia",
                padrao["aulas_por_dia"],
            ),
            "duracao_aula": _valor_configuracao(
                configuracao,
                "duracao_aula",
                padrao["duracao_aula"],
            ),
            "duracao_intervalo": _valor_configuracao(
                configuracao,
                "duracao_intervalo",
                padrao["duracao_intervalo"],
            ),
            "tem_aula_sabado": bool(
                _valor_configuracao(
                    configuracao,
                    "tem_aula_sabado",
                    padrao["tem_aula_sabado"],
                )
            ),
        }

        parametros_segmentos[codigo] = dados_js

        dados_tela = {
            "codigo": codigo,
            "nome": padrao["nome"],
            "classe_cor": padrao["classe_cor"],
            "ativo": ativo,
            "aulas_por_dia": dados_js["aulas_por_dia"],
        }

        if ativo:
            segmentos_ativos.append(dados_tela)
        else:
            segmentos_inativos.append(dados_tela)

    segmentos_ativos_codigos = {
        segmento["codigo"]
        for segmento in segmentos_ativos
    }

    segmento_inicial = (
        segmentos_ativos[0]["codigo"]
        if segmentos_ativos
        else "fundamental_2"
    )

    return render_template(
        "cadastros.html",
        escola=escola,
        professores=professores,
        disciplinas=disciplinas,
        turmas=turmas,
        segmentos_ativos=segmentos_ativos,
        segmentos_inativos=segmentos_inativos,
        segmentos_ativos_codigos=segmentos_ativos_codigos,
        possui_segmentos_ativos=bool(segmentos_ativos),
        parametros_segmentos=parametros_segmentos,
        segmento_inicial=segmento_inicial,
    )
