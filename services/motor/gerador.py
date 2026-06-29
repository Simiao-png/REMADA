from services.motor.estrutura import criar_grade_vazia
from services.motor.aulas import criar_fila_aulas
from services.motor.alocador import alocar_melhor_posicao
from services.motor.inviabilidade import analisar_inviabilidade


def gerar_grade(resultado):
    analise = analisar_inviabilidade(resultado["dados"])

    if not analise["viavel"]:
        return {
            "grade": None,
            "fila": [],
            "nao_alocadas": [],
            "status": "inviavel",
            "problemas": analise["problemas"]
        }

    configuracao = resultado["dados"]["configuracoes"][0]

    grade = criar_grade_vazia(
        configuracao,
        resultado["turmas"]
    )

    fila = criar_fila_aulas(
        resultado["dados"]["cargas_horarias"]
    )

    nao_alocadas = []

    disponibilidades = resultado["dados"]["disponibilidades"]

    indice = 0

    while indice < len(fila):
        aula = fila[indice]
        aulas_restantes = len(fila) - indice

        quantidade_alocada = alocar_melhor_posicao(
            grade,
            aula,
            disponibilidades,
            aulas_restantes
        )

        if quantidade_alocada == 0:
            nao_alocadas.append(aula)
            indice += 1
        else:
            indice += quantidade_alocada

    return {
        "grade": grade,
        "fila": fila,
        "nao_alocadas": nao_alocadas,
        "status": "ok" if len(nao_alocadas) == 0 else "parcial",
        "problemas": []
    }