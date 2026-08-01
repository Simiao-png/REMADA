from ortools.sat.python import cp_model

from services.motor.estrutura import (
    buscar_configuracao_turma
)


DESCRICOES_STATUS = {
    cp_model.UNKNOWN: (
        "O solver não encontrou uma solução "
        "dentro do tempo disponível."
    ),
    cp_model.MODEL_INVALID: (
        "O modelo CP-SAT possui uma configuração "
        "inválida."
    ),
    cp_model.INFEASIBLE: (
        "Não existe uma grade que satisfaça todas "
        "as regras obrigatórias."
    )
}


def montar_diagnostico(
    status,
    dados,
    turmas
):
    problemas = []

    problemas.append({
        "tipo": "status_cp_sat",
        "mensagem": DESCRICOES_STATUS.get(
            status,
            "O solver não conseguiu gerar a grade."
        )
    })

    problemas.extend(
        diagnosticar_turmas_sem_configuracao(
            dados,
            turmas
        )
    )

    problemas.extend(
        diagnosticar_carga_das_turmas(
            dados,
            turmas
        )
    )

    problemas.extend(
        diagnosticar_disciplinas_sem_professor(
            dados
        )
    )

    problemas.extend(
        diagnosticar_professores_sem_disponibilidade(
            dados
        )
    )

    problemas.extend(
        diagnosticar_insuficiencia_disponibilidade_professor(
            dados
        )
    )

    problemas.extend(
        diagnosticar_limite_semanal_professor(
            dados
        )
    )

    return remover_problemas_duplicados(
        problemas
    )


def diagnosticar_turmas_sem_configuracao(
    dados,
    turmas
):
    configuracoes = dados.get(
        "configuracoes",
        []
    )

    problemas = []

    for turma_id, turma in turmas.items():
        configuracao = buscar_configuracao_turma(
            turma,
            configuracoes
        )

        if configuracao:
            continue

        problemas.append({
            "tipo": "turma_sem_configuracao",
            "turma_id": turma_id,
            "mensagem": (
                f"A turma '{obter_valor(turma, 'nome')}' "
                "não possui configuração horária válida."
            )
        })

    return problemas


def diagnosticar_carga_das_turmas(
    dados,
    turmas
):
    configuracoes = dados.get(
        "configuracoes",
        []
    )

    matrizes = dados.get(
        "turma_disciplina",
        []
    )

    carga_por_turma = {}

    for matriz in matrizes:
        turma_id = obter_valor(
            matriz,
            "turma_id"
        )

        aulas_por_semana = int(
            obter_valor(
                matriz,
                "aulas_por_semana"
            )
            or 0
        )

        carga_por_turma[turma_id] = (
            carga_por_turma.get(
                turma_id,
                0
            )
            + aulas_por_semana
        )

    problemas = []

    for turma_id, turma in turmas.items():
        configuracao = buscar_configuracao_turma(
            turma,
            configuracoes
        )

        aulas_por_dia_padrao = (
            obter_quantidade_aulas_padrao(
                turma
            )
        )

        if configuracao:
            quantidade_dias = contar_dias_ativos(
                configuracao
            )

            aulas_por_dia = int(
                obter_valor(
                    configuracao,
                    "aulas_por_dia"
                )
                or aulas_por_dia_padrao
            )
        else:
            quantidade_dias = 5
            aulas_por_dia = aulas_por_dia_padrao

        total_horarios = (
            quantidade_dias
            * aulas_por_dia
        )

        carga_semanal = carga_por_turma.get(
            turma_id,
            0
        )

        if carga_semanal <= total_horarios:
            continue

        problemas.append({
            "tipo": "carga_excede_horarios",
            "turma_id": turma_id,
            "mensagem": (
                f"A turma '{obter_valor(turma, 'nome')}' "
                f"possui {carga_semanal} aulas semanais, "
                f"mas somente {total_horarios} horários "
                "disponíveis."
            )
        })

    return problemas


def diagnosticar_disciplinas_sem_professor(
    dados
):
    """
    Verifica se cada item da matriz curricular possui
    uma atribuição ProfessorTurma correspondente.

    ProfessorTurma representa diretamente:
    professor + turma + disciplina.
    """
    matrizes = dados.get(
        "turma_disciplina",
        []
    )

    atribuicoes = dados.get(
        "professor_turma",
        []
    )

    turmas = {
        obter_valor(turma, "id"): turma
        for turma in dados.get(
            "turmas",
            []
        )
    }

    disciplinas = {
        obter_valor(disciplina, "id"): disciplina
        for disciplina in dados.get(
            "disciplinas",
            []
        )
    }

    atribuicoes_validas = {
        (
            obter_valor(vinculo, "turma_id"),
            obter_valor(vinculo, "disciplina_id")
        )
        for vinculo in atribuicoes
        if (
            obter_valor(vinculo, "turma_id") is not None
            and obter_valor(vinculo, "disciplina_id") is not None
            and obter_valor(vinculo, "professor_id") is not None
        )
    }

    problemas = []

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

        if (
            turma_id,
            disciplina_id
        ) in atribuicoes_validas:
            continue

        turma = turmas.get(
            turma_id
        )

        disciplina = disciplinas.get(
            disciplina_id
        )

        nome_turma = (
            obter_valor(
                turma,
                "nome"
            )
            or f"ID {turma_id}"
        )

        nome_disciplina = (
            obter_valor(
                disciplina,
                "nome"
            )
            or f"ID {disciplina_id}"
        )

        problemas.append({
            "tipo": "disciplina_sem_professor",
            "turma_id": turma_id,
            "disciplina_id": disciplina_id,
            "mensagem": (
                f"A turma '{nome_turma}' possui "
                f"{aulas_por_semana} aula(s) de "
                f"'{nome_disciplina}', mas ainda não "
                "possui professor atribuído."
            )
        })

    return problemas


def diagnosticar_professores_sem_disponibilidade(
    dados
):
    atribuicoes = dados.get(
        "professor_turma",
        []
    )

    disponibilidades = dados.get(
        "disponibilidades",
        []
    )

    professores = {
        obter_valor(professor, "id"): professor
        for professor in dados.get(
            "professores",
            []
        )
    }

    professores_utilizados = {
        obter_valor(
            vinculo,
            "professor_id"
        )
        for vinculo in atribuicoes
        if obter_valor(
            vinculo,
            "professor_id"
        ) is not None
    }

    professores_disponiveis = {
        obter_valor(
            disponibilidade,
            "professor_id"
        )
        for disponibilidade in disponibilidades
        if (
            obter_valor(
                disponibilidade,
                "professor_id"
            ) is not None
            and obter_valor(
                disponibilidade,
                "disponivel"
            )
        )
    }

    problemas = []

    for professor_id in professores_utilizados:
        if professor_id in professores_disponiveis:
            continue

        professor = professores.get(
            professor_id
        )

        nome_professor = (
            obter_valor(
                professor,
                "nome"
            )
            or f"ID {professor_id}"
        )

        problemas.append({
            "tipo": "professor_sem_disponibilidade",
            "professor_id": professor_id,
            "mensagem": (
                f"O professor '{nome_professor}' possui "
                "aulas atribuídas, mas não possui nenhum "
                "horário disponível cadastrado."
            )
        })

    return problemas


def diagnosticar_insuficiencia_disponibilidade_professor(
    dados
):
    """
    Verifica se a quantidade de horários disponíveis do professor
    é suficiente para acomodar todas as aulas atribuídas a ele.
    """
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

    professores = {
        obter_valor(professor, "id"): professor
        for professor in dados.get(
            "professores",
            []
        )
    }

    carga_por_matriz = {}

    for matriz in matrizes:
        turma_id = obter_valor(
            matriz,
            "turma_id"
        )

        disciplina_id = obter_valor(
            matriz,
            "disciplina_id"
        )

        aulas = int(
            obter_valor(
                matriz,
                "aulas_por_semana"
            )
            or 0
        )

        carga_por_matriz[
            (
                turma_id,
                disciplina_id
            )
        ] = aulas

    carga_necessaria_professor = {}

    for vinculo in atribuicoes:
        professor_id = obter_valor(
            vinculo,
            "professor_id"
        )

        turma_id = obter_valor(
            vinculo,
            "turma_id"
        )

        disciplina_id = obter_valor(
            vinculo,
            "disciplina_id"
        )

        aulas = carga_por_matriz.get(
            (
                turma_id,
                disciplina_id
            ),
            0
        )

        if (
            professor_id is None
            or aulas <= 0
        ):
            continue

        carga_necessaria_professor[
            professor_id
        ] = (
            carga_necessaria_professor.get(
                professor_id,
                0
            )
            + aulas
        )

    horarios_marcados_professor = {}

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

        if professor_id is None:
            continue

        horarios_marcados_professor[
            professor_id
        ] = (
            horarios_marcados_professor.get(
                professor_id,
                0
            )
            + 1
        )

    problemas = []

    for professor_id, carga in (
        carga_necessaria_professor.items()
    ):
        marcados = horarios_marcados_professor.get(
            professor_id,
            0
        )

        if marcados >= carga:
            continue

        professor = professores.get(
            professor_id
        )

        nome_professor = (
            obter_valor(
                professor,
                "nome"
            )
            or f"ID {professor_id}"
        )

        problemas.append({
            "tipo": "disponibilidade_insuficiente",
            "professor_id": professor_id,
            "mensagem": (
                f"O professor '{nome_professor}' precisa "
                f"ministrar {carga} aula(s) na semana, "
                f"mas possui somente {marcados} horário(s) "
                "marcado(s) como disponível(is)."
            )
        })

    return problemas


def diagnosticar_limite_semanal_professor(
    dados
):
    """
    Compara a carga atribuída com o limite semanal cadastrado
    no professor.
    """
    matrizes = dados.get(
        "turma_disciplina",
        []
    )

    atribuicoes = dados.get(
        "professor_turma",
        []
    )

    professores = {
        obter_valor(professor, "id"): professor
        for professor in dados.get(
            "professores",
            []
        )
    }

    carga_por_matriz = {
        (
            obter_valor(matriz, "turma_id"),
            obter_valor(matriz, "disciplina_id")
        ): int(
            obter_valor(
                matriz,
                "aulas_por_semana"
            )
            or 0
        )
        for matriz in matrizes
    }

    carga_atribuida = {}

    for vinculo in atribuicoes:
        professor_id = obter_valor(
            vinculo,
            "professor_id"
        )

        turma_id = obter_valor(
            vinculo,
            "turma_id"
        )

        disciplina_id = obter_valor(
            vinculo,
            "disciplina_id"
        )

        aulas = carga_por_matriz.get(
            (
                turma_id,
                disciplina_id
            ),
            0
        )

        if professor_id is None:
            continue

        carga_atribuida[
            professor_id
        ] = (
            carga_atribuida.get(
                professor_id,
                0
            )
            + aulas
        )

    problemas = []

    for professor_id, carga in carga_atribuida.items():
        professor = professores.get(
            professor_id
        )

        if not professor:
            continue

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

        if carga <= limite:
            continue

        nome_professor = (
            obter_valor(
                professor,
                "nome"
            )
            or f"ID {professor_id}"
        )

        problemas.append({
            "tipo": "limite_semanal_excedido",
            "professor_id": professor_id,
            "mensagem": (
                f"O professor '{nome_professor}' possui "
                f"{carga} aula(s) atribuída(s), mas seu "
                f"limite semanal é de {limite} aula(s)."
            )
        })

    return problemas


def contar_dias_ativos(
    configuracao
):
    atributos = [
        "tem_aula_segunda",
        "tem_aula_terca",
        "tem_aula_quarta",
        "tem_aula_quinta",
        "tem_aula_sexta",
        "tem_aula_sabado"
    ]

    return sum(
        1
        for atributo in atributos
        if obter_valor(
            configuracao,
            atributo
        )
    )


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


def remover_problemas_duplicados(
    problemas
):
    problemas_unicos = []
    mensagens = set()

    for problema in problemas:
        mensagem = problema.get(
            "mensagem",
            str(problema)
        )

        if mensagem in mensagens:
            continue

        mensagens.add(
            mensagem
        )

        problemas_unicos.append(
            problema
        )

    return problemas_unicos


def obter_valor(
    objeto,
    atributo
):
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