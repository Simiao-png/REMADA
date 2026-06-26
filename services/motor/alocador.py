from services.motor.validacoes import (
    pode_alocar_aula,
    pode_alocar_dupla
)

from services.motor.heuristicas import ordenar_dias_por_menor_ocupacao
from services.motor.penalidades import calcular_penalidade
from services.motor.debug_penalidades import imprimir_candidato


def alocar_melhor_posicao(
    grade,
    aula,
    disponibilidades,
    aulas_restantes
):
    turma_id = aula["turma_id"]
    professor_id = aula["professor_id"]
    disciplina_id = aula["disciplina_id"]

    aula_grade = {
        "professor": professor_id,
        "disciplina": disciplina_id
    }

    candidatos = coletar_candidatos(
        grade,
        aula,
        disponibilidades,
        aulas_restantes
    )

    if len(candidatos) == 0:
        return 0

    melhor_candidato = escolher_melhor_candidato(candidatos)

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

    grade[turma_id][dia][indice] = aula_grade

    if quantidade == 2:
        grade[turma_id][dia][indice + 1] = aula_grade

    return quantidade


def coletar_candidatos(
    grade,
    aula,
    disponibilidades,
    aulas_restantes
):
    candidatos = []

    turma_id = aula["turma_id"]
    professor_id = aula["professor_id"]
    disciplina_id = aula["disciplina_id"]

    dias_ordenados = ordenar_dias_por_menor_ocupacao(
        grade,
        turma_id
    )

    if aulas_restantes >= 2:
        for dia in dias_ordenados:
            horarios = grade[turma_id][dia]

            for indice, horario in enumerate(horarios):
                if pode_alocar_dupla(
                    grade,
                    disponibilidades,
                    turma_id,
                    professor_id,
                    disciplina_id,
                    dia,
                    indice
                ):
                    penalidade = calcular_penalidade(
                        grade,
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

    if len(candidatos) == 0:
        for dia in dias_ordenados:
            horarios = grade[turma_id][dia]

            for indice, horario in enumerate(horarios):
                if pode_alocar_aula(
                    grade,
                    disponibilidades,
                    turma_id,
                    professor_id,
                    disciplina_id,
                    dia,
                    indice
                ):
                    penalidade = calcular_penalidade(
                        grade,
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

    return candidatos


def escolher_melhor_candidato(candidatos):
    candidatos_ordenados = sorted(
        candidatos,
        key=lambda candidato: (
            candidato["penalidade"],
            candidato["indice"]
        )
    )

    return candidatos_ordenados[0]