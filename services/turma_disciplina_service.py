from flask import jsonify, session

from models.db import db
from models.turma import Turma
from models.disciplina import Disciplina
from models.turma_disciplina import TurmaDisciplina
from models.configuracao_horaria import ConfiguracaoHoraria


def vinculo_para_dict(vinculo):
    return {
        "turma_id": vinculo.turma_id,
        "disciplina_id": vinculo.disciplina_id,
        "aulas_por_semana": vinculo.aulas_por_semana
    }


def obter_escola_id_atual():
    return session.get("escola_id")


def calcular_capacidade_semanal(turma):
    configuracao = None

    if turma.configuracao_horaria_id:
        configuracao = db.session.get(
            ConfiguracaoHoraria,
            turma.configuracao_horaria_id
        )

    if not configuracao:
        configuracao = ConfiguracaoHoraria.query.filter_by(
            escola_id=turma.escola_id,
            segmento=turma.segmento,
            ativo=True
        ).first()

    if not configuracao:
        return None

    quantidade_dias = 6 if configuracao.tem_aula_sabado else 5

    return {
        "configuracao_horaria_id": configuracao.id,
        "aulas_por_dia": configuracao.aulas_por_dia,
        "quantidade_dias": quantidade_dias,
        "tem_aula_sabado": bool(configuracao.tem_aula_sabado),
        "capacidade_semanal": (
            configuracao.aulas_por_dia * quantidade_dias
        )
    }


def buscar_turma_da_escola(turma_id):
    escola_id = obter_escola_id_atual()

    if not escola_id:
        return None

    return Turma.query.filter_by(
        id=turma_id,
        escola_id=escola_id
    ).first()


def buscar_disciplina_da_escola(disciplina_id):
    escola_id = obter_escola_id_atual()

    if not escola_id:
        return None

    return Disciplina.query.filter_by(
        id=disciplina_id,
        escola_id=escola_id
    ).first()


def listar_turma_disciplinas():
    escola_id = obter_escola_id_atual()

    if not escola_id:
        return jsonify({
            "erro": "Nenhuma escola selecionada."
        }), 400

    vinculos = (
        TurmaDisciplina.query
        .join(
            Turma,
            Turma.id == TurmaDisciplina.turma_id
        )
        .filter(
            Turma.escola_id == escola_id
        )
        .all()
    )

    return jsonify([
        vinculo_para_dict(vinculo)
        for vinculo in vinculos
    ])


def listar_matriz_da_turma(turma_id):
    escola_id = obter_escola_id_atual()

    if not escola_id:
        return jsonify({
            "erro": "Nenhuma escola selecionada."
        }), 400

    turma = buscar_turma_da_escola(turma_id)

    if not turma:
        return jsonify({
            "erro": "Turma não encontrada."
        }), 404

    capacidade = calcular_capacidade_semanal(turma)

    if not capacidade:
        return jsonify({
            "erro": (
                "A turma não possui uma configuração "
                "horária ativa."
            )
        }), 400

    disciplinas = Disciplina.query.filter_by(
        escola_id=escola_id
    ).order_by(
        Disciplina.nome
    ).all()

    vinculos = TurmaDisciplina.query.filter_by(
        turma_id=turma.id
    ).all()

    aulas_por_disciplina = {
        vinculo.disciplina_id: vinculo.aulas_por_semana
        for vinculo in vinculos
    }

    matriz = []

    for disciplina in disciplinas:
        matriz.append({
            "disciplina_id": disciplina.id,
            "disciplina_nome": disciplina.nome,
            "disciplina_cor": disciplina.cor or "#2563EB",
            "aulas_por_semana": aulas_por_disciplina.get(
                disciplina.id,
                0
            )
        })

    total_aulas = sum(
        item["aulas_por_semana"]
        for item in matriz
    )

    capacidade_semanal = capacidade["capacidade_semanal"]
    diferenca = capacidade_semanal - total_aulas

    return jsonify({
        "turma": {
            "id": turma.id,
            "nome": turma.nome,
            "serie": turma.serie,
            "segmento": turma.segmento,
            "turno": turma.turno
        },
        "configuracao": capacidade,
        "disciplinas": matriz,
        "resumo": {
            "total_aulas": total_aulas,
            "capacidade_semanal": capacidade_semanal,
            "faltam": max(diferenca, 0),
            "excedeu": max(-diferenca, 0),
            "completa": total_aulas == capacidade_semanal,
            "ultrapassou": total_aulas > capacidade_semanal
        }
    })


def buscar_turma_disciplina(turma_id, disciplina_id):
    escola_id = obter_escola_id_atual()

    if not escola_id:
        return jsonify({
            "erro": "Nenhuma escola selecionada."
        }), 400

    turma = buscar_turma_da_escola(turma_id)

    if not turma:
        return jsonify({
            "erro": "Turma não encontrada."
        }), 404

    disciplina = buscar_disciplina_da_escola(
        disciplina_id
    )

    if not disciplina:
        return jsonify({
            "erro": "Disciplina não encontrada."
        }), 404

    vinculo = db.session.get(
        TurmaDisciplina,
        (turma_id, disciplina_id)
    )

    if not vinculo:
        return jsonify({
            "erro": "Vínculo não encontrado."
        }), 404

    return jsonify(vinculo_para_dict(vinculo))


def criar_turma_disciplina(dados):
    escola_id = obter_escola_id_atual()

    if not escola_id:
        return jsonify({
            "erro": "Nenhuma escola selecionada."
        }), 400

    if not dados:
        return jsonify({
            "erro": "Nenhum dado enviado."
        }), 400

    turma_id = dados.get("turma_id")
    disciplina_id = dados.get("disciplina_id")
    aulas_por_semana = dados.get(
        "aulas_por_semana",
        0
    )

    if not turma_id or not disciplina_id:
        return jsonify({
            "erro": (
                "Turma e disciplina são obrigatórias."
            )
        }), 400

    if (
        isinstance(aulas_por_semana, bool)
        or not isinstance(aulas_por_semana, int)
        or aulas_por_semana < 0
    ):
        return jsonify({
            "erro": (
                "A quantidade de aulas deve ser "
                "um número inteiro maior ou igual a zero."
            )
        }), 400

    turma = buscar_turma_da_escola(turma_id)

    if not turma:
        return jsonify({
            "erro": "Turma não encontrada."
        }), 404

    disciplina = buscar_disciplina_da_escola(
        disciplina_id
    )

    if not disciplina:
        return jsonify({
            "erro": "Disciplina não encontrada."
        }), 404

    capacidade = calcular_capacidade_semanal(turma)

    if not capacidade:
        return jsonify({
            "erro": (
                "A turma não possui uma configuração "
                "horária ativa."
            )
        }), 400

    vinculos_atuais = TurmaDisciplina.query.filter_by(
        turma_id=turma.id
    ).all()

    total_sem_disciplina_atual = sum(
        vinculo.aulas_por_semana
        for vinculo in vinculos_atuais
        if vinculo.disciplina_id != disciplina.id
    )

    novo_total = (
        total_sem_disciplina_atual
        + aulas_por_semana
    )

    if novo_total > capacidade["capacidade_semanal"]:
        excesso = (
            novo_total
            - capacidade["capacidade_semanal"]
        )

        return jsonify({
            "erro": (
                f"A matriz ultrapassaria a carga semanal "
                f"da turma em {excesso} aula(s)."
            ),
            "total_informado": novo_total,
            "capacidade_semanal": (
                capacidade["capacidade_semanal"]
            ),
            "excedeu": excesso
        }), 400

    try:
        vinculo = db.session.get(
            TurmaDisciplina,
            (turma_id, disciplina_id)
        )

        if aulas_por_semana == 0:
            if vinculo:
                db.session.delete(vinculo)

            db.session.commit()

            return jsonify({
                "mensagem": (
                    "Disciplina removida da matriz."
                ),
                "total_aulas": novo_total,
                "capacidade_semanal": (
                    capacidade["capacidade_semanal"]
                )
            })

        if vinculo:
            vinculo.aulas_por_semana = (
                aulas_por_semana
            )
        else:
            vinculo = TurmaDisciplina(
                turma_id=turma_id,
                disciplina_id=disciplina_id,
                aulas_por_semana=aulas_por_semana
            )

            db.session.add(vinculo)

        db.session.commit()

        return jsonify({
            "mensagem": "Vínculo salvo com sucesso!",
            "vinculo": vinculo_para_dict(vinculo),
            "total_aulas": novo_total,
            "capacidade_semanal": (
                capacidade["capacidade_semanal"]
            )
        }), 201

    except Exception as erro:
        db.session.rollback()

        return jsonify({
            "erro": (
                "Não foi possível salvar o vínculo: "
                f"{str(erro)}"
            )
        }), 500


def salvar_matriz_curricular(turma_id, dados):
    escola_id = obter_escola_id_atual()

    if not escola_id:
        return jsonify({
            "erro": "Nenhuma escola selecionada."
        }), 400

    turma = buscar_turma_da_escola(turma_id)

    if not turma:
        return jsonify({
            "erro": "Turma não encontrada."
        }), 404

    if not dados:
        return jsonify({
            "erro": "Nenhum dado enviado."
        }), 400

    disciplinas_recebidas = dados.get("disciplinas")

    if not isinstance(disciplinas_recebidas, list):
        return jsonify({
            "erro": "Envie uma lista de disciplinas."
        }), 400

    capacidade = calcular_capacidade_semanal(turma)

    if not capacidade:
        return jsonify({
            "erro": (
                "A turma não possui uma configuração "
                "horária ativa."
            )
        }), 400

    disciplinas_validadas = []
    ids_recebidos = set()
    total_aulas = 0

    try:
        for item in disciplinas_recebidas:
            if not isinstance(item, dict):
                raise ValueError(
                    "Há uma disciplina inválida na matriz."
                )

            disciplina_id = item.get("disciplina_id")
            aulas_por_semana = item.get(
                "aulas_por_semana",
                0
            )

            if not disciplina_id:
                raise ValueError(
                    "Disciplina inválida."
                )

            if disciplina_id in ids_recebidos:
                raise ValueError(
                    "Uma disciplina foi enviada mais de uma vez."
                )

            ids_recebidos.add(disciplina_id)

            if (
                isinstance(aulas_por_semana, bool)
                or not isinstance(aulas_por_semana, int)
                or aulas_por_semana < 0
            ):
                raise ValueError(
                    "A quantidade de aulas deve ser um "
                    "número inteiro maior ou igual a zero."
                )

            disciplina = buscar_disciplina_da_escola(
                disciplina_id
            )

            if not disciplina:
                raise ValueError(
                    f"Disciplina {disciplina_id} "
                    "não encontrada nesta escola."
                )

            total_aulas += aulas_por_semana

            disciplinas_validadas.append({
                "disciplina_id": disciplina.id,
                "aulas_por_semana": aulas_por_semana
            })

        capacidade_semanal = (
            capacidade["capacidade_semanal"]
        )

        if total_aulas > capacidade_semanal:
            excesso = total_aulas - capacidade_semanal

            return jsonify({
                "erro": (
                    f"A matriz possui {total_aulas} aulas, "
                    f"mas a turma comporta no máximo "
                    f"{capacidade_semanal}. "
                    f"Reduza {excesso} aula(s)."
                ),
                "total_aulas": total_aulas,
                "capacidade_semanal": capacidade_semanal,
                "excedeu": excesso
            }), 400

        TurmaDisciplina.query.filter_by(
            turma_id=turma.id
        ).delete(
            synchronize_session=False
        )

        for item in disciplinas_validadas:
            if item["aulas_por_semana"] == 0:
                continue

            vinculo = TurmaDisciplina(
                turma_id=turma.id,
                disciplina_id=item["disciplina_id"],
                aulas_por_semana=(
                    item["aulas_por_semana"]
                )
            )

            db.session.add(vinculo)

        db.session.commit()

        faltam = capacidade_semanal - total_aulas

        return jsonify({
            "mensagem": (
                "Matriz curricular salva com sucesso!"
            ),
            "resumo": {
                "total_aulas": total_aulas,
                "capacidade_semanal": capacidade_semanal,
                "faltam": faltam,
                "excedeu": 0,
                "completa": faltam == 0,
                "ultrapassou": False
            }
        })

    except ValueError as erro:
        db.session.rollback()

        return jsonify({
            "erro": str(erro)
        }), 400

    except Exception as erro:
        db.session.rollback()

        return jsonify({
            "erro": (
                "Não foi possível salvar a matriz "
                f"curricular: {str(erro)}"
            )
        }), 500


def deletar_turma_disciplina(
    turma_id,
    disciplina_id
):
    escola_id = obter_escola_id_atual()

    if not escola_id:
        return jsonify({
            "erro": "Nenhuma escola selecionada."
        }), 400

    turma = buscar_turma_da_escola(turma_id)

    if not turma:
        return jsonify({
            "erro": "Turma não encontrada."
        }), 404

    disciplina = buscar_disciplina_da_escola(
        disciplina_id
    )

    if not disciplina:
        return jsonify({
            "erro": "Disciplina não encontrada."
        }), 404

    vinculo = db.session.get(
        TurmaDisciplina,
        (turma_id, disciplina_id)
    )

    if not vinculo:
        return jsonify({
            "erro": "Vínculo não encontrado."
        }), 404

    try:
        db.session.delete(vinculo)
        db.session.commit()

        return jsonify({
            "mensagem": (
                "Vínculo deletado com sucesso!"
            )
        })

    except Exception as erro:
        db.session.rollback()

        return jsonify({
            "erro": (
                "Não foi possível deletar o vínculo: "
                f"{str(erro)}"
            )
        }), 500