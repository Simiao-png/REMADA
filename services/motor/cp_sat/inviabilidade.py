from ortools.sat.python import cp_model
from services.motor.carregador import carregar_dados
from services.motor.cp_sat.variaveis import criar_variaveis
from services.motor.cp_sat.restricoes import (
    adicionar_carga_horaria_semanal,
    adicionar_limite_por_horario_da_turma,
    adicionar_limite_por_horario_do_professor,
    adicionar_disponibilidade_professor,
    adicionar_limite_disciplina_por_dia
)


def executar_diagnostico_passo_a_passo():
    """
    Carrega os dados via carregador.py e testa cada restrição incrementalmente no CP-SAT.
    """
    # Carrega os dados direto da base
    dados = carregar_dados()

    print("\n========== DIAGNÓSTICO INCREMENTAL CP-SAT ==========")

    # Teste 1: Carga Horária Semanal
    m1 = cp_model.CpModel()
    v1 = criar_variaveis(m1, dados)
    adicionar_carga_horaria_semanal(m1, dados, v1)
    s1 = cp_model.CpSolver()
    s1.parameters.max_time_in_seconds = 5
    r1 = s1.Solve(m1)
    print(f"1. Apenas Carga Horária Semanal: {s1.StatusName(r1)}")
    if r1 == cp_model.INFEASIBLE:
        return "GARGALO 1: A carga horária semanal cadastrada excede a capacidade física das turmas."

    # Teste 2: + Limite de Horário da Turma
    m2 = cp_model.CpModel()
    v2 = criar_variaveis(m2, dados)
    adicionar_carga_horaria_semanal(m2, dados, v2)
    adicionar_limite_por_horario_da_turma(m2, v2)
    s2 = cp_model.CpSolver()
    s2.parameters.max_time_in_seconds = 5
    r2 = s2.Solve(m2)
    print(f"2. + Limite de Horário da Turma: {s2.StatusName(r2)}")
    if r2 == cp_model.INFEASIBLE:
        return "GARGALO 2: Turmas possuem mais aulas cadastradas do que slots de horários ativos na semana."

    # Teste 3: + Limite de Horário do Professor
    m3 = cp_model.CpModel()
    v3 = criar_variaveis(m3, dados)
    adicionar_carga_horaria_semanal(m3, dados, v3)
    adicionar_limite_por_horario_da_turma(m3, v3)
    adicionar_limite_por_horario_do_professor(m3, v3)
    s3 = cp_model.CpSolver()
    s3.parameters.max_time_in_seconds = 5
    r3 = s3.Solve(m3)
    print(f"3. + Limite por Horário do Professor: {s3.StatusName(r3)}")
    if r3 == cp_model.INFEASIBLE:
        return "GARGALO 3: Choque de horários entre professores compartilhados em turmas simultâneas."

    # Teste 4: + Disponibilidade dos Professores
    m4 = cp_model.CpModel()
    v4 = criar_variaveis(m4, dados)
    adicionar_carga_horaria_semanal(m4, dados, v4)
    adicionar_limite_por_horario_da_turma(m4, v4)
    adicionar_limite_por_horario_do_professor(m4, v4)
    adicionar_disponibilidade_professor(m4, dados, v4)
    s4 = cp_model.CpSolver()
    s4.parameters.max_time_in_seconds = 5
    r4 = s4.Solve(m4)
    print(f"4. + Disponibilidade dos Professores: {s4.StatusName(r4)}")
    if r4 == cp_model.INFEASIBLE:
        return "GARGALO 4: As janelas de disponibilidade cadastradas para os professores são insuficientes."

    # Teste 5: + Limite de Disciplina por Dia
    m5 = cp_model.CpModel()
    v5 = criar_variaveis(m5, dados)
    adicionar_carga_horaria_semanal(m5, dados, v5)
    adicionar_limite_por_horario_da_turma(m5, v5)
    adicionar_limite_por_horario_do_professor(m5, v5)
    adicionar_disponibilidade_professor(m5, dados, v5)
    adicionar_limite_disciplina_por_dia(m5, v5)
    s5 = cp_model.CpSolver()
    s5.parameters.max_time_in_seconds = 5
    r5 = s5.Solve(m5)
    print(f"5. + Limite de Disciplina por Dia: {s5.StatusName(r5)}")
    if r5 == cp_model.INFEASIBLE:
        return "GARGALO 5: A trava de máximo de aulas da mesma disciplina por dia impede alocar a carga semanal."

    print("====================================================\n")
    return "Todas as restrições individuais passaram."