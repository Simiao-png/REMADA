from flask import Blueprint, render_template, request
from models.grade import Grade
from models.grade_aula import GradeAula

ver_grade_bp = Blueprint("ver_grade", __name__)


@ver_grade_bp.route("/ver-grade")
def tela_ver_grade():
    grade_id = request.args.get("id", type=int)

    if not grade_id:
        return "ID da grade não fornecido.", 400

    grade = Grade.query.get_or_404(grade_id)
    aulas = GradeAula.query.filter_by(grade_id=grade.id).all()

    grade_dict = {
        "id": grade.id,
        "versao": grade.versao,
        "penalidade": grade.penalidade,
        "tempo_execucao": grade.tempo_execucao,
        "criado_em": (
            grade.criado_em.strftime("%d/%m/%Y às %H:%M")
            if hasattr(grade, "criado_em") and grade.criado_em
            else ""
        ),
    }

    aulas_list = []
    for a in aulas:
        dia_val = getattr(a, "dia_semana", getattr(a, "dia", 1))
        aula_val = getattr(a, "numero_aula", getattr(a, "aula", 1))

        disc_nome = f"Disciplina {a.disciplina_id}"
        disc_cor = "#4a90e2"
        if hasattr(a, "disciplina") and a.disciplina:
            disc_nome = getattr(a.disciplina, "nome", disc_nome)
            disc_cor = getattr(
                a.disciplina,
                "cor",
                getattr(
                    a.disciplina,
                    "color",
                    getattr(a.disciplina, "cor_hex", "#4a90e2"),
                ),
            )

        turma_nome = f"Turma {a.turma_id}"
        if hasattr(a, "turma") and a.turma:
            turma_nome = getattr(a.turma, "nome", turma_nome)

        prof_nome = "A definir"
        if hasattr(a, "professor") and a.professor:
            prof_nome = getattr(a.professor, "nome", prof_nome)

        aulas_list.append(
            {
                "turma_id": a.turma_id,
                "turma_nome": turma_nome,
                "dia_semana": dia_val,
                "numero_aula": aula_val,
                "disciplina_id": a.disciplina_id,
                "disciplina_nome": disc_nome,
                "disciplina_cor": disc_cor,
                "professor_id": a.professor_id,
                "professor_nome": prof_nome,
            }
        )

    return render_template(
        "ver_grade.html", grade=grade_dict, aulas=aulas_list
    )