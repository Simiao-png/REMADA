PESO_ULTIMO_HORARIO = 3
PESO_PENULTIMO_HORARIO = 1
PESO_DISCIPLINA_DIA_CONSECUTIVO = 25
PESO_PROFESSOR_2_AULAS_NO_DIA = 5
PESO_PROFESSOR_4_AULAS_NO_DIA = 15


ORDEM_DIAS = [
    "segunda",
    "terca",
    "quarta",
    "quinta",
    "sexta",
    "sabado"
]


def adicionar_objetivo(
    modelo,
    dados,
    variaveis
):
    termos_objetivo = []

    adicionar_penalidade_ultimos_horarios(
        variaveis,
        termos_objetivo
    )

    adicionar_penalidade_dias_consecutivos(
        modelo,
        variaveis,
        termos_objetivo
    )

    adicionar_penalidade_carga_diaria_professor(
        modelo,
        variaveis,
        termos_objetivo
    )

    if termos_objetivo:
        modelo.Minimize(
            sum(termos_objetivo)
        )

    return termos_objetivo


def adicionar_penalidade_ultimos_horarios(
    variaveis,
    termos_objetivo
):
    maior_indice_por_turma_dia = {}

    for chave in variaveis:
        (
            turma_id,
            _,
            _,
            dia,
            indice
        ) = chave

        chave_turma_dia = (
            turma_id,
            dia
        )

        maior_indice_atual = (
            maior_indice_por_turma_dia.get(
                chave_turma_dia,
                -1
            )
        )

        maior_indice_por_turma_dia[
            chave_turma_dia
        ] = max(
            maior_indice_atual,
            indice
        )

    for chave, variavel in variaveis.items():
        (
            turma_id,
            _,
            _,
            dia,
            indice
        ) = chave

        ultimo_indice = (
            maior_indice_por_turma_dia[
                (
                    turma_id,
                    dia
                )
            ]
        )

        if indice == ultimo_indice:
            termos_objetivo.append(
                variavel
                * PESO_ULTIMO_HORARIO
            )

        elif indice == ultimo_indice - 1:
            termos_objetivo.append(
                variavel
                * PESO_PENULTIMO_HORARIO
            )


def adicionar_penalidade_dias_consecutivos(
    modelo,
    variaveis,
    termos_objetivo
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

        chave_grupo = (
            turma_id,
            disciplina_id,
            str(dia).lower().strip()
        )

        grupos.setdefault(
            chave_grupo,
            []
        )

        grupos[chave_grupo].append(
            variavel
        )

    presencas = {}

    for chave_grupo, variaveis_dia in grupos.items():
        (
            turma_id,
            disciplina_id,
            dia
        ) = chave_grupo

        presenca = modelo.NewBoolVar(
            criar_nome(
                "presenca",
                turma_id,
                disciplina_id,
                dia
            )
        )

        modelo.Add(
            sum(variaveis_dia) >= 1
        ).OnlyEnforceIf(
            presenca
        )

        modelo.Add(
            sum(variaveis_dia) == 0
        ).OnlyEnforceIf(
            presenca.Not()
        )

        presencas[
            (
                turma_id,
                disciplina_id,
                dia
            )
        ] = presenca

    turmas_disciplinas = {
        (
            turma_id,
            disciplina_id
        )
        for (
            turma_id,
            disciplina_id,
            _
        ) in presencas
    }

    for turma_id, disciplina_id in turmas_disciplinas:
        for indice_dia in range(
            len(ORDEM_DIAS) - 1
        ):
            dia_atual = ORDEM_DIAS[
                indice_dia
            ]

            proximo_dia = ORDEM_DIAS[
                indice_dia + 1
            ]

            presenca_atual = presencas.get(
                (
                    turma_id,
                    disciplina_id,
                    dia_atual
                )
            )

            presenca_proxima = presencas.get(
                (
                    turma_id,
                    disciplina_id,
                    proximo_dia
                )
            )

            if (
                presenca_atual is None
                or presenca_proxima is None
            ):
                continue

            dias_consecutivos = modelo.NewBoolVar(
                criar_nome(
                    "consecutiva",
                    turma_id,
                    disciplina_id,
                    dia_atual,
                    proximo_dia
                )
            )

            modelo.Add(
                dias_consecutivos
                <= presenca_atual
            )

            modelo.Add(
                dias_consecutivos
                <= presenca_proxima
            )

            modelo.Add(
                dias_consecutivos
                >= presenca_atual
                + presenca_proxima
                - 1
            )

            termos_objetivo.append(
                dias_consecutivos
                * PESO_DISCIPLINA_DIA_CONSECUTIVO
            )


def adicionar_penalidade_carga_diaria_professor(
    modelo,
    variaveis,
    termos_objetivo
):
    grupos = {}

    for chave, variavel in variaveis.items():
        (
            _,
            _,
            professor_id,
            dia,
            _
        ) = chave

        chave_professor_dia = (
            professor_id,
            str(dia).lower().strip()
        )

        grupos.setdefault(
            chave_professor_dia,
            []
        )

        grupos[
            chave_professor_dia
        ].append(
            variavel
        )

    for (
        professor_id,
        dia
    ), variaveis_dia in grupos.items():
        quantidade_maxima = len(
            variaveis_dia
        )

        quantidade_aulas = modelo.NewIntVar(
            0,
            quantidade_maxima,
            criar_nome(
                "carga_professor",
                professor_id,
                dia
            )
        )

        modelo.Add(
            quantidade_aulas
            == sum(variaveis_dia)
        )

        duas_ou_mais = criar_indicador_limite(
            modelo,
            quantidade_aulas,
            limite=2,
            nome=criar_nome(
                "professor_2_aulas",
                professor_id,
                dia
            )
        )

        quatro_ou_mais = criar_indicador_limite(
            modelo,
            quantidade_aulas,
            limite=4,
            nome=criar_nome(
                "professor_4_aulas",
                professor_id,
                dia
            )
        )

        termos_objetivo.append(
            duas_ou_mais
            * PESO_PROFESSOR_2_AULAS_NO_DIA
        )

        termos_objetivo.append(
            quatro_ou_mais
            * PESO_PROFESSOR_4_AULAS_NO_DIA
        )


def criar_indicador_limite(
    modelo,
    quantidade,
    limite,
    nome
):
    indicador = modelo.NewBoolVar(
        nome
    )

    modelo.Add(
        quantidade >= limite
    ).OnlyEnforceIf(
        indicador
    )

    modelo.Add(
        quantidade <= limite - 1
    ).OnlyEnforceIf(
        indicador.Not()
    )

    return indicador


def criar_nome(
    prefixo,
    *partes
):
    partes_texto = [
        str(parte)
        for parte in partes
    ]

    return (
        prefixo
        + "_"
        + "_".join(partes_texto)
    )