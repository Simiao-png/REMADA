def obter_valor(
    objeto,
    atributo
):
    """
    Extrai valores de dicionários ou objetos SQLAlchemy.
    """
    if objeto is None:
        return None

    if isinstance(
        objeto,
        dict
    ):
        return objeto.get(
            atributo
        )

    return getattr(
        objeto,
        atributo,
        None
    )


def normalizar_dia(
    dia
):
    """
    Normaliza os dias da semana para o padrão usado pelo motor.
    """
    if dia is None:
        return ""

    valor = str(
        dia
    ).lower().strip()

    mapa = {
        "1": "segunda",
        "segunda": "segunda",
        "segunda-feira": "segunda",

        "2": "terca",
        "terca": "terca",
        "terça": "terca",
        "terca-feira": "terca",
        "terça-feira": "terca",

        "3": "quarta",
        "quarta": "quarta",
        "quarta-feira": "quarta",

        "4": "quinta",
        "quinta": "quinta",
        "quinta-feira": "quinta",

        "5": "sexta",
        "sexta": "sexta",
        "sexta-feira": "sexta",

        "6": "sabado",
        "sabado": "sabado",
        "sábado": "sabado",
        "sabado-feira": "sabado"
    }

    return mapa.get(
        valor,
        valor
    )


def adicionar_restricoes(
    modelo,
    dados,
    variaveis
):
    """
    Aplica todas as restrições obrigatórias do modelo CP-SAT.
    """
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

    adicionar_limite_semanal_professor(
        modelo,
        dados,
        variaveis
    )

    adicionar_limite_disciplina_por_dia(
        modelo,
        variaveis,
        limite=2
    )


def adicionar_carga_horaria_semanal(
    modelo,
    dados,
    variaveis
):
    """
    Garante que cada turma cumpra exatamente a quantidade
    semanal definida para cada disciplina na matriz curricular.

    Se não existir variável para uma disciplina com carga positiva,
    o modelo se torna inviável, como deve ocorrer quando não há
    professor atribuído ou horário possível.
    """
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

        if aulas_por_semana <= 0:
            continue

        variaveis_da_matriz = [
            variavel
            for chave, variavel in variaveis.items()
            if (
                chave[0] == turma_id
                and chave[1] == disciplina_id
            )
        ]

        modelo.Add(
            sum(variaveis_da_matriz)
            == aulas_por_semana
        )


def adicionar_limite_por_horario_da_turma(
    modelo,
    variaveis
):
    """
    Impede que uma turma receba mais de uma aula
    no mesmo dia e horário.
    """
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
            normalizar_dia(dia),
            indice
        )

        grupos.setdefault(
            chave_horario,
            []
        ).append(
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
    """
    Impede que um professor lecione em mais de uma turma
    no mesmo dia e horário.
    """
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
            normalizar_dia(dia),
            indice
        )

        grupos.setdefault(
            chave_horario,
            []
        ).append(
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
    """
    Permite alocações somente nos horários marcados como disponíveis.

    Professor com aulas atribuídas e sem disponibilidade cadastrada
    fica sem horários possíveis, tornando o modelo inviável.
    """
    disponibilidades = dados.get(
        "disponibilidades",
        []
    )

    horarios_disponiveis = set()

    for disponibilidade in disponibilidades:
        if not obter_valor(
            disponibilidade,
            "disponivel"
        ):
            continue

        professor_id = obter_valor(
            disponibilidade,
            "professor_id"
        )

        dia = normalizar_dia(
            obter_valor(
                disponibilidade,
                "dia_semana"
            )
        )

        numero_aula = obter_valor(
            disponibilidade,
            "numero_aula"
        )

        if (
            professor_id is None
            or not dia
            or numero_aula is None
        ):
            continue

        try:
            indice_aula = int(
                numero_aula
            ) - 1
        except (
            TypeError,
            ValueError
        ):
            continue

        if indice_aula < 0:
            continue

        horarios_disponiveis.add(
            (
                professor_id,
                dia,
                indice_aula
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
            normalizar_dia(dia),
            indice
        )

        if (
            horario_professor
            not in horarios_disponiveis
        ):
            modelo.Add(
                variavel == 0
            )


def adicionar_limite_semanal_professor(
    modelo,
    dados,
    variaveis
):
    """
    Garante que o total semanal de aulas de cada professor
    não ultrapasse professor.limite_aulas_semana.

    Limite None, vazio ou menor ou igual a zero é tratado como
    não configurado e não cria restrição rígida. O diagnóstico
    pode informar essa situação separadamente.
    """
    professores = dados.get(
        "professores",
        []
    )

    variaveis_por_professor = {}

    for chave, variavel in variaveis.items():
        professor_id = chave[2]

        variaveis_por_professor.setdefault(
            professor_id,
            []
        ).append(
            variavel
        )

    for professor in professores:
        professor_id = obter_valor(
            professor,
            "id"
        )

        limite = obter_valor(
            professor,
            "limite_aulas_semana"
        )

        if limite in (
            None,
            ""
        ):
            continue

        try:
            limite = int(
                limite
            )
        except (
            TypeError,
            ValueError
        ):
            continue

        if limite <= 0:
            continue

        variaveis_professor = (
            variaveis_por_professor.get(
                professor_id,
                []
            )
        )

        if not variaveis_professor:
            continue

        modelo.Add(
            sum(variaveis_professor)
            <= limite
        )


def adicionar_limite_disciplina_por_dia(
    modelo,
    variaveis,
    limite=2
):
    """
    Limita a quantidade de aulas da mesma disciplina,
    para a mesma turma, em um único dia.

    O padrão de 2 permite uma aula dupla, mas impede
    uma terceira aula da mesma disciplina no mesmo dia.
    """
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
            normalizar_dia(dia)
        )

        grupos.setdefault(
            chave_disciplina_dia,
            []
        ).append(
            variavel
        )

    for variaveis_disciplina in grupos.values():
        modelo.Add(
            sum(variaveis_disciplina)
            <= limite
        )