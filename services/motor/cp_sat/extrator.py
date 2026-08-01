from services.motor.estrutura import (
    criar_grade_vazia
)


def extrair_grade(
    solver,
    variaveis,
    dados,
    turmas
):
    configuracoes = dados.get(
        "configuracoes",
        []
    )

    grade = criar_grade_vazia(
        configuracoes,
        turmas
    )

    quantidade_alocada = 0

    for chave, variavel in variaveis.items():
        if solver.Value(
            variavel
        ) != 1:
            continue

        (
            turma_id,
            disciplina_id,
            professor_id,
            dia,
            indice
        ) = chave

        if turma_id not in grade:
            print(
                "CP-SAT -> "
                f"Turma {turma_id} não encontrada "
                "na grade vazia."
            )
            continue

        if dia not in grade[
            turma_id
        ]:
            print(
                "CP-SAT -> "
                f"Dia '{dia}' não encontrado para "
                f"a turma {turma_id}."
            )
            continue

        horarios_dia = grade[
            turma_id
        ][dia]

        if (
            indice < 0
            or indice >= len(
                horarios_dia
            )
        ):
            print(
                "CP-SAT -> "
                f"Índice {indice} inválido para "
                f"a turma {turma_id} no dia {dia}."
            )
            continue

        if horarios_dia[
            indice
        ] is not None:
            print(
                "CP-SAT -> "
                f"Conflito inesperado na turma "
                f"{turma_id}, dia {dia}, "
                f"horário {indice + 1}."
            )
            continue

        horarios_dia[
            indice
        ] = {
            "professor": professor_id,
            "disciplina": disciplina_id
        }

        quantidade_alocada += 1

    print(
        f"CP-SAT -> "
        f"{quantidade_alocada} aula(s) "
        f"alocada(s)."
    )

    return grade