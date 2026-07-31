from flask import jsonify, session

from models.db import db
from models.configuracao_horaria import ConfiguracaoHoraria
from models.escola import Escola


NOMES_SEGMENTOS = {
    "fundamental_1": "Fundamental I",
    "fundamental_2": "Fundamental II",
    "ensino_medio": "Ensino Médio",
    "cursinho": "Cursinho"
}


def obter_escola_atual():
    escola_id = session.get("escola_id")

    if not escola_id:
        return None

    return db.session.get(Escola, escola_id)


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
    escola = obter_escola_atual()

    if not escola:
        return jsonify({"erro": "Nenhuma escola selecionada."}), 400

    configuracoes = ConfiguracaoHoraria.query.filter_by(
        escola_id=escola.id
    ).order_by(
        ConfiguracaoHoraria.id
    ).all()

    return jsonify([
        configuracao_para_dict(configuracao)
        for configuracao in configuracoes
    ])


def buscar_configuracao(id):
    escola = obter_escola_atual()

    if not escola:
        return jsonify({"erro": "Nenhuma escola selecionada."}), 400

    configuracao = ConfiguracaoHoraria.query.filter_by(
        id=id,
        escola_id=escola.id
    ).first()

    if not configuracao:
        return jsonify({
            "erro": "Configuração horária não encontrada."
        }), 404

    return jsonify(configuracao_para_dict(configuracao))


def buscar_configuracao_ativa(segmento=None):
    escola = obter_escola_atual()

    if not escola:
        return None

    consulta = ConfiguracaoHoraria.query.filter_by(
        escola_id=escola.id,
        ativo=True
    )

    if segmento:
        consulta = consulta.filter_by(segmento=segmento)

    return consulta.order_by(
        ConfiguracaoHoraria.id
    ).first()


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
    escola = obter_escola_atual()

    if not escola:
        return jsonify({"erro": "Nenhuma escola selecionada."}), 400

    segmentos = _normalizar_segmentos(dados)

    if not segmentos:
        return jsonify({"erro": "Nenhum segmento enviado."}), 400

    try:
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

            configuracao.aulas_por_dia = int(
                segmento.get("aulas_por_dia", 6)
            )

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

            configuracao.ativo = bool(
                segmento.get("ativo", False)
            )

        db.session.commit()

        return jsonify({
            "mensagem": "Parâmetros salvos com sucesso!"
        })

    except (TypeError, ValueError):
        db.session.rollback()

        return jsonify({
            "erro": "Os valores dos parâmetros são inválidos."
        }), 400

    except Exception as erro:
        db.session.rollback()

        return jsonify({
            "erro": f"Erro ao salvar os parâmetros: {str(erro)}"
        }), 500


def criar_configuracao(dados):
    return salvar_parametros(dados)


def atualizar_configuracao(id, dados):
    escola = obter_escola_atual()

    if not escola:
        return jsonify({"erro": "Nenhuma escola selecionada."}), 400

    configuracao = ConfiguracaoHoraria.query.filter_by(
        id=id,
        escola_id=escola.id
    ).first()

    if not configuracao:
        return jsonify({
            "erro": "Configuração horária não encontrada."
        }), 404

    try:
        configuracao.segmento = dados.get(
            "segmento",
            configuracao.segmento
        )

        configuracao.nome = dados.get(
            "nome",
            configuracao.nome
        )

        configuracao.aulas_por_dia = int(
            dados.get(
                "aulas_por_dia",
                configuracao.aulas_por_dia
            )
        )

        configuracao.duracao_aula_minutos = int(
            dados.get(
                "duracao_aula_minutos",
                dados.get(
                    "duracao_aula",
                    configuracao.duracao_aula_minutos
                )
            )
        )

        configuracao.duracao_intervalo_minutos = int(
            dados.get(
                "duracao_intervalo_minutos",
                dados.get(
                    "duracao_intervalo",
                    configuracao.duracao_intervalo_minutos
                )
            )
        )

        configuracao.tem_aula_segunda = True
        configuracao.tem_aula_terca = True
        configuracao.tem_aula_quarta = True
        configuracao.tem_aula_quinta = True
        configuracao.tem_aula_sexta = True

        configuracao.tem_aula_sabado = bool(
            dados.get(
                "tem_aula_sabado",
                configuracao.tem_aula_sabado
            )
        )

        configuracao.ativo = bool(
            dados.get(
                "ativo",
                configuracao.ativo
            )
        )

        db.session.commit()

        return jsonify({
            "mensagem": "Configuração horária atualizada com sucesso!"
        })

    except (TypeError, ValueError):
        db.session.rollback()

        return jsonify({
            "erro": "Os valores da configuração são inválidos."
        }), 400

    except Exception as erro:
        db.session.rollback()

        return jsonify({
            "erro": f"Erro ao atualizar a configuração: {str(erro)}"
        }), 500


def deletar_configuracao(id):
    escola = obter_escola_atual()

    if not escola:
        return jsonify({"erro": "Nenhuma escola selecionada."}), 400

    configuracao = ConfiguracaoHoraria.query.filter_by(
        id=id,
        escola_id=escola.id
    ).first()

    if not configuracao:
        return jsonify({
            "erro": "Configuração horária não encontrada."
        }), 404

    try:
        db.session.delete(configuracao)
        db.session.commit()

        return jsonify({
            "mensagem": "Configuração horária deletada com sucesso!"
        })

    except Exception as erro:
        db.session.rollback()

        return jsonify({
            "erro": f"Erro ao deletar a configuração: {str(erro)}"
        }), 500