def ordenar_dias_por_menor_ocupacao(
    estado,
    turma_id
):
    grade = estado["grade"]

    dias = list(
        grade[turma_id].keys()
    )

    dias.sort(
        key=lambda dia: (
            len(
                estado["turmas"]
                .get(turma_id, {})
                .get(dia, {})
                .get("horarios", set())
            )
        )
    )

    return dias