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
        if solver.Value(variavel) != 1:
            continue

        (
            turma_id,
            disciplina_id,
            professor_id,
            dia,
            indice
        ) = chave

        if turma_id not in grade:
            continue

        if dia not in grade[turma_id]:
            continue

        if indice >= len(
            grade[turma_id][dia]
        ):
            continue

        grade[turma_id][dia][indice] = {
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