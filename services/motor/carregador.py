from models.escola import Escola
from models.professor import Professor
from models.disciplina import Disciplina
from models.turma import Turma
from models.configuracao_horaria import ConfiguracaoHoraria
from models.disponibilidade_professor import DisponibilidadeProfessor
from models.carga_horaria import CargaHoraria
from models.professor_disciplina import ProfessorDisciplina
from models.professor_turma import ProfessorTurma
from models.turma_disciplina import TurmaDisciplina


def carregar_dados_motor():

    dados = {
        "escolas": Escola.query.all(),
        "professores": Professor.query.all(),
        "disciplinas": Disciplina.query.all(),
        "turmas": Turma.query.all(),
        "configuracoes": ConfiguracaoHoraria.query.all(),
        "disponibilidades": DisponibilidadeProfessor.query.all(),
        "cargas_horarias": CargaHoraria.query.all(),
        "professor_disciplina": ProfessorDisciplina.query.all(),
        "professor_turma": ProfessorTurma.query.all(),
        "turma_disciplina": TurmaDisciplina.query.all(),
    }

    print("\n========== DIAGNÓSTICO DO MOTOR ==========")
    print(f"Escolas.................: {len(dados['escolas'])}")
    print(f"Professores.............: {len(dados['professores'])}")
    print(f"Disciplinas.............: {len(dados['disciplinas'])}")
    print(f"Turmas..................: {len(dados['turmas'])}")
    print(f"Configurações...........: {len(dados['configuracoes'])}")
    print(f"Disponibilidades........: {len(dados['disponibilidades'])}")
    print(f"Cargas Horárias.........: {len(dados['cargas_horarias'])}")
    print(f"Professor x Disciplina..: {len(dados['professor_disciplina'])}")
    print(f"Professor x Turma.......: {len(dados['professor_turma'])}")
    print(f"Turma x Disciplina......: {len(dados['turma_disciplina'])}")
    print("==========================================\n")

    professores = {
        professor.id: professor
        for professor in dados["professores"]
    }

    turmas = {
        turma.id: turma
        for turma in dados["turmas"]
    }

    disciplinas = {
        disciplina.id: disciplina
        for disciplina in dados["disciplinas"]
    }

    resumo = {
        "total_escolas": len(dados["escolas"]),
        "total_professores": len(dados["professores"]),
        "total_disciplinas": len(dados["disciplinas"]),
        "total_turmas": len(dados["turmas"]),
        "total_configuracoes": len(dados["configuracoes"]),
        "total_disponibilidades": len(dados["disponibilidades"]),
        "total_cargas_horarias": len(dados["cargas_horarias"]),
        "total_professor_disciplina": len(dados["professor_disciplina"]),
        "total_professor_turma": len(dados["professor_turma"]),
        "total_turma_disciplina": len(dados["turma_disciplina"]),
    }

    return {
        "dados": dados,
        "professores": professores,
        "turmas": turmas,
        "disciplinas": disciplinas,
        "resumo": resumo
    }