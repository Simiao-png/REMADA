from services.motor.estado import (
    professor_livre
)


def professor_disponivel(
    disponibilidades,
    professor_id,
    dia,
    indice_horario
):
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


def limite_disciplina_por_dia(
    estado,
    turma_id,
    disciplina_id,
    dia,
    limite=2
):
    quantidade = (
        estado["turmas"]
        .get(turma_id, {})
        .get(dia, {})
        .get("disciplinas", {})
        .get(disciplina_id, 0)
    )

    return quantidade < limite


def validar_alocacao_aula(
    estado,
    disponibilidades,
    turma_id,
    professor_id,
    disciplina_id,
    dia,
    indice_horario
):
    grade = estado["grade"]

    if grade[turma_id][dia][indice_horario] is not None:
        return {
            "valido": False,
            "motivo": "turma_ocupada"
        }

    if not professor_livre(
        estado,
        professor_id,
        dia,
        indice_horario
    ):
        return {
            "valido": False,
            "motivo": "professor_ocupado"
        }

    if not professor_disponivel(
        disponibilidades,
        professor_id,
        dia,
        indice_horario
    ):
        return {
            "valido": False,
            "motivo": "professor_indisponivel"
        }

    if not limite_disciplina_por_dia(
        estado,
        turma_id,
        disciplina_id,
        dia
    ):
        return {
            "valido": False,
            "motivo": "limite_disciplina_dia"
        }

    return {
        "valido": True,
        "motivo": None
    }


def pode_alocar_aula(
    estado,
    disponibilidades,
    turma_id,
    professor_id,
    disciplina_id,
    dia,
    indice_horario
):
    validacao = validar_alocacao_aula(
        estado,
        disponibilidades,
        turma_id,
        professor_id,
        disciplina_id,
        dia,
        indice_horario
    )

    return validacao["valido"]


def validar_alocacao_dupla(
    estado,
    disponibilidades,
    turma_id,
    professor_id,
    disciplina_id,
    dia,
    indice_horario
):
    grade = estado["grade"]
    horarios = grade[turma_id][dia]

    segundo_indice = indice_horario + 1

    if segundo_indice >= len(horarios):
        return {
            "valido": False,
            "motivo": "sem_espaco_para_dupla"
        }

    if horarios[indice_horario] is not None:
        return {
            "valido": False,
            "motivo": "turma_ocupada"
        }

    if horarios[segundo_indice] is not None:
        return {
            "valido": False,
            "motivo": "turma_ocupada"
        }

    quantidade_disciplina = (
        estado["turmas"]
        .get(turma_id, {})
        .get(dia, {})
        .get("disciplinas", {})
        .get(disciplina_id, 0)
    )

    if quantidade_disciplina + 2 > 2:
        return {
            "valido": False,
            "motivo": "limite_disciplina_dia"
        }

    for indice in [
        indice_horario,
        segundo_indice
    ]:
        if not professor_livre(
            estado,
            professor_id,
            dia,
            indice
        ):
            return {
                "valido": False,
                "motivo": "professor_ocupado"
            }

        if not professor_disponivel(
            disponibilidades,
            professor_id,
            dia,
            indice
        ):
            return {
                "valido": False,
                "motivo": "professor_indisponivel"
            }

    return {
        "valido": True,
        "motivo": None
    }


def pode_alocar_dupla(
    estado,
    disponibilidades,
    turma_id,
    professor_id,
    disciplina_id,
    dia,
    indice_horario
):
    validacao = validar_alocacao_dupla(
        estado,
        disponibilidades,
        turma_id,
        professor_id,
        disciplina_id,
        dia,
        indice_horario
    )

    return validacao["valido"]