def criar_grade_vazia(configuracao, turmas):
    grade = {}

    dias = [
        "segunda",
        "terca",
        "quarta",
        "quinta",
        "sexta"
    ]

    for turma_id in turmas:

        grade[turma_id] = {}

        for dia in dias:
            grade[turma_id][dia] = [
                None
                for _ in range(configuracao.aulas_por_dia)
            ]

    return grade