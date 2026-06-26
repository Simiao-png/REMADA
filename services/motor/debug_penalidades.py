def imprimir_candidato(
    turma_id,
    disciplina_id,
    professor_id,
    dia,
    indice,
    quantidade,
    penalidade
):
    print(
        f"Turma {turma_id} | "
        f"Disciplina {disciplina_id} | "
        f"Professor {professor_id} | "
        f"{dia} aula {indice + 1} | "
        f"Qtd {quantidade} | "
        f"Penalidade {penalidade}"
    )