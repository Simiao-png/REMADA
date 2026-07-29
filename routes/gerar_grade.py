from flask import Blueprint, render_template, request

from models.grade import Grade
from models.grade_aula import GradeAula

gerar_grade_bp = Blueprint("gerar_grade", __name__)


@gerar_grade_bp.route("/gerar-grade")
def tela_gerar_grade():
    grade_id = request.args.get("id", type=int)

    grade_dict = None
    aulas_list = []

    if grade_id:
        grade = Grade.query.get_or_404(grade_id)

        # Busca todas as aulas sem tentar ordenar por atributos que podem ter nomes diferentes no model
        aulas = GradeAula.query.filter_by(grade_id=grade.id).all()

        grade_dict = {
            "id": grade.id,
            "versao": grade.versao,
            "penalidade": grade.penalidade,
            "tempo_execucao": grade.tempo_execucao
        }

        # Converte os objetos GradeAula tratando com seguranca cada campo
        for a in aulas:
            # Pega o dia (seja 'dia' ou 'dia_semana') sem dar erro
            dia_val = getattr(a, 'dia', getattr(a, 'dia_semana', ''))
            # Pega a aula (seja 'aula' ou 'numero_aula')
            aula_val = getattr(a, 'aula', getattr(a, 'numero_aula', 1))

            aulas_list.append({
                "turma_id": a.turma_id,
                "turma_nome": a.turma.nome if (hasattr(a, 'turma') and a.turma) else f"Turma {a.turma_id}",
                "dia": dia_val,
                "aula": aula_val,
                "disciplina_id": a.disciplina_id,
                "disciplina_nome": a.disciplina.nome if (hasattr(a, 'disciplina') and a.disciplina) else f"Disc {a.disciplina_id}",
                "professor_id": a.professor_id,
                "professor_nome": a.professor.nome if (hasattr(a, 'professor') and a.professor) else "A definir"
            })

    # Envia os dados prontos para o HTML/JS
    return render_template(
        "gerar_grade.html",
        grade_json=grade_dict,
        aulas_json=aulas_list
    )