PESO_ULTIMO_HORARIO = 3
PESO_PENULTIMO_HORARIO = 1

# Penalidade moderada para evitar que uma disciplina
# apareça em dias consecutivos quando houver alternativa.
PESO_DISCIPLINA_DIA_CONSECUTIVO = 6

# Penalidades progressivas para concentração excessiva
# de aulas do mesmo professor no mesmo dia.
PESO_EXCESSO_PROFESSOR_ACIMA_4 = 4
PESO_EXCESSO_PROFESSOR_ACIMA_6 = 12


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
    """
    Adiciona preferências de qualidade à grade.

    Essas regras não tornam o modelo inviável.
    Elas apenas orientam o CP-SAT a escolher,
    entre as soluções válidas, a grade com menor
    custo total.
    """
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
    """
    Dá preferência aos primeiros horários do dia.

    A última aula recebe penalidade maior e a
    penúltima recebe penalidade menor.
    """
    maior_indice_por_turma_dia = {}

    for chave in variaveis:
        (
            turma_id,
            _,
            _,
            dia,
            indice
        ) = chave

        dia_normalizado = normalizar_dia(
            dia
        )

        chave_turma_dia = (
            turma_id,
            dia_normalizado
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

        dia_normalizado = normalizar_dia(
            dia
        )

        ultimo_indice = (
            maior_indice_por_turma_dia[
                (
                    turma_id,
                    dia_normalizado
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
    """
    Penaliza a presença da mesma disciplina,
    para a mesma turma, em dois dias consecutivos.

    É uma preferência, não uma proibição.
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

        dia_normalizado = normalizar_dia(
            dia
        )

        chave_grupo = (
            turma_id,
            disciplina_id,
            dia_normalizado
        )

        grupos.setdefault(
            chave_grupo,
            []
        ).append(
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

    for turma_id, disciplina_id in (
        turmas_disciplinas
    ):
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

            dias_consecutivos = (
                modelo.NewBoolVar(
                    criar_nome(
                        "consecutiva",
                        turma_id,
                        disciplina_id,
                        dia_atual,
                        proximo_dia
                    )
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
    """
    Penaliza somente concentração excessiva.

    Duas, três ou quatro aulas no mesmo dia são
    consideradas normais e não recebem penalidade.

    A partir da quinta aula, o custo cresce de forma
    progressiva. Acima da sexta aula, a penalidade
    adicional é maior.
    """
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
            normalizar_dia(dia)
        )

        grupos.setdefault(
            chave_professor_dia,
            []
        ).append(
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

        excesso_acima_4 = criar_excesso_limite(
            modelo,
            quantidade_aulas,
            limite=4,
            quantidade_maxima=quantidade_maxima,
            nome=criar_nome(
                "excesso_professor_acima_4",
                professor_id,
                dia
            )
        )

        excesso_acima_6 = criar_excesso_limite(
            modelo,
            quantidade_aulas,
            limite=6,
            quantidade_maxima=quantidade_maxima,
            nome=criar_nome(
                "excesso_professor_acima_6",
                professor_id,
                dia
            )
        )

        termos_objetivo.append(
            excesso_acima_4
            * PESO_EXCESSO_PROFESSOR_ACIMA_4
        )

        termos_objetivo.append(
            excesso_acima_6
            * PESO_EXCESSO_PROFESSOR_ACIMA_6
        )


def criar_excesso_limite(
    modelo,
    quantidade,
    limite,
    quantidade_maxima,
    nome
):
    """
    Cria uma variável equivalente a:

        max(0, quantidade - limite)

    Assim, quanto maior o excesso, maior a penalidade.
    """
    diferenca = modelo.NewIntVar(
        -limite,
        quantidade_maxima - limite,
        f"{nome}_diferenca"
    )

    modelo.Add(
        diferenca
        == quantidade - limite
    )

    excesso = modelo.NewIntVar(
        0,
        max(
            quantidade_maxima - limite,
            0
        ),
        nome
    )

    modelo.AddMaxEquality(
        excesso,
        [
            diferenca,
            0
        ]
    )

    return excesso


def normalizar_dia(
    dia
):
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
        + "_".join(
            partes_texto
        )
    )