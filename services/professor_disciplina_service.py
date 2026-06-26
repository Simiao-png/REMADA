from flask import jsonify
from models.db import db
from models.professor_disciplina import ProfessorDisciplina


def vinculo_para_dict(vinculo):
    return {
        "id": vinculo.id,
        "professor_id": vinculo.professor_id,
        "disciplina_id": vinculo.disciplina_id
    }


def listar_professor_disciplinas():
    vinculos = ProfessorDisciplina.query.all()
    return jsonify([vinculo_para_dict(vinculo) for vinculo in vinculos])


def buscar_professor_disciplina(id):
    vinculo = ProfessorDisciplina.query.get(id)

    if not vinculo:
        return jsonify({"erro": "Vínculo não encontrado"}), 404

    return jsonify(vinculo_para_dict(vinculo))


def criar_professor_disciplina(dados):
    vinculo = ProfessorDisciplina(
        professor_id=dados["professor_id"],
        disciplina_id=dados["disciplina_id"]
    )

    db.session.add(vinculo)
    db.session.commit()

    return jsonify({"mensagem": "Vínculo criado com sucesso!"}), 201


def atualizar_professor_disciplina(id, dados):
    vinculo = ProfessorDisciplina.query.get(id)

    if not vinculo:
        return jsonify({"erro": "Vínculo não encontrado"}), 404

    vinculo.professor_id = dados.get("professor_id", vinculo.professor_id)
    vinculo.disciplina_id = dados.get("disciplina_id", vinculo.disciplina_id)

    db.session.commit()

    return jsonify({"mensagem": "Vínculo atualizado com sucesso!"})


def deletar_professor_disciplina(id):
    vinculo = ProfessorDisciplina.query.get(id)

    if not vinculo:
        return jsonify({"erro": "Vínculo não encontrado"}), 404

    db.session.delete(vinculo)
    db.session.commit()

    return jsonify({"mensagem": "Vínculo deletado com sucesso!"})