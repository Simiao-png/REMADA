from services.motor.carregador import (
    carregar_dados_motor
)

from services.motor.cp_sat.solver import (
    resolver_cp_sat
)

from services.motor.seed import (
    popular_banco,
    popular_duas_turmas
)


def executar_motor():
    resultado = carregar_dados_motor()

    motor = executar_cp_sat(
        resultado
    )

    enriquecer_grade(
        motor,
        resultado
    )

    return motor


def executar_cp_sat(resultado):
    dados = resultado.get(
        "dados",
        {}
    )

    turmas = resultado.get(
        "turmas",
        {}
    )

    return resolver_cp_sat(
        dados,
        turmas
    )


def enriquecer_grade(
    motor,
    resultado
):
    if not isinstance(motor, dict):
        return

    grade = motor.get("grade")

    if not isinstance(grade, dict):
        return

    professores = resultado.get(
        "professores",
        {}
    )

    disciplinas = resultado.get(
        "disciplinas",
        {}
    )

    turmas = resultado.get(
        "turmas",
        {}
    )

    for turma_id, dias_turma in grade.items():
        turma = buscar_por_id(
            turmas,
            turma_id
        )

        turma_nome = obter_atributo(
            turma,
            "nome",
            f"Turma {turma_id}"
        )

        if not isinstance(dias_turma, dict):
            continue

        for horarios in dias_turma.values():
            if not isinstance(horarios, list):
                continue

            for indice, aula in enumerate(
                horarios
            ):
                if not isinstance(aula, dict):
                    continue

                professor_id = aula.get(
                    "professor"
                )

                disciplina_id = aula.get(
                    "disciplina"
                )

                professor = buscar_por_id(
                    professores,
                    professor_id
                )

                disciplina = buscar_por_id(
                    disciplinas,
                    disciplina_id
                )

                professor_nome = obter_atributo(
                    professor,
                    "nome",
                    f"Professor {professor_id}"
                )

                disciplina_nome = obter_atributo(
                    disciplina,
                    "nome",
                    f"Disciplina {disciplina_id}"
                )

                disciplina_cor = obter_cor_disciplina(
                    disciplina
                )

                horarios[indice] = {
                    "turma_id": converter_id(
                        turma_id
                    ),
                    "turma_nome": turma_nome,

                    "professor_id": professor_id,
                    "professor_nome": professor_nome,

                    "disciplina_id": disciplina_id,
                    "disciplina_nome": disciplina_nome,
                    "disciplina_cor": disciplina_cor
                }


def enriquecer_aulas_nao_alocadas(
    aulas,
    resultado
):
    if not isinstance(aulas, list):
        return []

    professores = resultado.get(
        "professores",
        {}
    )

    disciplinas = resultado.get(
        "disciplinas",
        {}
    )

    turmas = resultado.get(
        "turmas",
        {}
    )

    aulas_enriquecidas = []

    for aula in aulas:
        if not isinstance(aula, dict):
            aulas_enriquecidas.append(aula)
            continue

        professor_id = aula.get(
            "professor_id"
        )

        disciplina_id = aula.get(
            "disciplina_id"
        )

        turma_id = aula.get(
            "turma_id"
        )

        professor = buscar_por_id(
            professores,
            professor_id
        )

        disciplina = buscar_por_id(
            disciplinas,
            disciplina_id
        )

        turma = buscar_por_id(
            turmas,
            turma_id
        )

        aulas_enriquecidas.append({
            **aula,

            "professor_nome": obter_atributo(
                professor,
                "nome",
                f"Professor {professor_id}"
            ),

            "disciplina_nome": obter_atributo(
                disciplina,
                "nome",
                f"Disciplina {disciplina_id}"
            ),

            "disciplina_cor": obter_cor_disciplina(
                disciplina
            ),

            "turma_nome": obter_atributo(
                turma,
                "nome",
                f"Turma {turma_id}"
            )
        })

    return aulas_enriquecidas


def buscar_por_id(
    registros,
    registro_id
):
    if registro_id is None:
        return None

    if registro_id in registros:
        return registros[registro_id]

    try:
        registro_id_inteiro = int(
            registro_id
        )

        return registros.get(
            registro_id_inteiro
        )

    except (
        TypeError,
        ValueError
    ):
        return None


def converter_id(valor):
    try:
        return int(valor)

    except (
        TypeError,
        ValueError
    ):
        return valor


def obter_atributo(
    objeto,
    atributo,
    valor_padrao
):
    if objeto is None:
        return valor_padrao

    valor = getattr(
        objeto,
        atributo,
        None
    )

    if valor in (
        None,
        ""
    ):
        return valor_padrao

    return valor


def obter_cor_disciplina(
    disciplina
):
    if disciplina is None:
        return "#e9ecef"

    for atributo in [
        "cor",
        "color",
        "cor_hex"
    ]:
        valor = getattr(
            disciplina,
            atributo,
            None
        )

        if valor:
            return valor

    return "#e9ecef"


def montar_resposta_motor(motor):
    if not isinstance(motor, dict):
        return {
            "status": "erro",
            "grade": None,
            "fila": [],
            "nao_alocadas": [],
            "problemas": [
                {
                    "tipo": "retorno_invalido",
                    "mensagem": (
                        "O motor retornou um formato "
                        "de dados inválido."
                    )
                }
            ]
        }

    return {
        "status": motor.get(
            "status",
            "erro"
        ),
        "status_solver": motor.get(
            "status_solver"
        ),
        "grade": motor.get(
            "grade"
        ),
        "fila": motor.get(
            "fila",
            []
        ),
        "nao_alocadas": motor.get(
            "nao_alocadas",
            []
        ),
        "problemas": motor.get(
            "problemas",
            []
        ),
        "objetivo": motor.get(
            "objetivo"
        ),
        "tempo_segundos": motor.get(
            "tempo_segundos"
        )
    }


def diagnostico_motor():
    try:
        resultado = carregar_dados_motor()

        motor = executar_cp_sat(
            resultado
        )

        enriquecer_grade(
            motor,
            resultado
        )

        motor["nao_alocadas"] = (
            enriquecer_aulas_nao_alocadas(
                motor.get(
                    "nao_alocadas",
                    []
                ),
                resultado
            )
        )

        return montar_resposta_motor(
            motor
        )

    except Exception as erro:
        return {
            "status": "erro",
            "grade": None,
            "fila": [],
            "nao_alocadas": [],
            "problemas": [
                {
                    "tipo": "erro_execucao",
                    "mensagem": str(erro)
                }
            ]
        }


def gerar_motor():
    try:
        resultado = carregar_dados_motor()

        motor = executar_cp_sat(
            resultado
        )

        enriquecer_grade(
            motor,
            resultado
        )

        motor["nao_alocadas"] = (
            enriquecer_aulas_nao_alocadas(
                motor.get(
                    "nao_alocadas",
                    []
                ),
                resultado
            )
        )

        return montar_resposta_motor(
            motor
        )

    except Exception as erro:
        return {
            "status": "erro",
            "grade": None,
            "fila": [],
            "nao_alocadas": [],
            "problemas": [
                {
                    "tipo": "erro_execucao",
                    "mensagem": str(erro)
                }
            ]
        }


def popular_motor():
    resultado = popular_banco()

    return {
        "status": "ok",
        "mensagem": (
            "Banco populado com os dados "
            "de teste."
        ),
        "resultado": resultado
    }


def popular_motor_duas_turmas():
    resultado = popular_duas_turmas()

    return {
        "status": "ok",
        "mensagem": (
            "Banco populado com o cenário "
            "de duas turmas."
        ),
        "resultado": resultado
    }