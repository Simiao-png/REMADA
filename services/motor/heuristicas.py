def ordenar_dias_por_menor_ocupacao(grade, turma_id):

    dias = list(grade[turma_id].keys())

    dias.sort(
        key=lambda dia: sum(
            1 for aula in grade[turma_id][dia] if aula is not None
        )
    )

    return dias