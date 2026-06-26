def professor_livre_na_grade(grade, professor_id, dia, indice_horario):

    for turma_id, dias in grade.items():

        aula = dias[dia][indice_horario]

        if aula is None:
            continue

        if aula["professor"] == professor_id:
            return False

    return True


def professor_disponivel(disponibilidades, professor_id, dia, indice_horario):

    numero_aula = indice_horario + 1

    for disponibilidade in disponibilidades:

        if disponibilidade.professor_id != professor_id:
            continue

        if disponibilidade.dia_semana != dia:
            continue

        if disponibilidade.numero_aula != numero_aula:
            continue

        return disponibilidade.disponivel

    return False


def limite_disciplina_por_dia(grade, turma_id, disciplina_id, dia, limite=2):

    quantidade = 0

    for aula in grade[turma_id][dia]:

        if aula is None:
            continue

        if aula["disciplina"] == disciplina_id:
            quantidade += 1

    return quantidade < limite


def pode_alocar_aula(
    grade,
    disponibilidades,
    turma_id,
    professor_id,
    disciplina_id,
    dia,
    indice_horario
):

    if grade[turma_id][dia][indice_horario] is not None:
        return False

    if not professor_livre_na_grade(
        grade,
        professor_id,
        dia,
        indice_horario
    ):
        return False

    if not professor_disponivel(
        disponibilidades,
        professor_id,
        dia,
        indice_horario
    ):
        return False

    if not limite_disciplina_por_dia(
        grade,
        turma_id,
        disciplina_id,
        dia
    ):
        return False

    return True


def pode_alocar_dupla(
    grade,
    disponibilidades,
    turma_id,
    professor_id,
    disciplina_id,
    dia,
    indice_horario
):

    horarios = grade[turma_id][dia]

    if indice_horario + 1 >= len(horarios):
        return False

    return (
        pode_alocar_aula(
            grade,
            disponibilidades,
            turma_id,
            professor_id,
            disciplina_id,
            dia,
            indice_horario
        )
        and
        pode_alocar_aula(
            grade,
            disponibilidades,
            turma_id,
            professor_id,
            disciplina_id,
            dia,
            indice_horario + 1
        )
    )