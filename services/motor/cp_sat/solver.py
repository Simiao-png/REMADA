from ortools.sat.python import cp_model

from services.motor.cp_sat.modelo import (
    criar_modelo_cp_sat
)

from services.motor.cp_sat.extrator import (
    extrair_grade
)

from services.motor.cp_sat.diagnostico import (
    montar_diagnostico
)


TEMPO_MAXIMO_SEGUNDOS = 30
NUMERO_TRABALHADORES = 8


def resolver_cp_sat(
    dados,
    turmas
):
    resultado_modelo = criar_modelo_cp_sat(
        dados
    )

    modelo = resultado_modelo["modelo"]
    variaveis = resultado_modelo["variaveis"]

    solver = cp_model.CpSolver()

    solver.parameters.max_time_in_seconds = (
        TEMPO_MAXIMO_SEGUNDOS
    )

    solver.parameters.num_search_workers = (
        NUMERO_TRABALHADORES
    )

    status = solver.Solve(
        modelo
    )

    nome_status = solver.StatusName(
        status
    )

    print(
        "\n========== RESULTADO CP-SAT =========="
    )

    print(
        f"Status: {nome_status}"
    )

    if status in (
        cp_model.OPTIMAL,
        cp_model.FEASIBLE
    ):
        print(
            f"Objetivo: "
            f"{solver.ObjectiveValue()}"
        )

        print(
            f"Tempo: "
            f"{solver.WallTime():.2f} segundo(s)"
        )

        print(
            "=======================================\n"
        )

        grade = extrair_grade(
            solver,
            variaveis,
            dados,
            turmas
        )

        return {
            "grade": grade,
            "status": (
                "otimo"
                if status == cp_model.OPTIMAL
                else "viavel"
            ),
            "status_solver": nome_status,
            "objetivo": solver.ObjectiveValue(),
            "tempo_segundos": solver.WallTime(),
            "problemas": []
        }

    print(
        f"Tempo: "
        f"{solver.WallTime():.2f} segundo(s)"
    )

    print(
        "=======================================\n"
    )

    diagnostico = montar_diagnostico(
        status,
        dados,
        turmas
    )

    return {
        "grade": None,
        "status": "inviavel",
        "status_solver": nome_status,
        "objetivo": None,
        "tempo_segundos": solver.WallTime(),
        "problemas": diagnostico
    }