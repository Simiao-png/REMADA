from flask import jsonify, session

from models.db import db
from models.turma import Turma
from models.escola import Escola
from models.configuracao_horaria import ConfiguracaoHoraria


SEGMENTOS_VALIDOS = {
    "fundamental_1",
    "fundamental_2",
    "ensino_medio",
    "cursinho"
}


def turma_para_dict(turma):
    return {
        "id": turma.id,
        "escola_id": turma.escola_id,
        "configuracao_horaria_id": turma.configuracao_horaria_id,
        "nome": turma.nome,
        "serie": turma.serie,
        "segmento": turma.segmento,
        "turno": turma.turno,
        "ativo": turma.ativo
    }


def obter_escola_atual():
    escola_id = session.get("escola_id")

    if not escola_id:
        return None

    return db.session.get(Escola, escola_id)


def listar_turmas():
    escola = obter_escola_atual()

    if not escola:
        return jsonify({"erro": "Nenhuma escola selecionada."}), 400

    turmas = Turma.query.filter_by(
        escola_id=escola.id
    ).order_by(
        Turma.nome
    ).all()

    return jsonify([
        turma_para_dict(turma)
        for turma in turmas
    ])


def buscar_turma(id):
    escola = obter_escola_atual()

    if not escola:
        return jsonify({"erro": "Nenhuma escola selecionada."}), 400

    turma = Turma.query.filter_by(
        id=id,
        escola_id=escola.id
    ).first()

    if not turma:
        return jsonify({"erro": "Turma não encontrada."}), 404

    return jsonify(turma_para_dict(turma))


def criar_turma(dados):
    escola = obter_escola_atual()

    if not escola:
        return jsonify({"erro": "Nenhuma escola selecionada."}), 400

    if not dados:
        return jsonify({"erro": "Nenhum dado enviado."}), 400

    campos_obrigatorios = [
        "nome",
        "serie",
        "segmento",
        "turno"
    ]

    campos_ausentes = [
        campo
        for campo in campos_obrigatorios
        if not dados.get(campo)
    ]

    if campos_ausentes:
        return jsonify({
            "erro": "Preencha todos os campos obrigatórios.",
            "campos": campos_ausentes
        }), 400

    segmento = dados["segmento"]

    if segmento not in SEGMENTOS_VALIDOS:
        return jsonify({"erro": "Segmento inválido."}), 400

    configuracao = ConfiguracaoHoraria.query.filter_by(
        escola_id=escola.id,
        segmento=segmento,
        ativo=True
    ).first()

    if not configuracao:
        return jsonify({
            "erro": "Nenhuma configuração horária ativa para este segmento."
        }), 400

    try:
        turma = Turma(
            escola_id=escola.id,
            configuracao_horaria_id=configuracao.id,
            nome=dados["nome"].strip(),
            serie=dados["serie"].strip(),
            segmento=segmento,
            turno=dados["turno"],
            ativo=dados.get("ativo", True)
        )

        db.session.add(turma)
        db.session.commit()

        return jsonify({
            "mensagem": "Turma criada com sucesso!",
            "turma": turma_para_dict(turma)
        }), 201

    except Exception as erro:
        db.session.rollback()

        return jsonify({
            "erro": f"Erro ao criar turma: {str(erro)}"
        }), 500


def atualizar_turma(id, dados):
    escola = obter_escola_atual()

    if not escola:
        return jsonify({"erro": "Nenhuma escola selecionada."}), 400

    turma = Turma.query.filter_by(
        id=id,
        escola_id=escola.id
    ).first()

    if not turma:
        return jsonify({"erro": "Turma não encontrada."}), 404

    if not dados:
        return jsonify({"erro": "Nenhum dado enviado."}), 400

    segmento = dados.get("segmento", turma.segmento)

    if segmento not in SEGMENTOS_VALIDOS:
        return jsonify({"erro": "Segmento inválido."}), 400

    if "nome" in dados and not dados["nome"]:
        return jsonify({
            "erro": "O nome da turma é obrigatório."
        }), 400

    if "serie" in dados and not dados["serie"]:
        return jsonify({
            "erro": "A série da turma é obrigatória."
        }), 400

    if "turno" in dados and not dados["turno"]:
        return jsonify({
            "erro": "O turno da turma é obrigatório."
        }), 400

    configuracao = ConfiguracaoHoraria.query.filter_by(
        escola_id=escola.id,
        segmento=segmento,
        ativo=True
    ).first()

    if not configuracao:
        return jsonify({
            "erro": "Nenhuma configuração horária ativa para este segmento."
        }), 400

    try:
        turma.nome = dados.get(
            "nome",
            turma.nome
        ).strip()

        turma.serie = dados.get(
            "serie",
            turma.serie
        ).strip()

        turma.segmento = segmento
        turma.turno = dados.get("turno", turma.turno)
        turma.ativo = dados.get("ativo", turma.ativo)
        turma.configuracao_horaria_id = configuracao.id

        db.session.commit()

        return jsonify({
            "mensagem": "Turma atualizada com sucesso!",
            "turma": turma_para_dict(turma)
        })

    except Exception as erro:
        db.session.rollback()

        return jsonify({
            "erro": f"Erro ao atualizar turma: {str(erro)}"
        }), 500


def deletar_turma(id):
    escola = obter_escola_atual()

    if not escola:
        return jsonify({"erro": "Nenhuma escola selecionada."}), 400

    turma = Turma.query.filter_by(
        id=id,
        escola_id=escola.id
    ).first()

    if not turma:
        return jsonify({"erro": "Turma não encontrada."}), 404

    try:
        db.session.delete(turma)
        db.session.commit()

        return jsonify({
            "mensagem": "Turma deletada com sucesso!"
        })

    except Exception as erro:
        db.session.rollback()

        return jsonify({
            "erro": f"Erro ao deletar turma: {str(erro)}"
        }), 500