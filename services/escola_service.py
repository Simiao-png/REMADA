from flask import jsonify

from models.db import db
from models.escola import Escola
from models.disciplina import Disciplina


DISCIPLINAS_PADRAO = [
    {
        "nome": "Arte",
        "cor": "#F97316"
    },
    {
        "nome": "Biologia",
        "cor": "#16A34A"
    },
    {
        "nome": "Ciências",
        "cor": "#22C55E"
    },
    {
        "nome": "Educação Física",
        "cor": "#06B6D4"
    },
    {
        "nome": "Espanhol",
        "cor": "#EAB308"
    },
    {
        "nome": "Filosofia",
        "cor": "#7C3AED"
    },
    {
        "nome": "Física",
        "cor": "#F97316"
    },
    {
        "nome": "Geografia",
        "cor": "#F59E0B"
    },
    {
        "nome": "História",
        "cor": "#92400E"
    },
    {
        "nome": "Língua Inglesa",
        "cor": "#0EA5E9"
    },
    {
        "nome": "Língua Portuguesa",
        "cor": "#EF4444"
    },
    {
        "nome": "Literatura",
        "cor": "#EC4899"
    },
    {
        "nome": "Matemática",
        "cor": "#2563EB"
    },
    {
        "nome": "Português",
        "cor": "#DC2626"
    },
    {
        "nome": "Química",
        "cor": "#8B5CF6"
    },
    {
        "nome": "Sociologia",
        "cor": "#64748B"
    },
    {
        "nome": "Teatro",
        "cor": "#D946EF"
    }
]


def escola_para_dict(escola):
    return {
        "id": escola.id,
        "nome": escola.nome,
        "cidade": escola.cidade,
        "estado": escola.estado
    }


def normalizar_texto(valor):
    return str(
        valor or ""
    ).strip()


def criar_disciplinas_padrao(
    escola_id
):
    """
    Cria somente as disciplinas padrão que ainda não existem
    para a escola informada.

    A comparação é feita pelo nome em minúsculas para evitar
    duplicações como 'Matemática' e 'matemática'.
    """
    disciplinas_existentes = (
        Disciplina.query
        .filter_by(
            escola_id=escola_id
        )
        .all()
    )

    nomes_existentes = {
        normalizar_texto(
            disciplina.nome
        ).lower()
        for disciplina in disciplinas_existentes
    }

    quantidade_criada = 0

    for item in DISCIPLINAS_PADRAO:
        nome = normalizar_texto(
            item["nome"]
        )

        if nome.lower() in nomes_existentes:
            continue

        disciplina = Disciplina(
            escola_id=escola_id,
            nome=nome,
            cor=item["cor"],
            ativo=True
        )

        db.session.add(
            disciplina
        )

        nomes_existentes.add(
            nome.lower()
        )

        quantidade_criada += 1

    return quantidade_criada


def listar_escolas():
    escolas = (
        Escola.query
        .order_by(
            Escola.nome
        )
        .all()
    )

    return jsonify([
        escola_para_dict(
            escola
        )
        for escola in escolas
    ])


def buscar_escola(id):
    escola = db.session.get(
        Escola,
        id
    )

    if not escola:
        return jsonify({
            "erro": "Escola não encontrada."
        }), 404

    return jsonify(
        escola_para_dict(
            escola
        )
    )


def criar_escola(dados):
    dados = dados or {}

    nome = normalizar_texto(
        dados.get(
            "nome"
        )
    )

    cidade = normalizar_texto(
        dados.get(
            "cidade"
        )
    )

    estado = normalizar_texto(
        dados.get(
            "estado"
        )
    ).upper()

    if not nome:
        return jsonify({
            "erro": "O nome da escola é obrigatório."
        }), 400

    if not cidade:
        return jsonify({
            "erro": "A cidade é obrigatória."
        }), 400

    if not estado:
        return jsonify({
            "erro": "O estado é obrigatório."
        }), 400

    escola = Escola(
        nome=nome,
        cidade=cidade,
        estado=estado
    )

    try:
        db.session.add(
            escola
        )

        # Gera o ID antes de criar as disciplinas vinculadas.
        db.session.flush()

        quantidade_disciplinas = (
            criar_disciplinas_padrao(
                escola.id
            )
        )

        db.session.commit()

        return jsonify({
            "mensagem": (
                "Escola criada com sucesso!"
            ),
            "escola": escola_para_dict(
                escola
            ),
            "disciplinas_padrao_criadas": (
                quantidade_disciplinas
            )
        }), 201

    except Exception as erro:
        db.session.rollback()

        print(
            "Erro ao criar escola:",
            erro
        )

        return jsonify({
            "erro": (
                "Não foi possível criar a escola."
            )
        }), 500


def atualizar_escola(id, dados):
    dados = dados or {}

    escola = db.session.get(
        Escola,
        id
    )

    if not escola:
        return jsonify({
            "erro": "Escola não encontrada."
        }), 404

    nome = normalizar_texto(
        dados.get(
            "nome",
            escola.nome
        )
    )

    cidade = normalizar_texto(
        dados.get(
            "cidade",
            escola.cidade
        )
    )

    estado = normalizar_texto(
        dados.get(
            "estado",
            escola.estado
        )
    ).upper()

    if not nome:
        return jsonify({
            "erro": "O nome da escola é obrigatório."
        }), 400

    if not cidade:
        return jsonify({
            "erro": "A cidade é obrigatória."
        }), 400

    if not estado:
        return jsonify({
            "erro": "O estado é obrigatório."
        }), 400

    escola.nome = nome
    escola.cidade = cidade
    escola.estado = estado

    try:
        db.session.commit()

        return jsonify({
            "mensagem": (
                "Escola atualizada com sucesso!"
            ),
            "escola": escola_para_dict(
                escola
            )
        })

    except Exception as erro:
        db.session.rollback()

        print(
            "Erro ao atualizar escola:",
            erro
        )

        return jsonify({
            "erro": (
                "Não foi possível atualizar a escola."
            )
        }), 500


def completar_disciplinas_padrao(
    escola_id
):
    """
    Pode ser usado uma única vez para escolas antigas.

    Cria apenas as disciplinas padrão que ainda estiverem faltando.
    """
    escola = db.session.get(
        Escola,
        escola_id
    )

    if not escola:
        return jsonify({
            "erro": "Escola não encontrada."
        }), 404

    try:
        quantidade_criada = (
            criar_disciplinas_padrao(
                escola.id
            )
        )

        db.session.commit()

        return jsonify({
            "mensagem": (
                f"{quantidade_criada} disciplina(s) "
                "padrão criada(s)."
            ),
            "escola_id": escola.id,
            "disciplinas_criadas": (
                quantidade_criada
            )
        })

    except Exception as erro:
        db.session.rollback()

        print(
            "Erro ao completar disciplinas padrão:",
            erro
        )

        return jsonify({
            "erro": (
                "Não foi possível criar as "
                "disciplinas padrão."
            )
        }), 500


def deletar_escola(id):
    escola = db.session.get(
        Escola,
        id
    )

    if not escola:
        return jsonify({
            "erro": "Escola não encontrada."
        }), 404

    try:
        db.session.delete(
            escola
        )

        db.session.commit()

        return jsonify({
            "mensagem": (
                "Escola deletada com sucesso!"
            )
        })

    except Exception as erro:
        db.session.rollback()

        print(
            "Erro ao deletar escola:",
            erro
        )

        return jsonify({
            "erro": (
                "Não foi possível deletar a escola. "
                "Verifique se existem registros vinculados."
            )
        }), 500