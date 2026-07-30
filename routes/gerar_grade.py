from flask import Blueprint, jsonify, render_template, request

from models.db import db
from models.grade import Grade
from models.grade_aula import GradeAula

gerar_grade_bp = Blueprint("gerar_grade", __name__)


@gerar_grade_bp.route("/gerar-grade", methods=["GET"])
def tela_gerar_grade():
    grade_id = request.args.get("id", type=int)

    grade_dict = {
        "id": "",
        "versao": "Nova",
        "penalidade": 0,
        "tempo_execucao": 0
    }
    aulas_list = []

    if grade_id:
        grade = Grade.query.get(grade_id)
        if grade:
            aulas = GradeAula.query.filter_by(grade_id=grade.id).all()

            grade_dict = {
                "id": grade.id,
                "versao": getattr(grade, "versao", 1),
                "penalidade": getattr(grade, "penalidade", 0),
                "tempo_execucao": getattr(grade, "tempo_execucao", 0),
            }

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
        "gerar_grade.html",
        grade=grade_dict,
        grade_id=grade_id,
        grade_json=grade_dict,
        aulas_json=aulas_list
    )


@gerar_grade_bp.route("/motor/grade/<int:grade_id>", methods=["DELETE"])
def deletar_grade(grade_id):
    try:
        grade = Grade.query.get(grade_id)
        if not grade:
            return (
                jsonify(
                    {"status": "erro", "mensagem": "Grade não encontrada."}
                ),
                404,
            )

        GradeAula.query.filter_by(grade_id=grade.id).delete()
        db.session.delete(grade)
        db.session.commit()

        return (
            jsonify(
                {
                    "status": "sucesso",
                    "mensagem": "Grade excluída com sucesso.",
                }
            ),
            200,
        )

    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "erro", "mensagem": str(e)}), 500