def criar_estado(grade):
    return {
        "grade": grade,
        "professores": {},
        "turmas": {}
    }


def registrar_aula(
    estado,
    turma_id,
    professor_id,
    disciplina_id,
    dia,
    indice
):
    professores = estado["professores"]
    turmas = estado["turmas"]

    professores.setdefault(professor_id, {})
    professores[professor_id].setdefault(dia, set())
    professores[professor_id][dia].add(indice)

    turmas.setdefault(turma_id, {})
    turmas[turma_id].setdefault(
        dia,
        {
            "horarios": set(),
            "disciplinas": {}
        }
    )

    turmas[turma_id][dia]["horarios"].add(indice)

    disciplinas = (
        turmas[turma_id][dia]["disciplinas"]
    )

    disciplinas[disciplina_id] = (
        disciplinas.get(disciplina_id, 0) + 1
    )


def remover_aula(
    estado,
    turma_id,
    professor_id,
    disciplina_id,
    dia,
    indice
):
    professores = estado["professores"]
    turmas = estado["turmas"]

    if professor_id in professores:
        if dia in professores[professor_id]:
            professores[professor_id][dia].discard(indice)

            if not professores[professor_id][dia]:
                del professores[professor_id][dia]

        if not professores[professor_id]:
            del professores[professor_id]

    if turma_id not in turmas:
        return

    if dia not in turmas[turma_id]:
        return

    dados_dia = turmas[turma_id][dia]

    dados_dia["horarios"].discard(indice)

    disciplinas = dados_dia["disciplinas"]

    if disciplina_id in disciplinas:
        disciplinas[disciplina_id] -= 1

        if disciplinas[disciplina_id] <= 0:
            del disciplinas[disciplina_id]

    if (
        not dados_dia["horarios"]
        and not dados_dia["disciplinas"]
    ):
        del turmas[turma_id][dia]

    if not turmas[turma_id]:
        del turmas[turma_id]


def professor_livre(
    estado,
    professor_id,
    dia,
    indice
):
    horarios_ocupados = (
        estado["professores"]
        .get(professor_id, {})
        .get(dia, set())
    )

    return indice not in horarios_ocupados