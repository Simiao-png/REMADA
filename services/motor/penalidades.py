# Pesos das penalidades
PESO_DISCIPLINA_REPETIDA_NO_DIA = 10
PESO_ULTIMO_HORARIO = 3
PESO_PENULTIMO_HORARIO = 1
PESO_PROFESSOR_2_AULAS_NO_DIA = 5
PESO_PROFESSOR_4_AULAS_NO_DIA = 15
PESO_JANELA_PROFESSOR = 50
PESO_JANELA_TURMA = 40
PESO_DISCIPLINA_DIA_CONSECUTIVO = 25

# Bônus
BONUS_DIA_MENOS_OCUPADO = -2


ORDEM_DIAS = [
    "segunda",
    "terca",
    "quarta",
    "quinta",
    "sexta",
    "sabado"
]


def calcular_penalidade(
    grade,
    turma_id,
    professor_id,
    disciplina_id,
    dia,
    indice,
    quantidade_aulas=1
):
    penalidade = 0

    penalidade += penalizar_disciplina_repetida_no_dia(
        grade,
        turma_id,
        disciplina_id,
        dia
    )

    penalidade += penalizar_disciplina_em_dia_consecutivo(
        grade,
        turma_id,
        disciplina_id,
        dia
    )

    penalidade += penalizar_ultimos_horarios(
        grade,
        turma_id,
        dia,
        indice,
        quantidade_aulas
    )

    penalidade += penalizar_professor_muitas_aulas_no_dia(
        grade,
        professor_id,
        dia
    )

    penalidade += penalizar_janela_professor(
        grade,
        professor_id,
        dia,
        indice,
        quantidade_aulas
    )

    penalidade += penalizar_janela_turma(
        grade,
        turma_id,
        dia,
        indice,
        quantidade_aulas
    )

    penalidade += bonificar_dia_menos_ocupado(
        grade,
        turma_id,
        dia
    )

    return penalidade


def penalizar_disciplina_repetida_no_dia(
    grade,
    turma_id,
    disciplina_id,
    dia
):
    penalidade = 0

    for aula in grade[turma_id][dia]:
        if aula is not None and aula["disciplina"] == disciplina_id:
            penalidade += PESO_DISCIPLINA_REPETIDA_NO_DIA

    return penalidade


def penalizar_disciplina_em_dia_consecutivo(
    grade,
    turma_id,
    disciplina_id,
    dia
):
    indice_dia = obter_indice_dia(dia)

    if indice_dia is None:
        return 0

    penalidade = 0

    dia_anterior = obter_dia_por_indice(indice_dia - 1)
    proximo_dia = obter_dia_por_indice(indice_dia + 1)

    if dia_anterior in grade[turma_id]:
        if turma_tem_disciplina_no_dia(
            grade,
            turma_id,
            disciplina_id,
            dia_anterior
        ):
            penalidade += PESO_DISCIPLINA_DIA_CONSECUTIVO

    if proximo_dia in grade[turma_id]:
        if turma_tem_disciplina_no_dia(
            grade,
            turma_id,
            disciplina_id,
            proximo_dia
        ):
            penalidade += PESO_DISCIPLINA_DIA_CONSECUTIVO

    return penalidade


def turma_tem_disciplina_no_dia(
    grade,
    turma_id,
    disciplina_id,
    dia
):
    for aula in grade[turma_id][dia]:
        if aula is not None and aula["disciplina"] == disciplina_id:
            return True

    return False


def obter_indice_dia(dia):
    if dia not in ORDEM_DIAS:
        return None

    return ORDEM_DIAS.index(dia)


def obter_dia_por_indice(indice):
    if indice < 0:
        return None

    if indice >= len(ORDEM_DIAS):
        return None

    return ORDEM_DIAS[indice]


def penalizar_ultimos_horarios(
    grade,
    turma_id,
    dia,
    indice,
    quantidade_aulas
):
    quantidade_horarios = len(grade[turma_id][dia])
    ultimo_indice_usado = indice + quantidade_aulas - 1

    if ultimo_indice_usado == quantidade_horarios - 1:
        return PESO_ULTIMO_HORARIO

    if ultimo_indice_usado == quantidade_horarios - 2:
        return PESO_PENULTIMO_HORARIO

    return 0


def penalizar_professor_muitas_aulas_no_dia(
    grade,
    professor_id,
    dia
):
    quantidade = 0

    for turma_id in grade:
        for aula in grade[turma_id][dia]:
            if aula is not None and aula["professor"] == professor_id:
                quantidade += 1

    if quantidade >= 4:
        return PESO_PROFESSOR_4_AULAS_NO_DIA

    if quantidade >= 2:
        return PESO_PROFESSOR_2_AULAS_NO_DIA

    return 0


def penalizar_janela_professor(
    grade,
    professor_id,
    dia,
    indice,
    quantidade_aulas
):
    horarios_ocupados = []

    for turma_id in grade:
        for i, aula in enumerate(grade[turma_id][dia]):
            if aula is not None and aula["professor"] == professor_id:
                horarios_ocupados.append(i)

    novos_horarios = list(range(indice, indice + quantidade_aulas))

    horarios_ocupados.extend(novos_horarios)
    horarios_ocupados = sorted(set(horarios_ocupados))

    if existe_janela(horarios_ocupados):
        return PESO_JANELA_PROFESSOR

    return 0


def penalizar_janela_turma(
    grade,
    turma_id,
    dia,
    indice,
    quantidade_aulas
):
    horarios_ocupados = []

    for i, aula in enumerate(grade[turma_id][dia]):
        if aula is not None:
            horarios_ocupados.append(i)

    novos_horarios = list(range(indice, indice + quantidade_aulas))

    horarios_ocupados.extend(novos_horarios)
    horarios_ocupados = sorted(set(horarios_ocupados))

    if existe_janela(horarios_ocupados):
        return PESO_JANELA_TURMA

    return 0


def existe_janela(horarios_ocupados):
    if len(horarios_ocupados) <= 1:
        return False

    primeiro = min(horarios_ocupados)
    ultimo = max(horarios_ocupados)

    for i in range(primeiro, ultimo + 1):
        if i not in horarios_ocupados:
            return True

    return False


def bonificar_dia_menos_ocupado(
    grade,
    turma_id,
    dia
):
    ocupacoes = {}

    for dia_atual in grade[turma_id]:
        ocupacoes[dia_atual] = contar_aulas_da_turma_no_dia(
            grade,
            turma_id,
            dia_atual
        )

    menor_ocupacao = min(ocupacoes.values())

    if ocupacoes[dia] == menor_ocupacao:
        return BONUS_DIA_MENOS_OCUPADO

    return 0


def contar_aulas_da_turma_no_dia(
    grade,
    turma_id,
    dia
):
    total = 0

    for aula in grade[turma_id][dia]:
        if aula is not None:
            total += 1

    return total