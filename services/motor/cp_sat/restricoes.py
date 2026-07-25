def adicionar_restricoes(
    modelo,
    dados,
    variaveis
):
    adicionar_carga_horaria_semanal(
        modelo,
        dados,
        variaveis
    )

    adicionar_limite_por_horario_da_turma(
        modelo,
        variaveis
    )

    adicionar_limite_por_horario_do_professor(
        modelo,
        variaveis
    )

    adicionar_disponibilidade_professor(
        modelo,
        dados,
        variaveis
    )

    adicionar_limite_disciplina_por_dia(
        modelo,
        variaveis
    )


def adicionar_carga_horaria_semanal(
    modelo,
    dados,
    variaveis
):
    matrizes = dados.get(
        "turma_disciplina",
        []
    )

    for matriz in matrizes:
        turma_id = obter_valor(
            matriz,
            "turma_id"
        )

        disciplina_id = obter_valor(
            matriz,
            "disciplina_id"
        )

        aulas_por_semana = int(
            obter_valor(
                matriz,
                "aulas_por_semana"
            )
            or 0
        )

        variaveis_da_matriz = []

        for chave, variavel in variaveis.items():
            (
                chave_turma,
                chave_disciplina,
                _,
                _,
                _
            ) = chave

            if chave_turma != turma_id:
                continue

            if chave_disciplina != disciplina_id:
                continue

            variaveis_da_matriz.append(
                variavel
            )

        if not variaveis_da_matriz:
            continue

        modelo.Add(
            sum(variaveis_da_matriz)
            == aulas_por_semana
        )


def adicionar_limite_por_horario_da_turma(
    modelo,
    variaveis
):
    grupos = {}

    for chave, variavel in variaveis.items():
        (
            turma_id,
            _,
            _,
            dia,
            indice
        ) = chave

        chave_horario = (
            turma_id,
            dia,
            indice
        )

        grupos.setdefault(
            chave_horario,
            []
        )

        grupos[chave_horario].append(
            variavel
        )

    for variaveis_horario in grupos.values():
        modelo.Add(
            sum(variaveis_horario) <= 1
        )


def adicionar_limite_por_horario_do_professor(
    modelo,
    variaveis
):
    grupos = {}

    for chave, variavel in variaveis.items():
        (
            _,
            _,
            professor_id,
            dia,
            indice
        ) = chave

        chave_horario = (
            professor_id,
            dia,
            indice
        )

        grupos.setdefault(
            chave_horario,
            []
        )

        grupos[chave_horario].append(
            variavel
        )

    for variaveis_horario in grupos.values():
        modelo.Add(
            sum(variaveis_horario) <= 1
        )


def adicionar_disponibilidade_professor(
    modelo,
    dados,
    variaveis
):
    disponibilidades = dados.get(
        "disponibilidades",
        []
    )

    horarios_disponiveis = set()

    for disponibilidade in disponibilidades:
        disponivel = obter_valor(
            disponibilidade,
            "disponivel"
        )

        if not disponivel:
            continue

        professor_id = obter_valor(
            disponibilidade,
            "professor_id"
        )

        dia = obter_valor(
            disponibilidade,
            "dia_semana"
        )

        numero_aula = obter_valor(
            disponibilidade,
            "numero_aula"
        )

        if numero_aula is None:
            continue

        horarios_disponiveis.add(
            (
                professor_id,
                dia,
                int(numero_aula) - 1
            )
        )

    for chave, variavel in variaveis.items():
        (
            _,
            _,
            professor_id,
            dia,
            indice
        ) = chave

        horario_professor = (
            professor_id,
            dia,
            indice
        )

        if horario_professor not in horarios_disponiveis:
            modelo.Add(
                variavel == 0
            )


def adicionar_limite_disciplina_por_dia(
    modelo,
    variaveis,
    limite=2
):
    grupos = {}

    for chave, variavel in variaveis.items():
        (
            turma_id,
            disciplina_id,
            _,
            dia,
            _
        ) = chave

        chave_disciplina_dia = (
            turma_id,
            disciplina_id,
            dia
        )

        grupos.setdefault(
            chave_disciplina_dia,
            []
        )

        grupos[
            chave_disciplina_dia
        ].append(
            variavel
        )

    for variaveis_disciplina in grupos.values():
        modelo.Add(
            sum(variaveis_disciplina)
            <= limite
        )


def obter_valor(
    objeto,
    atributo
):
    if isinstance(objeto, dict):
        return objeto.get(atributo)

    return getattr(
        objeto,
        atributo,
        None
    )