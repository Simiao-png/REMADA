def obter_dias_configuracao(configuracao):
    dias = []

    if configuracao.tem_aula_segunda:
        dias.append("segunda")

    if configuracao.tem_aula_terca:
        dias.append("terca")

    if configuracao.tem_aula_quarta:
        dias.append("quarta")

    if configuracao.tem_aula_quinta:
        dias.append("quinta")

    if configuracao.tem_aula_sexta:
        dias.append("sexta")

    if configuracao.tem_aula_sabado:
        dias.append("sabado")

    return dias


def buscar_configuracao_turma(
    turma,
    configuracoes
):
    configuracoes_por_id = {
        configuracao.id: configuracao
        for configuracao in configuracoes
        if configuracao.ativo
    }

    configuracao = configuracoes_por_id.get(
        turma.configuracao_horaria_id
    )

    if configuracao:
        return configuracao

    for configuracao in configuracoes:
        if not configuracao.ativo:
            continue

        if configuracao.segmento == turma.segmento:
            return configuracao

    return None


def criar_grade_vazia(
    configuracoes,
    turmas
):
    grade = {}

    for turma_id, turma in turmas.items():
        configuracao = buscar_configuracao_turma(
            turma,
            configuracoes
        )

        if not configuracao:
            raise ValueError(
                f"A turma '{turma.nome}' não possui "
                "configuração horária válida."
            )

        dias = obter_dias_configuracao(
            configuracao
        )

        grade[turma_id] = {}

        for dia in dias:
            grade[turma_id][dia] = [
                None
                for _ in range(
                    configuracao.aulas_por_dia
                )
            ]

    return grade