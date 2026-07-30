def obter_valor(objeto, atributo):
    """Auxiliar para extrair valores tanto de dicionários quanto de objetos SQLAlchemy."""
    if isinstance(objeto, dict):
        return objeto.get(atributo)
    return getattr(objeto, atributo, None)


def normalizar_dia(dia):
    """Normaliza representações de dias da semana para string padronizada."""
    if dia is None:
        return ""
    d_str = str(dia).lower().strip()
    mapa = {
        "1": "segunda", "segunda": "segunda", "segunda-feira": "segunda",
        "2": "terca", "terca": "terca", "terça": "terca", "terca-feira": "terca", "terça-feira": "terca",
        "3": "quarta", "quarta": "quarta", "quarta-feira": "quarta",
        "4": "quinta", "quinta": "quinta", "quinta-feira": "quinta",
        "5": "sexta", "sexta": "sexta", "sexta-feira": "sexta",
        "6": "sabado", "sabado": "sabado", "sábado": "sabado", "sabado-feira": "sabado"
    }
    return mapa.get(d_str, d_str)


def adicionar_restricoes(modelo, dados, variaveis):
    """Aplica todas as restrições no modelo CP-SAT."""
    adicionar_carga_horaria_semanal(modelo, dados, variaveis)
    adicionar_limite_por_horario_da_turma(modelo, variaveis)
    adicionar_limite_por_horario_do_professor(modelo, variaveis)
    adicionar_disponibilidade_professor(modelo, dados, variaveis)
    adicionar_limite_disciplina_por_dia(modelo, variaveis, limite=2)


def adicionar_carga_horaria_semanal(modelo, dados, variaveis):
    """Garante que a turma cumpra exatamente a carga horária semanal cadastrada."""
    matrizes = dados.get("turma_disciplina", [])

    for matriz in matrizes:
        turma_id = obter_valor(matriz, "turma_id")
        disciplina_id = obter_valor(matriz, "disciplina_id")
        aulas_por_semana = int(obter_valor(matriz, "aulas_por_semana") or 0)

        variaveis_da_matriz = []
        for chave, variavel in variaveis.items():
            chave_turma, chave_disciplina, _, _, _ = chave
            if chave_turma == turma_id and chave_disciplina == disciplina_id:
                variaveis_da_matriz.append(variavel)

        if variaveis_da_matriz:
            modelo.Add(sum(variaveis_da_matriz) == aulas_por_semana)


def adicionar_limite_por_horario_da_turma(modelo, variaveis):
    """Garante que a turma tenha no máximo 1 aula por horário (sem choque de turma)."""
    grupos = {}
    for chave, variavel in variaveis.items():
        turma_id, _, _, dia, indice = chave
        chave_horario = (turma_id, normalizar_dia(dia), indice)
        grupos.setdefault(chave_horario, []).append(variavel)

    for variaveis_horario in grupos.values():
        modelo.Add(sum(variaveis_horario) <= 1)


def adicionar_limite_por_horario_do_professor(modelo, variaveis):
    """Garante que o professor esteja em no máximo 1 turma por horário (sem choque de professor)."""
    grupos = {}
    for chave, variavel in variaveis.items():
        _, _, professor_id, dia, indice = chave
        chave_horario = (professor_id, normalizar_dia(dia), indice)
        grupos.setdefault(chave_horario, []).append(variavel)

    for variaveis_horario in grupos.values():
        modelo.Add(sum(variaveis_horario) <= 1)


def adicionar_disponibilidade_professor(modelo, dados, variaveis):
    """Bloqueia alocações em horários indisponíveis do professor."""
    disponibilidades = dados.get("disponibilidades", [])
    horarios_disponiveis = set()
    professores_com_disponibilidade = set()

    for disp in disponibilidades:
        professor_id = obter_valor(disp, "professor_id")
        if professor_id is not None:
            professores_com_disponibilidade.add(professor_id)

        if not obter_valor(disp, "disponivel"):
            continue

        dia = obter_valor(disp, "dia_semana")
        numero_aula = obter_valor(disp, "numero_aula")
        if numero_aula is not None:
            aula_idx = int(numero_aula) - 1
            horarios_disponiveis.add((professor_id, normalizar_dia(dia), aula_idx))

    for chave, variavel in variaveis.items():
        _, _, professor_id, dia, indice = chave
        horario_professor = (professor_id, normalizar_dia(dia), indice)

        if professor_id in professores_com_disponibilidade:
            if horario_professor not in horarios_disponiveis:
                modelo.Add(variavel == 0)


def adicionar_limite_disciplina_por_dia(modelo, variaveis, limite=2):
    """
    Garante limite rígido de no MÁXIMO `limite` aulas (padrão=2) da mesma 
    disciplina no mesmo dia para uma turma, eliminando a 3ª aula indesejada.
    """
    grupos = {}
    for chave, variavel in variaveis.items():
        turma_id, disciplina_id, _, dia, _ = chave
        chave_disciplina_dia = (turma_id, disciplina_id, normalizar_dia(dia))
        grupos.setdefault(chave_disciplina_dia, []).append(variavel)

    for variaveis_disciplina in grupos.values():
        # Trava rígida em no máximo 2 aulas por dia (ex: 1 dobradinha ou aulas isoladas)
        modelo.Add(sum(variaveis_disciplina) <= limite)