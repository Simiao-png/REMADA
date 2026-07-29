from models.db import db
from models.grade import Grade
from models.grade_aula import GradeAula
from services.motor.carregador import carregar_dados_motor
from services.motor.cp_sat.solver import resolver_cp_sat
from services.motor.seed import popular_banco, popular_duas_turmas


def executar_motor():
    resultado = carregar_dados_motor()
    motor = executar_cp_sat(resultado)
    enriquecer_grade(motor, resultado)
    return motor


def executar_cp_sat(resultado):
    dados = resultado.get("dados", {})
    turmas = resultado.get("turmas", {})
    return resolver_cp_sat(dados, turmas)


def enriquecer_grade(motor, resultado):
    if not isinstance(motor, dict):
        return

    grade = motor.get("grade")
    if not isinstance(grade, dict):
        return

    professores = resultado.get("professores", {})
    disciplinas = resultado.get("disciplinas", {})
    turmas = resultado.get("turmas", {})

    for turma_id, dias_turma in grade.items():
        turma = buscar_por_id(turmas, turma_id)
        turma_nome = obter_atributo(turma, "nome", f"Turma {turma_id}")

        if not isinstance(dias_turma, dict):
            continue

        for horarios in dias_turma.values():
            if not isinstance(horarios, list):
                continue

            for indice, aula in enumerate(horarios):
                if not isinstance(aula, dict):
                    continue

                professor_id = aula.get("professor") or aula.get("professor_id")
                disciplina_id = aula.get("disciplina") or aula.get("disciplina_id")

                professor = buscar_por_id(professores, professor_id)
                disciplina = buscar_por_id(disciplinas, disciplina_id)

                professor_nome = obter_atributo(
                    professor, "nome", f"Professor {professor_id}"
                )
                disciplina_nome = obter_atributo(
                    disciplina, "nome", f"Disciplina {disciplina_id}"
                )
                disciplina_cor = obter_cor_disciplina(disciplina)

                horarios[indice] = {
                    "turma_id": converter_id(turma_id),
                    "turma_nome": turma_nome,
                    "professor_id": professor_id,
                    "professor_nome": professor_nome,
                    "disciplina_id": disciplina_id,
                    "disciplina_nome": disciplina_nome,
                    "disciplina_cor": disciplina_cor,
                }


def enriquecer_aulas_nao_alocadas(aulas, resultado):
    if not isinstance(aulas, list):
        return []

    professores = resultado.get("professores", {})
    disciplinas = resultado.get("disciplinas", {})
    turmas = resultado.get("turmas", {})

    aulas_enriquecidas = []

    for aula in aulas:
        if not isinstance(aula, dict):
            aulas_enriquecidas.append(aula)
            continue

        professor_id = aula.get("professor_id") or aula.get("professor")
        disciplina_id = aula.get("disciplina_id") or aula.get("disciplina")
        turma_id = aula.get("turma_id") or aula.get("turma")

        professor = buscar_por_id(professores, professor_id)
        disciplina = buscar_por_id(disciplinas, disciplina_id)
        turma = buscar_por_id(turmas, turma_id)

        aulas_enriquecidas.append(
            {
                **aula,
                "professor_nome": obter_atributo(
                    professor, "nome", f"Professor {professor_id}"
                ),
                "disciplina_nome": obter_atributo(
                    disciplina, "nome", f"Disciplina {disciplina_id}"
                ),
                "disciplina_cor": obter_cor_disciplina(disciplina),
                "turma_nome": obter_atributo(
                    turma, "nome", f"Turma {turma_id}"
                ),
            }
        )

    return aulas_enriquecidas


def buscar_por_id(registros, registro_id):
    if registro_id is None:
        return None

    if registro_id in registros:
        return registros[registro_id]

    try:
        registro_id_inteiro = int(registro_id)
        return registros.get(registro_id_inteiro)
    except (TypeError, ValueError):
        return None


def converter_id(valor):
    try:
        return int(valor)
    except (TypeError, ValueError):
        return valor


def obter_atributo(objeto, atributo, valor_padrao):
    if objeto is None:
        return valor_padrao

    valor = getattr(objeto, atributo, None)

    if valor in (None, ""):
        return valor_padrao

    return valor


def obter_cor_disciplina(disciplina):
    if disciplina is None:
        return "#4a90e2"

    for atributo in ["cor", "color", "cor_hex"]:
        valor = getattr(disciplina, atributo, None)
        if valor:
            return valor

    return "#4a90e2"


def mapear_dia_para_int(dia_str):
    mapa = {
        "segunda": 1,
        "terca": 2,
        "terça": 2,
        "quarta": 3,
        "quinta": 4,
        "sexta": 5,
        "sabado": 6,
        "sábado": 6,
    }
    return mapa.get(str(dia_str).lower().strip(), 1)


def salvar_grade(motor, resultado):
    if not isinstance(motor, dict):
        return None

    if motor.get("status") == "erro":
        return None

    grade_gerada = motor.get("grade")

    if not isinstance(grade_gerada, dict):
        return None

    turmas = resultado.get("turmas", {})
    escola_id = None

    for turma in turmas.values():
        escola_id = getattr(turma, "escola_id", None)
        if escola_id is not None:
            break

    if escola_id is None:
        escola_id = 1  # Fallback padrao de escola caso nao esteja setado

    ultima_versao = (
        db.session.query(db.func.max(Grade.versao))
        .filter(Grade.escola_id == escola_id)
        .scalar()
        or 0
    )

    total_aulas = 0

    for dias_turma in grade_gerada.values():
        if not isinstance(dias_turma, dict):
            continue

        for horarios in dias_turma.values():
            if not isinstance(horarios, list):
                continue

            total_aulas += sum(
                1 for aula in horarios if isinstance(aula, dict)
            )

    nova_grade = Grade(
        escola_id=escola_id,
        versao=ultima_versao + 1,
        status="ATIVA",
        solver_status=(motor.get("status_solver") or "DESCONHECIDO"),
        penalidade=motor.get("objetivo"),
        tempo_execucao=motor.get("tempo_segundos"),
        total_aulas=total_aulas,
    )

    db.session.add(nova_grade)
    db.session.commit()

    motor["grade_id"] = nova_grade.id
    motor["versao"] = nova_grade.versao

    # GRAVAÇÃO GARANTIDA DE TODAS AS AULAS NA TABELA GRADE_AULAS
    objetos_aulas = []

    for turma_id_key, dias_turma in grade_gerada.items():
        if not isinstance(dias_turma, dict):
            continue

        for dia_nome, horarios in dias_turma.items():
            if not isinstance(horarios, list):
                continue

            dia_int = mapear_dia_para_int(dia_nome)

            for numero_aula_index, aula in enumerate(horarios):
                if not isinstance(aula, dict):
                    continue

                turma_id_val = aula.get("turma_id") or converter_id(turma_id_key)
                disciplina_id_val = aula.get("disciplina_id") or aula.get("disciplina")
                professor_id_val = aula.get("professor_id") or aula.get("professor")

                if turma_id_val and disciplina_id_val and professor_id_val:
                    nova_aula = GradeAula(
                        grade_id=nova_grade.id,
                        turma_id=converter_id(turma_id_val),
                        disciplina_id=converter_id(disciplina_id_val),
                        professor_id=converter_id(professor_id_val),
                        dia_semana=dia_int,
                        numero_aula=numero_aula_index + 1,
                    )
                    objetos_aulas.append(nova_aula)

    if objetos_aulas:
        db.session.add_all(objetos_aulas)
        db.session.commit()

    return nova_grade


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
                    "mensagem": "O motor retornou um formato de dados inválido.",
                }
            ],
        }

    return {
        "status": motor.get("status", "erro"),
        "status_solver": motor.get("status_solver"),
        "grade": motor.get("grade"),
        "grade_id": motor.get("grade_id"),
        "versao": motor.get("versao"),
        "fila": motor.get("fila", []),
        "nao_alocadas": motor.get("nao_alocadas", []),
        "problemas": motor.get("problemas", []),
        "objetivo": motor.get("objetivo"),
        "tempo_segundos": motor.get("tempo_segundos"),
    }


def diagnostico_motor():
    try:
        resultado = carregar_dados_motor()
        motor = executar_cp_sat(resultado)
        enriquecer_grade(motor, resultado)
        motor["nao_alocadas"] = enriquecer_aulas_nao_alocadas(
            motor.get("nao_alocadas", []), resultado
        )
        return montar_resposta_motor(motor)
    except Exception as erro:
        return {
            "status": "erro",
            "grade": None,
            "fila": [],
            "nao_alocadas": [],
            "problemas": [{"tipo": "erro_execucao", "mensagem": str(erro)}],
        }


def gerar_motor():
    try:
        resultado = carregar_dados_motor()
        motor = executar_cp_sat(resultado)
        enriquecer_grade(motor, resultado)
        motor["nao_alocadas"] = enriquecer_aulas_nao_alocadas(
            motor.get("nao_alocadas", []), resultado
        )
        salvar_grade(motor, resultado)
        return montar_resposta_motor(motor)
    except Exception as erro:
        db.session.rollback()
        return {
            "status": "erro",
            "grade": None,
            "fila": [],
            "nao_alocadas": [],
            "problemas": [{"tipo": "erro_execucao", "mensagem": str(erro)}],
        }


def popular_motor():
    resultado = popular_banco()
    return {
        "status": "ok",
        "mensagem": "Banco populado com os dados de teste.",
        "resultado": resultado,
    }


def popular_motor_duas_turmas():
    resultado = popular_duas_turmas()
    return {
        "status": "ok",
        "mensagem": "Banco populado com o cenário de duas turmas.",
        "resultado": resultado,
    }