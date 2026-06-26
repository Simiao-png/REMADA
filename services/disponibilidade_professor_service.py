from flask import jsonify
from models.db import db
from models.disponibilidade_professor import DisponibilidadeProfessor


def disponibilidade_para_dict(disponibilidade):
    return {
        "id": disponibilidade.id,
        "professor_id": disponibilidade.professor_id,
        "dia_semana": disponibilidade.dia_semana,
        "numero_aula": disponibilidade.numero_aula,
        "disponivel": disponibilidade.disponivel
    }


def listar_disponibilidades():
    disponibilidades = DisponibilidadeProfessor.query.all()
    return jsonify([
        disponibilidade_para_dict(disponibilidade)
        for disponibilidade in disponibilidades
    ])


def buscar_disponibilidade(id):
    disponibilidade = DisponibilidadeProfessor.query.get(id)

    if not disponibilidade:
        return jsonify({"erro": "Disponibilidade não encontrada"}), 404

    return jsonify(disponibilidade_para_dict(disponibilidade))


def criar_disponibilidade(dados):
    disponibilidade = DisponibilidadeProfessor(
        professor_id=dados["professor_id"],
        dia_semana=dados["dia_semana"],
        numero_aula=dados["numero_aula"],
        disponivel=dados.get("disponivel", True)
    )

    db.session.add(disponibilidade)
    db.session.commit()

    return jsonify({"mensagem": "Disponibilidade criada com sucesso!"}), 201


def atualizar_disponibilidade(id, dados):
    disponibilidade = DisponibilidadeProfessor.query.get(id)

    if not disponibilidade:
        return jsonify({"erro": "Disponibilidade não encontrada"}), 404

    disponibilidade.professor_id = dados.get("professor_id", disponibilidade.professor_id)
    disponibilidade.dia_semana = dados.get("dia_semana", disponibilidade.dia_semana)
    disponibilidade.numero_aula = dados.get("numero_aula", disponibilidade.numero_aula)
    disponibilidade.disponivel = dados.get("disponivel", disponibilidade.disponivel)

    db.session.commit()

    return jsonify({"mensagem": "Disponibilidade atualizada com sucesso!"})


def deletar_disponibilidade(id):
    disponibilidade = DisponibilidadeProfessor.query.get(id)

    if not disponibilidade:
        return jsonify({"erro": "Disponibilidade não encontrada"}), 404

    db.session.delete(disponibilidade)
    db.session.commit()

    return jsonify({"mensagem": "Disponibilidade deletada com sucesso!"})