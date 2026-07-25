from flask import Blueprint, render_template


gerar_grade_bp = Blueprint(
    "gerar_grade",
    __name__
)


@gerar_grade_bp.route("/gerar-grade")
def tela_gerar_grade():
    return render_template("gerar_grade.html")