from flask import jsonify
from models.db import db
from models.carga_horaria import CargaHoraria


def carga_horaria_para_dict(carga):
    return {
        "id": carga.id,
        "turma_id": carga.turma_id,
        "disciplina_id": carga.disciplina_id,
        "quantidade_aulas_semana": carga.quantidade_aulas_semana,
        "permite_aula_dupla": carga.permite_aula_dupla,
        "permite_aula_tripla": carga.permite_aula_tripla,
        "exige_distribuicao_semanal": carga.exige_distribuicao_semanal,
        "quantidade_minima_dias_semana": carga.quantidade_minima_dias_semana
    }


def listar_cargas_horarias():
    cargas = CargaHoraria.query.all()
    return jsonify([carga_horaria_para_dict(carga) for carga in cargas])


def buscar_carga_horaria(id):
    carga = CargaHoraria.query.get(id)

    if not carga:
        return jsonify({"erro": "Carga horária não encontrada"}), 404

    return jsonify(carga_horaria_para_dict(carga))


def criar_carga_horaria(dados):
    carga = CargaHoraria(
        turma_id=dados["turma_id"],
        disciplina_id=dados["disciplina_id"],
        quantidade_aulas_semana=dados["quantidade_aulas_semana"],
        permite_aula_dupla=dados.get("permite_aula_dupla", True),
        permite_aula_tripla=dados.get("permite_aula_tripla", False),
        exige_distribuicao_semanal=dados.get("exige_distribuicao_semanal", False),
        quantidade_minima_dias_semana=dados.get("quantidade_minima_dias_semana", 1)
    )

    db.session.add(carga)
    db.session.commit()

    return jsonify({"mensagem": "Carga horária criada com sucesso!"}), 201


def atualizar_carga_horaria(id, dados):
    carga = CargaHoraria.query.get(id)

    if not carga:
        return jsonify({"erro": "Carga horária não encontrada"}), 404

    carga.turma_id = dados.get("turma_id", carga.turma_id)
    carga.disciplina_id = dados.get("disciplina_id", carga.disciplina_id)
    carga.quantidade_aulas_semana = dados.get(
        "quantidade_aulas_semana",
        carga.quantidade_aulas_semana
    )
    carga.permite_aula_dupla = dados.get(
        "permite_aula_dupla",
        carga.permite_aula_dupla
    )
    carga.permite_aula_tripla = dados.get(
        "permite_aula_tripla",
        carga.permite_aula_tripla
    )
    carga.exige_distribuicao_semanal = dados.get(
        "exige_distribuicao_semanal",
        carga.exige_distribuicao_semanal
    )
    carga.quantidade_minima_dias_semana = dados.get(
        "quantidade_minima_dias_semana",
        carga.quantidade_minima_dias_semana
    )

    db.session.commit()

    return jsonify({"mensagem": "Carga horária atualizada com sucesso!"})


def deletar_carga_horaria(id):
    carga = CargaHoraria.query.get(id)

    if not carga:
        return jsonify({"erro": "Carga horária não encontrada"}), 404

    db.session.delete(carga)
    db.session.commit()

    return jsonify({"mensagem": "Carga horária deletada com sucesso!"})