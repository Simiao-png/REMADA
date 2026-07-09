from flask import jsonify
from models.db import db
from models.configuracao_horaria import ConfiguracaoHoraria
from models.escola import Escola


NOMES_SEGMENTOS = {
    "fundamental_1": "Fundamental I",
    "fundamental_2": "Fundamental II",
    "ensino_medio": "Ensino Médio",
    "cursinho": "Cursinho"
}


def configuracao_para_dict(configuracao):
    return {
        "id": configuracao.id,
        "escola_id": configuracao.escola_id,
        "segmento": configuracao.segmento,
        "nome": configuracao.nome,
        "aulas_por_dia": configuracao.aulas_por_dia,
        "duracao_aula_minutos": configuracao.duracao_aula_minutos,
        "duracao_intervalo_minutos": configuracao.duracao_intervalo_minutos,
        "tem_aula_segunda": configuracao.tem_aula_segunda,
        "tem_aula_terca": configuracao.tem_aula_terca,
        "tem_aula_quarta": configuracao.tem_aula_quarta,
        "tem_aula_quinta": configuracao.tem_aula_quinta,
        "tem_aula_sexta": configuracao.tem_aula_sexta,
        "tem_aula_sabado": configuracao.tem_aula_sabado,
        "ativo": configuracao.ativo
    }


def listar_configuracoes():
    configuracoes = ConfiguracaoHoraria.query.order_by(
        ConfiguracaoHoraria.id
    ).all()

    return jsonify([
        configuracao_para_dict(configuracao)
        for configuracao in configuracoes
    ])


def buscar_configuracao(id):
    configuracao = ConfiguracaoHoraria.query.get(id)

    if not configuracao:
        return jsonify({"erro": "Configuração horária não encontrada"}), 404

    return jsonify(configuracao_para_dict(configuracao))


def buscar_configuracao_ativa():
    configuracao = ConfiguracaoHoraria.query.filter_by(
        ativo=True
    ).order_by(
        ConfiguracaoHoraria.id
    ).first()

    if not configuracao:
        return None

    return configuracao


def _normalizar_segmentos(dados):
    segmentos = dados.get("segmentos")

    if isinstance(segmentos, dict):
        return [
            {
                "codigo": codigo,
                **valores
            }
            for codigo, valores in segmentos.items()
        ]

    if isinstance(segmentos, list):
        return segmentos

    return [
        {
            "codigo": dados.get("segmento", "geral"),
            "ativo": dados.get("ativo", True),
            "aulas_por_dia": dados.get("aulas_por_dia", 6),
            "duracao_aula": dados.get(
                "duracao_aula",
                dados.get("duracao_aula_minutos", 50)
            ),
            "duracao_intervalo": dados.get(
                "duracao_intervalo",
                dados.get("duracao_intervalo_minutos", 15)
            ),
            "tem_aula_sabado": dados.get(
                "tem_aula_sabado",
                dados.get("sabado", False)
            )
        }
    ]


def salvar_parametros(dados):
    escola = Escola.query.first()

    if not escola:
        return jsonify({"erro": "Nenhuma escola cadastrada."}), 400

    segmentos = _normalizar_segmentos(dados)

    if not segmentos:
        return jsonify({"erro": "Nenhum segmento enviado."}), 400

    for segmento in segmentos:
        codigo = segmento.get("codigo") or segmento.get("segmento")

        if not codigo:
            continue

        configuracao = ConfiguracaoHoraria.query.filter_by(
            escola_id=escola.id,
            segmento=codigo
        ).first()

        if not configuracao:
            configuracao = ConfiguracaoHoraria(
                escola_id=escola.id,
                segmento=codigo,
                nome=NOMES_SEGMENTOS.get(codigo, codigo),
                aulas_por_dia=6,
                duracao_aula_minutos=50,
                duracao_intervalo_minutos=15,
                tem_aula_segunda=True,
                tem_aula_terca=True,
                tem_aula_quarta=True,
                tem_aula_quinta=True,
                tem_aula_sexta=True,
                tem_aula_sabado=False,
                ativo=False
            )

            db.session.add(configuracao)

        configuracao.nome = segmento.get(
            "nome",
            NOMES_SEGMENTOS.get(codigo, codigo)
        )

        configuracao.aulas_por_dia = int(segmento.get("aulas_por_dia", 6))

        configuracao.duracao_aula_minutos = int(
            segmento.get(
                "duracao_aula_minutos",
                segmento.get("duracao_aula", 50)
            )
        )

        configuracao.duracao_intervalo_minutos = int(
            segmento.get(
                "duracao_intervalo_minutos",
                segmento.get("duracao_intervalo", 15)
            )
        )

        configuracao.tem_aula_segunda = True
        configuracao.tem_aula_terca = True
        configuracao.tem_aula_quarta = True
        configuracao.tem_aula_quinta = True
        configuracao.tem_aula_sexta = True

        configuracao.tem_aula_sabado = bool(
            segmento.get(
                "tem_aula_sabado",
                segmento.get("sabado", False)
            )
        )

        configuracao.ativo = bool(segmento.get("ativo", False))

    db.session.commit()

    return jsonify({"mensagem": "Parâmetros salvos com sucesso!"})


def criar_configuracao(dados):
    return salvar_parametros(dados)


def atualizar_configuracao(id, dados):
    configuracao = ConfiguracaoHoraria.query.get(id)

    if not configuracao:
        return jsonify({"erro": "Configuração horária não encontrada"}), 404

    configuracao.segmento = dados.get("segmento", configuracao.segmento)
    configuracao.nome = dados.get("nome", configuracao.nome)
    configuracao.aulas_por_dia = dados.get(
        "aulas_por_dia",
        configuracao.aulas_por_dia
    )

    configuracao.duracao_aula_minutos = dados.get(
        "duracao_aula_minutos",
        configuracao.duracao_aula_minutos
    )

    configuracao.duracao_intervalo_minutos = dados.get(
        "duracao_intervalo_minutos",
        configuracao.duracao_intervalo_minutos
    )

    configuracao.tem_aula_segunda = True
    configuracao.tem_aula_terca = True
    configuracao.tem_aula_quarta = True
    configuracao.tem_aula_quinta = True
    configuracao.tem_aula_sexta = True

    configuracao.tem_aula_sabado = dados.get(
        "tem_aula_sabado",
        configuracao.tem_aula_sabado
    )

    configuracao.ativo = dados.get("ativo", configuracao.ativo)

    db.session.commit()

    return jsonify({"mensagem": "Configuração horária atualizada com sucesso!"})


def deletar_configuracao(id):
    configuracao = ConfiguracaoHoraria.query.get(id)

    if not configuracao:
        return jsonify({"erro": "Configuração horária não encontrada"}), 404

    db.session.delete(configuracao)
    db.session.commit()

    return jsonify({"mensagem": "Configuração horária deletada com sucesso!"})
