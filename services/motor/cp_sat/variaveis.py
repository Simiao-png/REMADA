from services.motor.estrutura import (
    buscar_configuracao_turma,
    obter_dias_configuracao
)


def criar_variaveis(
    modelo,
    dados
):
    variaveis = {}

    turmas = dados.get(
        "turmas",
        []
    )

    turma_disciplina = dados.get(
        "turma_disciplina",
        []
    )

    professor_turma = dados.get(
        "professor_turma",
        []
    )

    configuracoes = dados.get(
        "configuracoes",
        []
    )

    turmas_por_id = {
        obter_valor(turma, "id"): turma
        for turma in turmas
    }

    professores_por_atribuicao = (
        criar_professores_por_atribuicao(
            professor_turma
        )
    )

    horarios_por_turma = (
        criar_horarios_por_turma(
            turmas_por_id,
            configuracoes
        )
    )

    for matriz in turma_disciplina:
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

        professores_validos = (
            professores_por_atribuicao.get(
                (
                    turma_id,
                    disciplina_id
                ),
                set()
            )
        )

        horarios_turma = (
            horarios_por_turma.get(
                turma_id,
                {}
            )
        )

        for professor_id in professores_validos:
            for dia, quantidade_aulas in (
                horarios_turma.items()
            ):
                for indice in range(
                    quantidade_aulas
                ):
                    chave = (
                        turma_id,
                        disciplina_id,
                        professor_id,
                        dia,
                        indice
                    )

                    nome = (
                        f"aula_"
                        f"t{turma_id}_"
                        f"d{disciplina_id}_"
                        f"p{professor_id}_"
                        f"{dia}_"
                        f"h{indice}"
                    )

                    variaveis[chave] = (
                        modelo.NewBoolVar(
                            nome
                        )
                    )

    print(
        f"CP-SAT -> "
        f"{len(variaveis)} variável(is) criada(s)."
    )

    return variaveis


def criar_professores_por_atribuicao(
    vinculos
):
    """
    Agrupa os professores pela atribuição completa:

    turma + disciplina -> professores

    ProfessorTurma já representa diretamente:
    professor_id + turma_id + disciplina_id.
    """
    professores_por_atribuicao = {}

    for vinculo in vinculos:
        turma_id = obter_valor(
            vinculo,
            "turma_id"
        )

        disciplina_id = obter_valor(
            vinculo,
            "disciplina_id"
        )

        professor_id = obter_valor(
            vinculo,
            "professor_id"
        )

        if (
            turma_id is None
            or disciplina_id is None
            or professor_id is None
        ):
            continue

        chave_atribuicao = (
            turma_id,
            disciplina_id
        )

        professores_por_atribuicao.setdefault(
            chave_atribuicao,
            set()
        ).add(
            professor_id
        )

    return professores_por_atribuicao


def criar_horarios_por_turma(
    turmas,
    configuracoes
):
    horarios_por_turma = {}

    for turma_id, turma in turmas.items():
        configuracao = (
            buscar_configuracao_turma(
                turma,
                configuracoes
            )
        )

        quantidade_aulas_padrao = (
            obter_quantidade_aulas_padrao(
                turma
            )
        )

        dias_padrao = [
            "segunda",
            "terca",
            "quarta",
            "quinta",
            "sexta"
        ]

        if configuracao is not None:
            quantidade_aulas = int(
                obter_valor(
                    configuracao,
                    "aulas_por_dia"
                )
                or quantidade_aulas_padrao
            )

            dias = obter_dias_configuracao(
                configuracao
            )

            if not dias:
                dias = dias_padrao

        else:
            quantidade_aulas = (
                quantidade_aulas_padrao
            )

            dias = dias_padrao

        if quantidade_aulas <= 0:
            quantidade_aulas = (
                quantidade_aulas_padrao
            )

        horarios_por_turma[
            turma_id
        ] = {
            normalizar_dia(dia):
                quantidade_aulas
            for dia in dias
            if normalizar_dia(dia)
        }

    return horarios_por_turma


def obter_quantidade_aulas_padrao(
    turma
):
    segmento = str(
        obter_valor(
            turma,
            "segmento"
        )
        or ""
    ).lower()

    if (
        "médio" in segmento
        or "medio" in segmento
        or "ensino_medio" in segmento
    ):
        return 7

    return 6


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


def obter_valor(
    objeto,
    atributo
):
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