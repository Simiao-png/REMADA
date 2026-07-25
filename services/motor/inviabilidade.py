from services.motor.estrutura import (
    buscar_configuracao_turma,
    obter_dias_configuracao
)


def analisar_inviabilidade(dados):
    problemas = []

    problemas.extend(
        verificar_carga_horaria_vs_slots(dados)
    )

    problemas.extend(
        verificar_professor_sem_disponibilidade(dados)
    )

    problemas.extend(
        verificar_disciplina_sem_professor(dados)
    )

    problemas.extend(
        verificar_professor_com_carga_excessiva(dados)
    )

    problemas.extend(
        verificar_atribuicao_invalida(dados)
    )

    return {
        "viavel": len(problemas) == 0,
        "problemas": problemas
    }


def verificar_carga_horaria_vs_slots(dados):
    problemas = []

    turmas = dados.get("turmas", [])
    matrizes = dados.get(
        "turma_disciplina",
        []
    )

    configuracoes = dados.get(
        "configuracoes",
        []
    )

    for turma in turmas:
        configuracao = buscar_configuracao_turma(
            turma,
            configuracoes
        )

        if not configuracao:
            problemas.append({
                "tipo": "TURMA_SEM_CONFIGURACAO",
                "turma_id": turma.id,
                "turma": turma.nome,
                "mensagem": (
                    f"A turma '{turma.nome}' não possui "
                    "configuração horária válida."
                )
            })

            continue

        dias = obter_dias_configuracao(
            configuracao
        )

        capacidade = (
            len(dias)
            * int(configuracao.aulas_por_dia or 0)
        )

        carga_total = sum(
            int(matriz.aulas_por_semana or 0)
            for matriz in matrizes
            if matriz.turma_id == turma.id
        )

        if carga_total > capacidade:
            problemas.append({
                "tipo": "CARGA_HORARIA_EXCESSIVA",
                "turma_id": turma.id,
                "turma": turma.nome,
                "carga_total": carga_total,
                "capacidade": capacidade,
                "mensagem": (
                    f"A turma '{turma.nome}' possui "
                    f"{carga_total} aulas para apenas "
                    f"{capacidade} horários."
                )
            })

    return problemas


def verificar_professor_sem_disponibilidade(
    dados
):
    problemas = []

    professores = dados.get(
        "professores",
        []
    )

    disponibilidades = dados.get(
        "disponibilidades",
        []
    )

    atribuicoes = dados.get(
        "professor_turma",
        []
    )

    mapa_professores = {
        professor.id: professor.nome
        for professor in professores
    }

    professores_utilizados = {
        atribuicao.professor_id
        for atribuicao in atribuicoes
    }

    professores_com_disponibilidade = {
        disponibilidade.professor_id
        for disponibilidade in disponibilidades
        if disponibilidade.disponivel
    }

    for professor_id in professores_utilizados:
        if (
            professor_id
            not in professores_com_disponibilidade
        ):
            nome_professor = mapa_professores.get(
                professor_id,
                f"Professor {professor_id}"
            )

            problemas.append({
                "tipo": (
                    "PROFESSOR_SEM_DISPONIBILIDADE"
                ),
                "professor_id": professor_id,
                "professor": nome_professor,
                "mensagem": (
                    f"O professor '{nome_professor}' "
                    "não possui disponibilidade cadastrada."
                )
            })

    return problemas


def verificar_disciplina_sem_professor(dados):
    problemas = []

    matrizes = dados.get(
        "turma_disciplina",
        []
    )

    atribuicoes = dados.get(
        "professor_turma",
        []
    )

    turmas = dados.get(
        "turmas",
        []
    )

    disciplinas = dados.get(
        "disciplinas",
        []
    )

    mapa_turmas = {
        turma.id: turma.nome
        for turma in turmas
    }

    mapa_disciplinas = {
        disciplina.id: disciplina.nome
        for disciplina in disciplinas
    }

    chaves_atribuidas = {
        (
            atribuicao.turma_id,
            atribuicao.disciplina_id
        )
        for atribuicao in atribuicoes
    }

    for matriz in matrizes:
        quantidade = int(
            matriz.aulas_por_semana or 0
        )

        if quantidade <= 0:
            continue

        chave = (
            matriz.turma_id,
            matriz.disciplina_id
        )

        if chave in chaves_atribuidas:
            continue

        nome_turma = mapa_turmas.get(
            matriz.turma_id,
            f"Turma {matriz.turma_id}"
        )

        nome_disciplina = mapa_disciplinas.get(
            matriz.disciplina_id,
            f"Disciplina {matriz.disciplina_id}"
        )

        problemas.append({
            "tipo": "DISCIPLINA_SEM_PROFESSOR",
            "turma_id": matriz.turma_id,
            "disciplina_id": matriz.disciplina_id,
            "mensagem": (
                f"A disciplina '{nome_disciplina}' "
                f"da turma '{nome_turma}' não possui "
                "professor atribuído."
            )
        })

    return problemas


def verificar_professor_com_carga_excessiva(
    dados
):
    problemas = []

    professores = dados.get(
        "professores",
        []
    )

    matrizes = dados.get(
        "turma_disciplina",
        []
    )

    atribuicoes = dados.get(
        "professor_turma",
        []
    )

    disponibilidades = dados.get(
        "disponibilidades",
        []
    )

    mapa_professores = {
        professor.id: professor
        for professor in professores
    }

    mapa_matrizes = {
        (
            matriz.turma_id,
            matriz.disciplina_id
        ): int(matriz.aulas_por_semana or 0)
        for matriz in matrizes
    }

    carga_por_professor = {}

    for atribuicao in atribuicoes:
        chave = (
            atribuicao.turma_id,
            atribuicao.disciplina_id
        )

        quantidade = mapa_matrizes.get(
            chave,
            0
        )

        carga_por_professor[
            atribuicao.professor_id
        ] = (
            carga_por_professor.get(
                atribuicao.professor_id,
                0
            )
            + quantidade
        )

    disponibilidade_por_professor = {}

    for disponibilidade in disponibilidades:
        if not disponibilidade.disponivel:
            continue

        professor_id = (
            disponibilidade.professor_id
        )

        disponibilidade_por_professor[
            professor_id
        ] = (
            disponibilidade_por_professor.get(
                professor_id,
                0
            )
            + 1
        )

    for professor_id, carga_total in (
        carga_por_professor.items()
    ):
        professor = mapa_professores.get(
            professor_id
        )

        disponibilidade_total = (
            disponibilidade_por_professor.get(
                professor_id,
                0
            )
        )

        nome_professor = (
            professor.nome
            if professor
            else f"Professor {professor_id}"
        )

        if carga_total > disponibilidade_total:
            problemas.append({
                "tipo": (
                    "PROFESSOR_COM_CARGA_EXCESSIVA"
                ),
                "professor_id": professor_id,
                "carga_total": carga_total,
                "disponibilidade_total": (
                    disponibilidade_total
                ),
                "mensagem": (
                    f"O professor '{nome_professor}' "
                    f"possui {carga_total} aulas atribuídas, "
                    f"mas apenas {disponibilidade_total} "
                    "horários disponíveis."
                )
            })

        if not professor:
            continue

        carga_contratada = int(
            professor.carga_horaria_semanal or 0
        )

        if (
            carga_contratada > 0
            and carga_total > carga_contratada
        ):
            problemas.append({
                "tipo": (
                    "PROFESSOR_ACIMA_DA_CARGA_SEMANAL"
                ),
                "professor_id": professor_id,
                "carga_atribuida": carga_total,
                "carga_semanal": carga_contratada,
                "mensagem": (
                    f"O professor '{nome_professor}' "
                    f"possui {carga_total} aulas atribuídas "
                    f"para uma carga semanal de "
                    f"{carga_contratada} aulas."
                )
            })

    return problemas


def verificar_atribuicao_invalida(dados):
    problemas = []

    atribuicoes = dados.get(
        "professor_turma",
        []
    )

    professores_disciplinas = dados.get(
        "professor_disciplina",
        []
    )

    matrizes = dados.get(
        "turma_disciplina",
        []
    )

    professores = dados.get(
        "professores",
        []
    )

    turmas = dados.get(
        "turmas",
        []
    )

    disciplinas = dados.get(
        "disciplinas",
        []
    )

    mapa_professores = {
        professor.id: professor.nome
        for professor in professores
    }

    mapa_turmas = {
        turma.id: turma.nome
        for turma in turmas
    }

    mapa_disciplinas = {
        disciplina.id: disciplina.nome
        for disciplina in disciplinas
    }

    vinculos_professor_disciplina = {
        (
            vinculo.professor_id,
            vinculo.disciplina_id
        )
        for vinculo in professores_disciplinas
    }

    matrizes_validas = {
        (
            matriz.turma_id,
            matriz.disciplina_id
        )
        for matriz in matrizes
        if int(matriz.aulas_por_semana or 0) > 0
    }

    for atribuicao in atribuicoes:
        chave_professor_disciplina = (
            atribuicao.professor_id,
            atribuicao.disciplina_id
        )

        chave_matriz = (
            atribuicao.turma_id,
            atribuicao.disciplina_id
        )

        nome_professor = mapa_professores.get(
            atribuicao.professor_id,
            f"Professor {atribuicao.professor_id}"
        )

        nome_turma = mapa_turmas.get(
            atribuicao.turma_id,
            f"Turma {atribuicao.turma_id}"
        )

        nome_disciplina = mapa_disciplinas.get(
            atribuicao.disciplina_id,
            f"Disciplina {atribuicao.disciplina_id}"
        )

        if (
            chave_professor_disciplina
            not in vinculos_professor_disciplina
        ):
            problemas.append({
                "tipo": (
                    "PROFESSOR_NAO_LECIONA_DISCIPLINA"
                ),
                "professor_id": (
                    atribuicao.professor_id
                ),
                "turma_id": atribuicao.turma_id,
                "disciplina_id": (
                    atribuicao.disciplina_id
                ),
                "mensagem": (
                    f"O professor '{nome_professor}' "
                    f"foi atribuído à disciplina "
                    f"'{nome_disciplina}' da turma "
                    f"'{nome_turma}', mas não está "
                    "vinculado a essa disciplina."
                )
            })

        if chave_matriz not in matrizes_validas:
            problemas.append({
                "tipo": (
                    "ATRIBUICAO_FORA_DA_MATRIZ"
                ),
                "professor_id": (
                    atribuicao.professor_id
                ),
                "turma_id": atribuicao.turma_id,
                "disciplina_id": (
                    atribuicao.disciplina_id
                ),
                "mensagem": (
                    f"A atribuição de '{nome_disciplina}' "
                    f"para a turma '{nome_turma}' não possui "
                    "carga válida na matriz curricular."
                )
            })

    return problemas