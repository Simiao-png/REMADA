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

        # Trata dinamicamente turmas de Ensino Médio com 7 aulas por dia
        segmento = str(obter_valor(turma, "segmento") or "").lower()
        if "médio" in segmento or "medio" in segmento:
            aulas_por_dia_padrao = 7
        else:
            aulas_por_dia_padrao = 6

        if configuracao:
            quantidade_dias = contar_dias_ativos(configuracao)
            aulas_por_dia = int(
                obter_valor(configuracao, "aulas_por_dia") or aulas_por_dia_padrao
            )
        else:
            quantidade_dias = 5
            aulas_por_dia = aulas_por_dia_padrao

        total_horarios = quantidade_dias * aulas_por_dia
        carga_semanal = carga_por_turma.get(turma_id, 0)

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
    matrizes = dados.get(
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

    professores_por_turma = {}

    for vinculo in professor_turma:
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

    professores_por_disciplina = {}

    for vinculo in professor_disciplina:
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

        if professores_validos:
            continue

        problemas.append({
            "tipo": "disciplina_sem_professor",
            "turma_id": turma_id,
            "disciplina_id": disciplina_id,
            "mensagem": (
                f"A turma {turma_id} possui "
                f"{aulas_por_semana} aula(s) da "
                f"disciplina {disciplina_id}, mas não "
                "existe professor vinculado à turma "
                "e à disciplina simultaneamente."
            )
        })

    return problemas


def diagnosticar_professores_sem_disponibilidade(
    dados
):
    professor_turma = dados.get(
        "professor_turma",
        []
    )

    disponibilidades = dados.get(
        "disponibilidades",
        []
    )

    professores_utilizados = {
        obter_valor(
            vinculo,
            "professor_id"
        )
        for vinculo in professor_turma
    }

    professores_disponiveis = {
        obter_valor(
            disponibilidade,
            "professor_id"
        )
        for disponibilidade in disponibilidades
    }

    problemas = []

    for professor_id in professores_utilizados:
        if professor_id in professores_disponiveis:
            continue

        problemas.append({
            "tipo": "professor_sem_disponibilidade",
            "professor_id": professor_id,
            "mensagem": (
                f"O professor {professor_id} está "
                "vinculado a uma turma, mas não possui "
                "disponibilidade cadastrada."
            )
        })

    return problemas


def diagnosticar_insuficiencia_disponibilidade_professor(
    dados
):
    """
    Diagnostica se algum professor possui mais aulas atribuídas na carga horária
    do que horários marcados como disponíveis na sua grade semanal.
    """
    matrizes = dados.get("turma_disciplina", [])
    professor_turma = dados.get("professor_turma", [])
    professor_disciplina = dados.get("professor_disciplina", [])
    disponibilidades = dados.get("disponibilidades", [])
    professores = {p.id: p for p in dados.get("professores", [])}

    professores_por_turma = {}
    for vinculo in professor_turma:
        professores_por_turma.setdefault(obter_valor(vinculo, "turma_id"), set()).add(obter_valor(vinculo, "professor_id"))

    professores_por_disciplina = {}
    for vinculo in professor_disciplina:
        professores_por_disciplina.setdefault(obter_valor(vinculo, "disciplina_id"), set()).add(obter_valor(vinculo, "professor_id"))

    carga_necessaria_professor = {}

    for matriz in matrizes:
        t_id = obter_valor(matriz, "turma_id")
        d_id = obter_valor(matriz, "disciplina_id")
        aulas = int(obter_valor(matriz, "aulas_por_semana") or 0)

        professores_validos = professores_por_turma.get(t_id, set()) & professores_por_disciplina.get(d_id, set())
        for p_id in professores_validos:
            carga_necessaria_professor[p_id] = carga_necessaria_professor.get(p_id, 0) + aulas

    horarios_marcados_professor = {}
    for d in disponibilidades:
        if obter_valor(d, "disponivel"):
            p_id = obter_valor(d, "professor_id")
            horarios_marcados_professor[p_id] = horarios_marcados_professor.get(p_id, 0) + 1

    problemas = []
    for p_id, carga in carga_necessaria_professor.items():
        # Se o professor tem registro de disponibilidade
        if p_id in horarios_marcados_professor:
            marcados = horarios_marcados_professor[p_id]
            if marcados < carga:
                prof_obj = professores.get(p_id)
                prof_nome = obter_valor(prof_obj, "nome") or f"ID {p_id}"
                problemas.append({
                    "tipo": "disponibilidade_insuficiente",
                    "professor_id": p_id,
                    "mensagem": (
                        f"O professor '{prof_nome}' precisa ministrar {carga} aula(s) "
                        f"na semana, mas só possui {marcados} horário(s) marcados "
                        "como disponíveis."
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
    if isinstance(objeto, dict):
        return objeto.get(
            atributo
        )

    return getattr(
        objeto,
        atributo,
        None
    )