from flask import jsonify
from models.db import db
from models.professor import Professor


def professor_para_dict(professor):
    return {
        "id": professor.id,
        "escola_id": professor.escola_id,
        "nome": professor.nome,
        "email": professor.email,
        "telefone": professor.telefone,
        "ativo": professor.ativo,
        "trabalha_outra_escola": professor.trabalha_outra_escola,
        "observacoes": professor.observacoes
    }


def listar_professores():
    professores = Professor.query.all()
    return jsonify([professor_para_dict(professor) for professor in professores])


def buscar_professor(id):
    professor = Professor.query.get(id)

    if not professor:
        return jsonify({"erro": "Professor não encontrado"}), 404

    return jsonify(professor_para_dict(professor))


def criar_professor(dados):
    professor = Professor(
        escola_id=dados["escola_id"],
        nome=dados["nome"],
        email=dados.get("email"),
        telefone=dados.get("telefone"),
        ativo=dados.get("ativo", True),
        trabalha_outra_escola=dados.get("trabalha_outra_escola", False),
        observacoes=dados.get("observacoes")
    )

    db.session.add(professor)
    db.session.commit()

    return jsonify({"mensagem": "Professor criado com sucesso!"}), 201


def atualizar_professor(id, dados):
    professor = Professor.query.get(id)

    if not professor:
        return jsonify({"erro": "Professor não encontrado"}), 404

    professor.escola_id = dados.get("escola_id", professor.escola_id)
    professor.nome = dados.get("nome", professor.nome)
    professor.email = dados.get("email", professor.email)
    professor.telefone = dados.get("telefone", professor.telefone)
    professor.ativo = dados.get("ativo", professor.ativo)
    professor.trabalha_outra_escola = dados.get(
        "trabalha_outra_escola",
        professor.trabalha_outra_escola
    )
    professor.observacoes = dados.get("observacoes", professor.observacoes)

    db.session.commit()

    return jsonify({"mensagem": "Professor atualizado com sucesso!"})


def deletar_professor(id):
    professor = Professor.query.get(id)

    if not professor:
        return jsonify({"erro": "Professor não encontrado"}), 404

    db.session.delete(professor)
    db.session.commit()

    return jsonify({"mensagem": "Professor deletado com sucesso!"})