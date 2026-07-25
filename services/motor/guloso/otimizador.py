from services.motor.guloso.estado import (
    registrar_aula,
    remover_aula
)

from services.motor.guloso.validacoes import (
    pode_alocar_aula
)

from services.motor.guloso.penalidades import (
    calcular_penalidade
)


MAXIMO_MOVIMENTOS = 100


def otimizar_grade(
    estado,
    disponibilidades
):
    movimentos_realizados = 0

    while movimentos_realizados < MAXIMO_MOVIMENTOS:
        melhor_movimento = encontrar_melhor_movimento(
            estado,
            disponibilidades
        )

        if melhor_movimento is None:
            break

        executar_movimento(
            estado,
            melhor_movimento
        )

        movimentos_realizados += 1

        imprimir_movimento(
            melhor_movimento,
            movimentos_realizados
        )

    print(
        f"\nAJUSTE FINO FINALIZADO -> "
        f"{movimentos_realizados} movimento(s) realizado(s).\n"
    )

    return estado["grade"]


def encontrar_melhor_movimento(
    estado,
    disponibilidades
):
    aulas = listar_aulas_alocadas(estado)

    melhor_movimento = None
    melhor_reducao = 0

    for aula in aulas:
        movimento = avaliar_movimentos_da_aula(
            estado,
            disponibilidades,
            aula
        )

        if movimento is None:
            continue

        reducao = movimento["reducao"]

        if reducao > melhor_reducao:
            melhor_reducao = reducao
            melhor_movimento = movimento

    return melhor_movimento


def avaliar_movimentos_da_aula(
    estado,
    disponibilidades,
    aula
):
    grade = estado["grade"]

    turma_id = aula["turma_id"]
    professor_id = aula["professor_id"]
    disciplina_id = aula["disciplina_id"]

    dia_origem = aula["dia"]
    indice_origem = aula["indice"]

    retirar_aula(
        estado,
        turma_id,
        professor_id,
        disciplina_id,
        dia_origem,
        indice_origem
    )

    penalidade_origem = calcular_penalidade(
        estado,
        turma_id,
        professor_id,
        disciplina_id,
        dia_origem,
        indice_origem,
        quantidade_aulas=1
    )

    melhor_movimento = None
    melhor_reducao = 0

    for dia_destino, horarios in grade[turma_id].items():
        for indice_destino in range(len(horarios)):
            if (
                dia_destino == dia_origem
                and indice_destino == indice_origem
            ):
                continue

            if not pode_alocar_aula(
                estado,
                disponibilidades,
                turma_id,
                professor_id,
                disciplina_id,
                dia_destino,
                indice_destino
            ):
                continue

            penalidade_destino = calcular_penalidade(
                estado,
                turma_id,
                professor_id,
                disciplina_id,
                dia_destino,
                indice_destino,
                quantidade_aulas=1
            )

            reducao = (
                penalidade_origem
                - penalidade_destino
            )

            if reducao <= melhor_reducao:
                continue

            melhor_reducao = reducao

            melhor_movimento = {
                "turma_id": turma_id,
                "professor_id": professor_id,
                "disciplina_id": disciplina_id,
                "dia_origem": dia_origem,
                "indice_origem": indice_origem,
                "dia_destino": dia_destino,
                "indice_destino": indice_destino,
                "penalidade_origem": penalidade_origem,
                "penalidade_destino": penalidade_destino,
                "reducao": reducao
            }

    colocar_aula(
        estado,
        turma_id,
        professor_id,
        disciplina_id,
        dia_origem,
        indice_origem
    )

    return melhor_movimento


def executar_movimento(
    estado,
    movimento
):
    turma_id = movimento["turma_id"]
    professor_id = movimento["professor_id"]
    disciplina_id = movimento["disciplina_id"]

    retirar_aula(
        estado,
        turma_id,
        professor_id,
        disciplina_id,
        movimento["dia_origem"],
        movimento["indice_origem"]
    )

    colocar_aula(
        estado,
        turma_id,
        professor_id,
        disciplina_id,
        movimento["dia_destino"],
        movimento["indice_destino"]
    )


def retirar_aula(
    estado,
    turma_id,
    professor_id,
    disciplina_id,
    dia,
    indice
):
    grade = estado["grade"]

    grade[turma_id][dia][indice] = None

    remover_aula(
        estado,
        turma_id,
        professor_id,
        disciplina_id,
        dia,
        indice
    )


def colocar_aula(
    estado,
    turma_id,
    professor_id,
    disciplina_id,
    dia,
    indice
):
    grade = estado["grade"]

    grade[turma_id][dia][indice] = {
        "professor": professor_id,
        "disciplina": disciplina_id
    }

    registrar_aula(
        estado,
        turma_id,
        professor_id,
        disciplina_id,
        dia,
        indice
    )


def listar_aulas_alocadas(estado):
    grade = estado["grade"]
    aulas = []

    for turma_id, dias in grade.items():
        for dia, horarios in dias.items():
            for indice, aula in enumerate(horarios):
                if aula is None:
                    continue

                aulas.append({
                    "turma_id": turma_id,
                    "professor_id": aula["professor"],
                    "disciplina_id": aula["disciplina"],
                    "dia": dia,
                    "indice": indice
                })

    return aulas


def imprimir_movimento(
    movimento,
    numero_movimento
):
    print(
        f"AJUSTE {numero_movimento} -> "
        f"Turma {movimento['turma_id']} | "
        f"Disciplina {movimento['disciplina_id']} | "
        f"Professor {movimento['professor_id']} | "
        f"{movimento['dia_origem']} "
        f"aula {movimento['indice_origem'] + 1} "
        f"-> "
        f"{movimento['dia_destino']} "
        f"aula {movimento['indice_destino'] + 1} | "
        f"Penalidade "
        f"{movimento['penalidade_origem']} "
        f"-> "
        f"{movimento['penalidade_destino']}"
    )