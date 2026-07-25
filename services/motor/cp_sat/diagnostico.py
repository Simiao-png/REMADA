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

        if not configuracao:
            continue

        quantidade_dias = contar_dias_ativos(
            configuracao
        )

        aulas_por_dia = int(
            obter_valor(
                configuracao,
                "aulas_por_dia"
            )
            or 0
        )

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