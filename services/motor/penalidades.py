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
    estado,
    turma_id,
    professor_id,
    disciplina_id,
    dia,
    indice,
    quantidade_aulas=1
):
    penalidade = 0

    penalidade += penalizar_disciplina_repetida_no_dia(
        estado,
        turma_id,
        disciplina_id,
        dia
    )

    penalidade += penalizar_disciplina_em_dia_consecutivo(
        estado,
        turma_id,
        disciplina_id,
        dia
    )

    penalidade += penalizar_ultimos_horarios(
        estado,
        turma_id,
        dia,
        indice,
        quantidade_aulas
    )

    penalidade += penalizar_professor_muitas_aulas_no_dia(
        estado,
        professor_id,
        dia
    )

    penalidade += penalizar_janela_professor(
        estado,
        professor_id,
        dia,
        indice,
        quantidade_aulas
    )

    penalidade += penalizar_janela_turma(
        estado,
        turma_id,
        dia,
        indice,
        quantidade_aulas
    )

    penalidade += bonificar_dia_menos_ocupado(
        estado,
        turma_id,
        dia
    )

    return penalidade


def penalizar_disciplina_repetida_no_dia(
    estado,
    turma_id,
    disciplina_id,
    dia
):
    quantidade = obter_quantidade_disciplina_no_dia(
        estado,
        turma_id,
        disciplina_id,
        dia
    )

    return (
        quantidade
        * PESO_DISCIPLINA_REPETIDA_NO_DIA
    )


def penalizar_disciplina_em_dia_consecutivo(
    estado,
    turma_id,
    disciplina_id,
    dia
):
    indice_dia = obter_indice_dia(dia)

    if indice_dia is None:
        return 0

    penalidade = 0

    dia_anterior = obter_dia_por_indice(
        indice_dia - 1
    )

    proximo_dia = obter_dia_por_indice(
        indice_dia + 1
    )

    if turma_tem_disciplina_no_dia(
        estado,
        turma_id,
        disciplina_id,
        dia_anterior
    ):
        penalidade += (
            PESO_DISCIPLINA_DIA_CONSECUTIVO
        )

    if turma_tem_disciplina_no_dia(
        estado,
        turma_id,
        disciplina_id,
        proximo_dia
    ):
        penalidade += (
            PESO_DISCIPLINA_DIA_CONSECUTIVO
        )

    return penalidade


def turma_tem_disciplina_no_dia(
    estado,
    turma_id,
    disciplina_id,
    dia
):
    if dia is None:
        return False

    grade = estado["grade"]

    if turma_id not in grade:
        return False

    if dia not in grade[turma_id]:
        return False

    quantidade = obter_quantidade_disciplina_no_dia(
        estado,
        turma_id,
        disciplina_id,
        dia
    )

    return quantidade > 0


def obter_quantidade_disciplina_no_dia(
    estado,
    turma_id,
    disciplina_id,
    dia
):
    return (
        estado["turmas"]
        .get(turma_id, {})
        .get(dia, {})
        .get("disciplinas", {})
        .get(disciplina_id, 0)
    )


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
    estado,
    turma_id,
    dia,
    indice,
    quantidade_aulas
):
    grade = estado["grade"]

    quantidade_horarios = len(
        grade[turma_id][dia]
    )

    ultimo_indice_usado = (
        indice
        + quantidade_aulas
        - 1
    )

    if ultimo_indice_usado == (
        quantidade_horarios - 1
    ):
        return PESO_ULTIMO_HORARIO

    if ultimo_indice_usado == (
        quantidade_horarios - 2
    ):
        return PESO_PENULTIMO_HORARIO

    return 0


def penalizar_professor_muitas_aulas_no_dia(
    estado,
    professor_id,
    dia
):
    horarios_ocupados = obter_horarios_professor(
        estado,
        professor_id,
        dia
    )

    quantidade = len(horarios_ocupados)

    if quantidade >= 4:
        return PESO_PROFESSOR_4_AULAS_NO_DIA

    if quantidade >= 2:
        return PESO_PROFESSOR_2_AULAS_NO_DIA

    return 0


def penalizar_janela_professor(
    estado,
    professor_id,
    dia,
    indice,
    quantidade_aulas
):
    horarios_ocupados = obter_horarios_professor(
        estado,
        professor_id,
        dia
    )

    novos_horarios = list(
        range(
            indice,
            indice + quantidade_aulas
        )
    )

    horarios_simulados = sorted(
        set(
            horarios_ocupados
            + novos_horarios
        )
    )

    if existe_janela(horarios_simulados):
        return PESO_JANELA_PROFESSOR

    return 0


def penalizar_janela_turma(
    estado,
    turma_id,
    dia,
    indice,
    quantidade_aulas
):
    horarios_ocupados = obter_horarios_turma(
        estado,
        turma_id,
        dia
    )

    novos_horarios = list(
        range(
            indice,
            indice + quantidade_aulas
        )
    )

    horarios_simulados = sorted(
        set(
            horarios_ocupados
            + novos_horarios
        )
    )

    if existe_janela(horarios_simulados):
        return PESO_JANELA_TURMA

    return 0


def obter_horarios_professor(
    estado,
    professor_id,
    dia
):
    horarios = (
        estado["professores"]
        .get(professor_id, {})
        .get(dia, set())
    )

    return list(horarios)


def obter_horarios_turma(
    estado,
    turma_id,
    dia
):
    horarios = (
        estado["turmas"]
        .get(turma_id, {})
        .get(dia, {})
        .get("horarios", set())
    )

    return list(horarios)


def existe_janela(horarios_ocupados):
    if len(horarios_ocupados) <= 1:
        return False

    primeiro = min(horarios_ocupados)
    ultimo = max(horarios_ocupados)

    for indice in range(
        primeiro,
        ultimo + 1
    ):
        if indice not in horarios_ocupados:
            return True

    return False


def bonificar_dia_menos_ocupado(
    estado,
    turma_id,
    dia
):
    grade = estado["grade"]
    ocupacoes = {}

    for dia_atual in grade[turma_id]:
        ocupacoes[dia_atual] = (
            contar_aulas_da_turma_no_dia(
                estado,
                turma_id,
                dia_atual
            )
        )

    if not ocupacoes:
        return 0

    menor_ocupacao = min(
        ocupacoes.values()
    )

    if ocupacoes[dia] == menor_ocupacao:
        return BONUS_DIA_MENOS_OCUPADO

    return 0


def contar_aulas_da_turma_no_dia(
    estado,
    turma_id,
    dia
):
    horarios_ocupados = obter_horarios_turma(
        estado,
        turma_id,
        dia
    )

    return len(horarios_ocupados)