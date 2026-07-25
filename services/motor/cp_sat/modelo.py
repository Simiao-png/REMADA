from ortools.sat.python import cp_model

from services.motor.cp_sat.variaveis import (
    criar_variaveis
)

from services.motor.cp_sat.restricoes import (
    adicionar_restricoes
)

from services.motor.cp_sat.objetivo import (
    adicionar_objetivo
)


def criar_modelo_cp_sat(dados):
    modelo = cp_model.CpModel()

    variaveis = criar_variaveis(
        modelo,
        dados
    )

    adicionar_restricoes(
        modelo,
        dados,
        variaveis
    )

    adicionar_objetivo(
        modelo,
        dados,
        variaveis
    )

    return {
        "modelo": modelo,
        "variaveis": variaveis
    }