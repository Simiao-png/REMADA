from models.escola import Escola
from models.professor import Professor
from models.disciplina import Disciplina
from models.turma import Turma
from models.configuracao_horaria import (
    ConfiguracaoHoraria
)
from models.disponibilidade_professor import (
    DisponibilidadeProfessor
)
from models.professor_disciplina import (
    ProfessorDisciplina
)
from models.professor_turma import (
    ProfessorTurma
)
from models.turma_disciplina import (
    TurmaDisciplina
)


def carregar_dados_motor():
    dados = {
        "escolas": Escola.query.all(),
        "professores": Professor.query.all(),
        "disciplinas": Disciplina.query.all(),
        "turmas": Turma.query.all(),
        "configuracoes": ConfiguracaoHoraria.query.all(),
        "disponibilidades": (
            DisponibilidadeProfessor.query.all()
        ),
        "professor_disciplina": (
            ProfessorDisciplina.query.all()
        ),
        "professor_turma": (
            ProfessorTurma.query.all()
        ),
        "turma_disciplina": (
            TurmaDisciplina.query.all()
        )
    }

    print(
        "\n========== DIAGNÓSTICO DO MOTOR =========="
    )
    print(
        f"Escolas.................: "
        f"{len(dados['escolas'])}"
    )
    print(
        f"Professores.............: "
        f"{len(dados['professores'])}"
    )
    print(
        f"Disciplinas.............: "
        f"{len(dados['disciplinas'])}"
    )
    print(
        f"Turmas..................: "
        f"{len(dados['turmas'])}"
    )
    print(
        f"Configurações...........: "
        f"{len(dados['configuracoes'])}"
    )
    print(
        f"Disponibilidades........: "
        f"{len(dados['disponibilidades'])}"
    )
    print(
        f"Professor x Disciplina..: "
        f"{len(dados['professor_disciplina'])}"
    )
    print(
        f"Professor x Turma.......: "
        f"{len(dados['professor_turma'])}"
    )
    print(
        f"Turma x Disciplina......: "
        f"{len(dados['turma_disciplina'])}"
    )
    print(
        "==========================================\n"
    )

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

    configuracoes = {
        configuracao.id: configuracao
        for configuracao in dados["configuracoes"]
    }

    resumo = {
        "total_escolas": len(
            dados["escolas"]
        ),
        "total_professores": len(
            dados["professores"]
        ),
        "total_disciplinas": len(
            dados["disciplinas"]
        ),
        "total_turmas": len(
            dados["turmas"]
        ),
        "total_configuracoes": len(
            dados["configuracoes"]
        ),
        "total_disponibilidades": len(
            dados["disponibilidades"]
        ),
        "total_professor_disciplina": len(
            dados["professor_disciplina"]
        ),
        "total_professor_turma": len(
            dados["professor_turma"]
        ),
        "total_turma_disciplina": len(
            dados["turma_disciplina"]
        )
    }

    return {
        "dados": dados,
        "professores": professores,
        "turmas": turmas,
        "disciplinas": disciplinas,
        "configuracoes": configuracoes,
        "resumo": resumo
    }