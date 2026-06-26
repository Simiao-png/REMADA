from flask import jsonify
from models.db import db
from models.professor_turma import ProfessorTurma


def vinculo_para_dict(vinculo):
    return {
        "professor_id": vinculo.professor_id,
        "turma_id": vinculo.turma_id
    }


def listar_professor_turmas():
    vinculos = ProfessorTurma.query.all()
    return jsonify([vinculo_para_dict(v) for v in vinculos])


def buscar_professor_turma(professor_id, turma_id):
    vinculo = ProfessorTurma.query.get((professor_id, turma_id))

    if not vinculo:
        return jsonify({"erro": "Vínculo não encontrado"}), 404

    return jsonify(vinculo_para_dict(vinculo))


def criar_professor_turma(dados):
    vinculo = ProfessorTurma(
        professor_id=dados["professor_id"],
        turma_id=dados["turma_id"]
    )

    db.session.add(vinculo)
    db.session.commit()

    return jsonify({"mensagem": "Vínculo criado com sucesso!"}), 201


def deletar_professor_turma(professor_id, turma_id):
    vinculo = ProfessorTurma.query.get((professor_id, turma_id))

    if not vinculo:
        return jsonify({"erro": "Vínculo não encontrado"}), 404

    db.session.delete(vinculo)
    db.session.commit()

    return jsonify({"mensagem": "Vínculo deletado com sucesso!"})