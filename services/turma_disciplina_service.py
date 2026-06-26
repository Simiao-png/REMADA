from flask import jsonify
from models.db import db
from models.turma_disciplina import TurmaDisciplina


def vinculo_para_dict(vinculo):
    return {
        "turma_id": vinculo.turma_id,
        "disciplina_id": vinculo.disciplina_id
    }


def listar_turma_disciplinas():
    vinculos = TurmaDisciplina.query.all()
    return jsonify([vinculo_para_dict(v) for v in vinculos])


def buscar_turma_disciplina(turma_id, disciplina_id):
    vinculo = TurmaDisciplina.query.get((turma_id, disciplina_id))

    if not vinculo:
        return jsonify({"erro": "Vínculo não encontrado"}), 404

    return jsonify(vinculo_para_dict(vinculo))


def criar_turma_disciplina(dados):
    vinculo = TurmaDisciplina(
        turma_id=dados["turma_id"],
        disciplina_id=dados["disciplina_id"]
    )

    db.session.add(vinculo)
    db.session.commit()

    return jsonify({"mensagem": "Vínculo criado com sucesso!"}), 201


def deletar_turma_disciplina(turma_id, disciplina_id):
    vinculo = TurmaDisciplina.query.get((turma_id, disciplina_id))

    if not vinculo:
        return jsonify({"erro": "Vínculo não encontrado"}), 404

    db.session.delete(vinculo)
    db.session.commit()

    return jsonify({"mensagem": "Vínculo deletado com sucesso!"})