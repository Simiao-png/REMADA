def criar_fila_aulas(
    turmas_disciplinas,
    professores_turmas,
    disponibilidades
):
    fila = []

    mapa_professores = {
        (
            vinculo.turma_id,
            vinculo.disciplina_id
        ): vinculo.professor_id
        for vinculo in professores_turmas
    }

    carga_por_professor = (
        calcular_carga_por_professor(
            turmas_disciplinas,
            mapa_professores
        )
    )

    horarios_por_professor = (
        calcular_horarios_disponiveis(
            disponibilidades
        )
    )

    matrizes_ordenadas = sorted(
        turmas_disciplinas,
        key=lambda matriz: (
            calcular_prioridade_matriz(
                matriz,
                mapa_professores,
                carga_por_professor,
                horarios_por_professor
            )
        )
    )

    for matriz in matrizes_ordenadas:
        quantidade_aulas = int(
            matriz.aulas_por_semana or 0
        )

        if quantidade_aulas <= 0:
            continue

        professor_id = mapa_professores.get(
            (
                matriz.turma_id,
                matriz.disciplina_id
            )
        )

        carga_professor = (
            carga_por_professor.get(
                professor_id,
                0
            )
        )

        horarios_disponiveis = len(
            horarios_por_professor.get(
                professor_id,
                set()
            )
        )

        margem_professor = (
            horarios_disponiveis
            - carga_professor
        )

        for _ in range(quantidade_aulas):
            fila.append({
                "turma_id": matriz.turma_id,
                "disciplina_id": (
                    matriz.disciplina_id
                ),
                "professor_id": professor_id,

                "permite_aula_dupla": (
                    quantidade_aulas >= 2
                ),

                "permite_aula_tripla": False,

                "exige_distribuicao_semanal": (
                    quantidade_aulas >= 3
                ),

                "quantidade_minima_dias_semana": min(
                    quantidade_aulas,
                    3
                ),

                "carga_professor": (
                    carga_professor
                ),

                "horarios_disponiveis_professor": (
                    horarios_disponiveis
                ),

                "margem_professor": (
                    margem_professor
                )
            })

    imprimir_prioridade_fila(fila)

    return fila


def calcular_carga_por_professor(
    turmas_disciplinas,
    mapa_professores
):
    carga_por_professor = {}

    for matriz in turmas_disciplinas:
        professor_id = mapa_professores.get(
            (
                matriz.turma_id,
                matriz.disciplina_id
            )
        )

        if professor_id is None:
            continue

        quantidade = int(
            matriz.aulas_por_semana or 0
        )

        carga_por_professor[professor_id] = (
            carga_por_professor.get(
                professor_id,
                0
            )
            + quantidade
        )

    return carga_por_professor


def calcular_horarios_disponiveis(
    disponibilidades
):
    horarios_por_professor = {}

    for disponibilidade in disponibilidades:
        if not disponibilidade.disponivel:
            continue

        professor_id = (
            disponibilidade.professor_id
        )

        horarios_por_professor.setdefault(
            professor_id,
            set()
        )

        horarios_por_professor[
            professor_id
        ].add(
            (
                disponibilidade.dia_semana,
                disponibilidade.numero_aula
            )
        )

    return horarios_por_professor


def calcular_prioridade_matriz(
    matriz,
    mapa_professores,
    carga_por_professor,
    horarios_por_professor
):
    professor_id = mapa_professores.get(
        (
            matriz.turma_id,
            matriz.disciplina_id
        )
    )

    quantidade_aulas = int(
        matriz.aulas_por_semana or 0
    )

    if professor_id is None:
        return (
            1,
            0,
            0,
            -quantidade_aulas,
            matriz.turma_id,
            matriz.disciplina_id
        )

    carga_professor = (
        carga_por_professor.get(
            professor_id,
            0
        )
    )

    quantidade_horarios = len(
        horarios_por_professor.get(
            professor_id,
            set()
        )
    )

    margem = (
        quantidade_horarios
        - carga_professor
    )

    if quantidade_horarios > 0:
        taxa_ocupacao = (
            carga_professor
            / quantidade_horarios
        )
    else:
        taxa_ocupacao = float("inf")

    return (
        0,

        # Menor margem entra primeiro.
        margem,

        # Maior taxa de ocupação entra primeiro.
        -taxa_ocupacao,

        # Maior carga total entra primeiro.
        -carga_professor,

        # Maior quantidade desta disciplina primeiro.
        -quantidade_aulas,

        # Mantém agrupadas as aulas iguais.
        matriz.turma_id,
        matriz.disciplina_id
    )


def imprimir_prioridade_fila(fila):
    print(
        "\n========== PRIORIDADE DA FILA =========="
    )

    aulas_exibidas = set()

    for aula in fila:
        chave = (
            aula["turma_id"],
            aula["disciplina_id"],
            aula["professor_id"]
        )

        if chave in aulas_exibidas:
            continue

        aulas_exibidas.add(chave)

        print(
            f"Turma {aula['turma_id']} | "
            f"Disciplina {aula['disciplina_id']} | "
            f"Professor {aula['professor_id']} | "
            f"Carga {aula['carga_professor']} | "
            f"Disponíveis "
            f"{aula['horarios_disponiveis_professor']} | "
            f"Margem {aula['margem_professor']}"
        )

    print(
        "========================================\n"
    )