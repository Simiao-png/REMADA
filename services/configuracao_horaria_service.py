from flask import jsonify
from models.db import db
from models.configuracao_horaria import ConfiguracaoHoraria


def configuracao_para_dict(configuracao):
    return {
        "id": configuracao.id,
        "escola_id": configuracao.escola_id,
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
    configuracoes = ConfiguracaoHoraria.query.all()
    return jsonify([
        configuracao_para_dict(configuracao)
        for configuracao in configuracoes
    ])


def buscar_configuracao(id):
    configuracao = ConfiguracaoHoraria.query.get(id)

    if not configuracao:
        return jsonify({"erro": "Configuração horária não encontrada"}), 404

    return jsonify(configuracao_para_dict(configuracao))


def criar_configuracao(dados):
    configuracao = ConfiguracaoHoraria(
        escola_id=dados["escola_id"],
        nome=dados["nome"],
        aulas_por_dia=dados["aulas_por_dia"],
        duracao_aula_minutos=dados["duracao_aula_minutos"],
        duracao_intervalo_minutos=dados["duracao_intervalo_minutos"],
        tem_aula_segunda=dados.get("tem_aula_segunda", True),
        tem_aula_terca=dados.get("tem_aula_terca", True),
        tem_aula_quarta=dados.get("tem_aula_quarta", True),
        tem_aula_quinta=dados.get("tem_aula_quinta", True),
        tem_aula_sexta=dados.get("tem_aula_sexta", True),
        tem_aula_sabado=dados.get("tem_aula_sabado", False),
        ativo=dados.get("ativo", True)
    )

    db.session.add(configuracao)
    db.session.commit()

    return jsonify({"mensagem": "Configuração horária criada com sucesso!"}), 201


def atualizar_configuracao(id, dados):
    configuracao = ConfiguracaoHoraria.query.get(id)

    if not configuracao:
        return jsonify({"erro": "Configuração horária não encontrada"}), 404

    configuracao.escola_id = dados.get("escola_id", configuracao.escola_id)
    configuracao.nome = dados.get("nome", configuracao.nome)
    configuracao.aulas_por_dia = dados.get("aulas_por_dia", configuracao.aulas_por_dia)
    configuracao.duracao_aula_minutos = dados.get(
        "duracao_aula_minutos",
        configuracao.duracao_aula_minutos
    )
    configuracao.duracao_intervalo_minutos = dados.get(
        "duracao_intervalo_minutos",
        configuracao.duracao_intervalo_minutos
    )

    configuracao.tem_aula_segunda = dados.get(
        "tem_aula_segunda",
        configuracao.tem_aula_segunda
    )
    configuracao.tem_aula_terca = dados.get(
        "tem_aula_terca",
        configuracao.tem_aula_terca
    )
    configuracao.tem_aula_quarta = dados.get(
        "tem_aula_quarta",
        configuracao.tem_aula_quarta
    )
    configuracao.tem_aula_quinta = dados.get(
        "tem_aula_quinta",
        configuracao.tem_aula_quinta
    )
    configuracao.tem_aula_sexta = dados.get(
        "tem_aula_sexta",
        configuracao.tem_aula_sexta
    )
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