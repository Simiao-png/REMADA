def criar_fila_aulas(
    turmas_disciplinas,
    professores_turmas
):
    fila = []

    mapa_professores = {
        (
            vinculo.turma_id,
            vinculo.disciplina_id
        ): vinculo.professor_id
        for vinculo in professores_turmas
    }

    matrizes_ordenadas = sorted(
        turmas_disciplinas,
        key=lambda matriz: (
            -int(matriz.aulas_por_semana or 0),
            matriz.turma_id,
            matriz.disciplina_id
        )
    )

    for matriz in matrizes_ordenadas:
        quantidade_aulas = int(
            matriz.aulas_por_semana or 0
        )

        if quantidade_aulas <= 0:
            continue

        professor_id = mapa_professores.get(
            (
                matriz.turma_id,
                matriz.disciplina_id
            )
        )

        for _ in range(quantidade_aulas):
            fila.append({
                "turma_id": matriz.turma_id,
                "disciplina_id": matriz.disciplina_id,
                "professor_id": professor_id,

                # Por enquanto, disciplinas com duas ou mais
                # aulas semanais podem formar aula dupla.
                "permite_aula_dupla": (
                    quantidade_aulas >= 2
                ),

                "permite_aula_tripla": False,

                "exige_distribuicao_semanal": (
                    quantidade_aulas >= 3
                ),

                "quantidade_minima_dias_semana": min(
                    quantidade_aulas,
                    3
                )
            })

    return fila