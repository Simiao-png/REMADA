from flask import jsonify
from models.db import db
from models.turma import Turma


def turma_para_dict(turma):
    return {
        "id": turma.id,
        "escola_id": turma.escola_id,
        "configuracao_horaria_id": turma.configuracao_horaria_id,
        "nome": turma.nome,
        "serie": turma.serie,
        "turno": turma.turno,
        "ativo": turma.ativo
    }


def listar_turmas():
    turmas = Turma.query.all()
    return jsonify([turma_para_dict(turma) for turma in turmas])


def buscar_turma(id):
    turma = Turma.query.get(id)

    if not turma:
        return jsonify({"erro": "Turma não encontrada"}), 404

    return jsonify(turma_para_dict(turma))


def criar_turma(dados):
    turma = Turma(
        escola_id=dados["escola_id"],
        configuracao_horaria_id=dados["configuracao_horaria_id"],
        nome=dados["nome"],
        serie=dados["serie"],
        turno=dados["turno"],
        ativo=dados.get("ativo", True)
    )

    db.session.add(turma)
    db.session.commit()

    return jsonify({"mensagem": "Turma criada com sucesso!"}), 201


def atualizar_turma(id, dados):
    turma = Turma.query.get(id)

    if not turma:
        return jsonify({"erro": "Turma não encontrada"}), 404

    turma.escola_id = dados.get("escola_id", turma.escola_id)
    turma.configuracao_horaria_id = dados.get(
        "configuracao_horaria_id",
        turma.configuracao_horaria_id
    )
    turma.nome = dados.get("nome", turma.nome)
    turma.serie = dados.get("serie", turma.serie)
    turma.turno = dados.get("turno", turma.turno)
    turma.ativo = dados.get("ativo", turma.ativo)

    db.session.commit()

    return jsonify({"mensagem": "Turma atualizada com sucesso!"})


def deletar_turma(id):
    turma = Turma.query.get(id)

    if not turma:
        return jsonify({"erro": "Turma não encontrada"}), 404

    db.session.delete(turma)
    db.session.commit()

    return jsonify({"mensagem": "Turma deletada com sucesso!"})