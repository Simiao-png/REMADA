from services.motor.estrutura import (
    criar_grade_vazia
)

from services.motor.guloso.aulas import (
    criar_fila_aulas
)

from services.motor.guloso.alocador import (
    alocar_melhor_posicao
)

from services.motor.inviabilidade import (
    analisar_inviabilidade
)

from services.motor.guloso.estado import (
    criar_estado
)


def mesma_aula(aula_1, aula_2):
    return (
        aula_1["turma_id"] == aula_2["turma_id"]
        and
        aula_1["disciplina_id"] == aula_2["disciplina_id"]
        and
        aula_1["professor_id"] == aula_2["professor_id"]
    )


def contar_aulas_iguais_restantes(
    fila,
    indice
):
    aula_atual = fila[indice]
    quantidade = 0

    for posicao in range(
        indice,
        len(fila)
    ):
        if not mesma_aula(
            aula_atual,
            fila[posicao]
        ):
            break

        quantidade += 1

    return quantidade


def gerar_grade(resultado):
    dados = resultado["dados"]

    analise = analisar_inviabilidade(
        dados
    )

    if not analise["viavel"]:
        return {
            "grade": None,
            "fila": [],
            "nao_alocadas": [],
            "status": "inviavel",
            "problemas": analise["problemas"]
        }

    configuracoes = dados.get(
        "configuracoes",
        []
    )

    turmas = resultado.get(
        "turmas",
        {}
    )

    disponibilidades = dados.get(
        "disponibilidades",
        []
    )

    grade = criar_grade_vazia(
        configuracoes,
        turmas
    )

    estado = criar_estado(
        grade
    )

    fila = criar_fila_aulas(
        dados.get(
            "turma_disciplina",
            []
        ),
        dados.get(
            "professor_turma",
            []
        ),
        disponibilidades
    )

    nao_alocadas = []
    indice = 0

    while indice < len(fila):
        aula = fila[indice]

        if aula["professor_id"] is None:
            nao_alocadas.append({
                **aula,
                "motivo": (
                    "Nenhum professor atribuído "
                    "para esta turma e disciplina."
                )
            })

            indice += 1
            continue

        aulas_iguais_restantes = (
            contar_aulas_iguais_restantes(
                fila,
                indice
            )
        )

        quantidade_alocada = (
            alocar_melhor_posicao(
                estado,
                aula,
                disponibilidades,
                aulas_iguais_restantes
            )
        )

        if quantidade_alocada == 0:
            nao_alocadas.append({
                **aula,
                "motivo": (
                    "Nenhuma posição válida "
                    "encontrada."
                )
            })

            indice += 1
        else:
            indice += quantidade_alocada

    status = (
        "ok"
        if len(nao_alocadas) == 0
        else "parcial"
    )

    return {
        "grade": grade,
        "fila": fila,
        "nao_alocadas": nao_alocadas,
        "status": status,
        "problemas": []
    }