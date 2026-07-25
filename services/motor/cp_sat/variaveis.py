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

    professor_disciplina = dados.get(
        "professor_disciplina",
        []
    )

    configuracoes = dados.get(
        "configuracoes",
        []
    )

    turmas_por_id = {
        turma.id: turma
        for turma in turmas
    }

    professores_por_turma = (
        criar_professores_por_turma(
            professor_turma
        )
    )

    professores_por_disciplina = (
        criar_professores_por_disciplina(
            professor_disciplina
        )
    )

    horarios_por_turma = criar_horarios_por_turma(
        turmas_por_id,
        configuracoes
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

        professores_turma = (
            professores_por_turma.get(
                turma_id,
                set()
            )
        )

        professores_disciplina = (
            professores_por_disciplina.get(
                disciplina_id,
                set()
            )
        )

        professores_validos = (
            professores_turma
            & professores_disciplina
        )

        horarios_turma = horarios_por_turma.get(
            turma_id,
            {}
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


def criar_professores_por_turma(
    vinculos
):
    professores_por_turma = {}

    for vinculo in vinculos:
        turma_id = obter_valor(
            vinculo,
            "turma_id"
        )

        professor_id = obter_valor(
            vinculo,
            "professor_id"
        )

        professores_por_turma.setdefault(
            turma_id,
            set()
        ).add(
            professor_id
        )

    return professores_por_turma


def criar_professores_por_disciplina(
    vinculos
):
    professores_por_disciplina = {}

    for vinculo in vinculos:
        disciplina_id = obter_valor(
            vinculo,
            "disciplina_id"
        )

        professor_id = obter_valor(
            vinculo,
            "professor_id"
        )

        professores_por_disciplina.setdefault(
            disciplina_id,
            set()
        ).add(
            professor_id
        )

    return professores_por_disciplina


def criar_horarios_por_turma(
    turmas,
    configuracoes
):
    horarios_por_turma = {}

    for turma_id, turma in turmas.items():
        configuracao = buscar_configuracao_turma(
            turma,
            configuracoes
        )

        if configuracao is None:
            continue

        quantidade_aulas = int(
            obter_valor(
                configuracao,
                "aulas_por_dia"
            )
            or 0
        )

        if quantidade_aulas <= 0:
            continue

        dias = obter_dias_configuracao(
            configuracao
        )

        horarios_por_turma[
            turma_id
        ] = {
            dia: quantidade_aulas
            for dia in dias
        }

    return horarios_por_turma


def obter_valor(
    objeto,
    atributo
):
    if isinstance(objeto, dict):
        return objeto.get(
            atributo
        )

    return getattr(
        objeto,
        atributo,
        None
    )