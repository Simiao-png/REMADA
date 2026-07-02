def analisar_inviabilidade(dados):
    problemas = []

    problemas.extend(verificar_carga_horaria_vs_slots(dados))
    problemas.extend(verificar_professor_sem_disponibilidade(dados))
    problemas.extend(verificar_disciplina_sem_professor(dados))
    problemas.extend(verificar_professor_com_carga_excessiva(dados))
    problemas.extend(verificar_professor_disciplina_sem_turma(dados))

    return {
        "viavel": len(problemas) == 0,
        "problemas": problemas
    }


def verificar_carga_horaria_vs_slots(dados):
    problemas = []

    turmas = dados.get("turmas", [])
    cargas = dados.get("cargas_horarias", [])
    configuracoes = dados.get("configuracoes", [])

    aulas_por_dia = 6

    if configuracoes:
        aulas_por_dia = configuracoes[0].aulas_por_dia

    dias_semana = 5

    for turma in turmas:
        carga_total = sum(
            carga.quantidade_aulas_semana
            for carga in cargas
            if carga.turma_id == turma.id
        )

        capacidade = aulas_por_dia * dias_semana

        if carga_total > capacidade:
            problemas.append({
                "tipo": "CARGA_HORARIA_EXCESSIVA",
                "turma": turma.nome,
                "mensagem": (
                    f"A turma '{turma.nome}' possui "
                    f"{carga_total} aulas para apenas "
                    f"{capacidade} horários."
                )
            })

    return problemas


def verificar_professor_sem_disponibilidade(dados):
    problemas = []

    professores = dados.get("professores", [])
    disponibilidades = dados.get("disponibilidades", [])
    professor_disciplina = dados.get("professor_disciplina", [])
    professor_turma = dados.get("professor_turma", [])

    professores_com_disponibilidade = {
        disp.professor_id
        for disp in disponibilidades
    }

    professores_utilizados = {
        rel_disciplina.professor_id
        for rel_disciplina in professor_disciplina
        for rel_turma in professor_turma
        if rel_disciplina.professor_id == rel_turma.professor_id
    }

    for professor in professores:
        if (
            professor.id in professores_utilizados
            and professor.id not in professores_com_disponibilidade
        ):
            problemas.append({
                "tipo": "PROFESSOR_SEM_DISPONIBILIDADE",
                "professor": professor.nome,
                "mensagem": (
                    f"O professor '{professor.nome}' "
                    "não possui disponibilidade cadastrada."
                )
            })

    return problemas


def verificar_disciplina_sem_professor(dados):
    problemas = []

    cargas = dados.get("cargas_horarias", [])
    professor_disciplina = dados.get("professor_disciplina", [])

    disciplinas = {
        rel.disciplina_id
        for rel in professor_disciplina
    }

    for carga in cargas:
        if carga.disciplina_id not in disciplinas:
            problemas.append({
                "tipo": "DISCIPLINA_SEM_PROFESSOR",
                "disciplina_id": carga.disciplina_id,
                "mensagem": (
                    "Existe uma carga horária cadastrada "
                    "para uma disciplina sem professor."
                )
            })

    return problemas


def verificar_professor_com_carga_excessiva(dados):
    problemas = []

    cargas = dados.get("cargas_horarias", [])
    disponibilidades = dados.get("disponibilidades", [])
    professor_disciplina = dados.get("professor_disciplina", [])

    for relacao in professor_disciplina:
        carga_total = sum(
            carga.quantidade_aulas_semana
            for carga in cargas
            if carga.disciplina_id == relacao.disciplina_id
        )

        disponibilidade = sum(
            1
            for disp in disponibilidades
            if disp.professor_id == relacao.professor_id
        )

        if carga_total > disponibilidade:
            problemas.append({
                "tipo": "PROFESSOR_COM_CARGA_EXCESSIVA",
                "professor_id": relacao.professor_id,
                "mensagem": (
                    f"O professor {relacao.professor_id} "
                    f"possui apenas {disponibilidade} horários "
                    f"para {carga_total} aulas."
                )
            })

    return problemas

def verificar_professor_disciplina_sem_turma(dados):
    problemas = []

    cargas = dados.get("cargas_horarias", [])
    professor_disciplina = dados.get("professor_disciplina", [])
    professor_turma = dados.get("professor_turma", [])
    professores = dados.get("professores", [])

    mapa_professores = {
        professor.id: professor.nome
        for professor in professores
    }

    for relacao in professor_disciplina:
        turmas_que_precisam_da_disciplina = {
            carga.turma_id
            for carga in cargas
            if carga.disciplina_id == relacao.disciplina_id
        }

        turmas_do_professor = {
            rel_turma.turma_id
            for rel_turma in professor_turma
            if rel_turma.professor_id == relacao.professor_id
        }

        turmas_compativeis = turmas_que_precisam_da_disciplina.intersection(
            turmas_do_professor
        )

        if turmas_que_precisam_da_disciplina and not turmas_compativeis:
            nome_professor = mapa_professores.get(
                relacao.professor_id,
                f"Professor {relacao.professor_id}"
            )

            problemas.append({
                "tipo": "PROFESSOR_DISCIPLINA_SEM_TURMA",
                "professor_id": relacao.professor_id,
                "disciplina_id": relacao.disciplina_id,
                "mensagem": (
                    f"O professor '{nome_professor}' está vinculado "
                    f"à disciplina {relacao.disciplina_id}, mas não está "
                    "vinculado a nenhuma turma que precisa dessa disciplina."
                )
            })

    return problemas