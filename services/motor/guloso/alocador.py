import random

from services.motor.guloso.validacoes import (
    validar_alocacao_aula,
    validar_alocacao_dupla
)

from services.motor.guloso.heuristicas import (
    ordenar_dias_por_menor_ocupacao
)

from services.motor.guloso.penalidades import (
    calcular_penalidade
)

from services.motor.guloso.debug_penalidades import (
    imprimir_candidato
)

from services.motor.guloso.estado import (
    registrar_aula
)

DESCRICOES_MOTIVOS = {
    "turma_ocupada": (
        "A turma já possui outra aula "
        "nesse horário."
    ),
    "professor_ocupado": (
        "O professor já está dando aula "
        "para outra turma nesse horário."
    ),
    "professor_indisponivel": (
        "O professor não está disponível "
        "nesse horário."
    ),
    "limite_disciplina_dia": (
        "A turma já atingiu o limite de "
        "2 aulas dessa disciplina no dia."
    ),
    "sem_espaco_para_dupla": (
        "Não existem dois horários "
        "consecutivos disponíveis."
    )
}


def alocar_melhor_posicao(
    estado,
    aula,
    disponibilidades,
    aulas_restantes
):
    grade = estado["grade"]

    turma_id = aula["turma_id"]
    professor_id = aula["professor_id"]
    disciplina_id = aula["disciplina_id"]

    aula_grade = {
        "professor": professor_id,
        "disciplina": disciplina_id
    }

    resultado_candidatos = coletar_candidatos(
        estado,
        aula,
        disponibilidades,
        aulas_restantes
    )

    candidatos = resultado_candidatos[
        "candidatos"
    ]

    if not candidatos:
        aula["diagnostico"] = montar_diagnostico(
            resultado_candidatos[
                "rejeicoes"
            ]
        )

        return 0

    melhor_candidato = escolher_melhor_candidato(
        candidatos
    )

    dia = melhor_candidato["dia"]
    indice = melhor_candidato["indice"]
    quantidade = melhor_candidato["quantidade"]
    penalidade = melhor_candidato["penalidade"]

    print(
        f"ESCOLHIDA -> Turma {turma_id} | "
        f"Disciplina {disciplina_id} | "
        f"Professor {professor_id} | "
        f"{dia} aula {indice + 1} | "
        f"Qtd {quantidade} | "
        f"Penalidade {penalidade}"
    )

    for deslocamento in range(quantidade):
        indice_atual = indice + deslocamento

        grade[turma_id][dia][indice_atual] = (
            aula_grade.copy()
        )

        registrar_aula(
            estado,
            turma_id,
            professor_id,
            disciplina_id,
            dia,
            indice_atual
        )

    return quantidade


def coletar_candidatos(
    estado,
    aula,
    disponibilidades,
    aulas_restantes
):
    grade = estado["grade"]
    candidatos = []

    rejeicoes = {
        "simples": {},
        "dupla": {},
        "horarios": []
    }

    turma_id = aula["turma_id"]
    professor_id = aula["professor_id"]
    disciplina_id = aula["disciplina_id"]

    dias_ordenados = ordenar_dias_por_menor_ocupacao(
        estado,
        turma_id
    )

    permite_dupla = (
        aula.get(
            "permite_aula_dupla",
            False
        )
        and aulas_restantes >= 2
    )

    for dia in dias_ordenados:
        horarios = grade[turma_id][dia]

        for indice in range(len(horarios)):
            validacao_simples = (
                validar_alocacao_aula(
                    estado,
                    disponibilidades,
                    turma_id,
                    professor_id,
                    disciplina_id,
                    dia,
                    indice
                )
            )

            if validacao_simples["valido"]:
                penalidade = calcular_penalidade(
                    estado,
                    turma_id,
                    professor_id,
                    disciplina_id,
                    dia,
                    indice,
                    quantidade_aulas=1
                )

                imprimir_candidato(
                    turma_id,
                    disciplina_id,
                    professor_id,
                    dia,
                    indice,
                    1,
                    penalidade
                )

                candidatos.append({
                    "dia": dia,
                    "indice": indice,
                    "quantidade": 1,
                    "penalidade": penalidade
                })

            else:
                registrar_rejeicao(
                    rejeicoes,
                    "simples",
                    validacao_simples["motivo"],
                    dia,
                    indice
                )

            if permite_dupla:
                validacao_dupla = (
                    validar_alocacao_dupla(
                        estado,
                        disponibilidades,
                        turma_id,
                        professor_id,
                        disciplina_id,
                        dia,
                        indice
                    )
                )

                if validacao_dupla["valido"]:
                    penalidade = calcular_penalidade(
                        estado,
                        turma_id,
                        professor_id,
                        disciplina_id,
                        dia,
                        indice,
                        quantidade_aulas=2
                    )

                    imprimir_candidato(
                        turma_id,
                        disciplina_id,
                        professor_id,
                        dia,
                        indice,
                        2,
                        penalidade
                    )

                    candidatos.append({
                        "dia": dia,
                        "indice": indice,
                        "quantidade": 2,
                        "penalidade": penalidade
                    })

                else:
                    registrar_rejeicao(
                        rejeicoes,
                        "dupla",
                        validacao_dupla["motivo"],
                        dia,
                        indice
                    )

    return {
        "candidatos": candidatos,
        "rejeicoes": rejeicoes
    }


def registrar_rejeicao(
    rejeicoes,
    tipo,
    motivo,
    dia,
    indice
):
    if not motivo:
        return

    rejeicoes[tipo][motivo] = (
        rejeicoes[tipo].get(
            motivo,
            0
        )
        + 1
    )

    if tipo == "simples":
        rejeicoes["horarios"].append({
            "dia": dia,
            "numero_aula": indice + 1,
            "motivo": motivo,
            "descricao": (
                DESCRICOES_MOTIVOS.get(
                    motivo,
                    motivo
                )
            )
        })


def montar_diagnostico(rejeicoes):
    motivos_simples = rejeicoes.get(
        "simples",
        {}
    )

    motivos_dupla = rejeicoes.get(
        "dupla",
        {}
    )

    horarios = rejeicoes.get(
        "horarios",
        []
    )

    motivo_principal = None

    if motivos_simples:
        motivo_principal = max(
            motivos_simples,
            key=motivos_simples.get
        )

    resumo = []

    for motivo, quantidade in sorted(
        motivos_simples.items(),
        key=lambda item: item[1],
        reverse=True
    ):
        resumo.append({
            "codigo": motivo,
            "descricao": (
                DESCRICOES_MOTIVOS.get(
                    motivo,
                    motivo
                )
            ),
            "quantidade_horarios": quantidade
        })

    return {
        "motivo_principal": motivo_principal,
        "descricao_principal": (
            DESCRICOES_MOTIVOS.get(
                motivo_principal,
                "Nenhuma posição válida encontrada."
            )
        ),
        "resumo": resumo,
        "rejeicoes_aula_dupla": motivos_dupla,
        "horarios_analisados": horarios,
        "total_horarios_analisados": len(
            horarios
        )
    }


def escolher_melhor_candidato(candidatos):
    menor_penalidade = min(
        candidato["penalidade"]
        for candidato in candidatos
    )

    melhores_candidatos = [
        candidato
        for candidato in candidatos
        if candidato["penalidade"] == menor_penalidade
    ]

    return random.choice(
        melhores_candidatos
    )