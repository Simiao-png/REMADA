from flask import Blueprint
from models.turma_disciplina import TurmaDisciplina

turma_disciplina_bp = Blueprint(
    "turma_disciplina",
    __name__
)


@turma_disciplina_bp.route("/turma-disciplinas")
def listar_turma_disciplinas():
    registros = TurmaDisciplina.query.all()

    html = "<h1>Turma x Disciplina</h1>"

    for registro in registros:
        html += f"""
        <p>
            Turma ID: {registro.turma_id}<br>
            Disciplina ID: {registro.disciplina_id}
        </p>
        <hr>
        """

    return html