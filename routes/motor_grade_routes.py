from flask import Blueprint, jsonify, request
from models.db import db
from models.grade import Grade
from models.grade_aula import GradeAula
from services.motor.gerador import diagnostico_motor, gerar_motor

motor_grade_bp = Blueprint("motor_grade", __name__)


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


@motor_grade_bp.route("/motor/gerar", methods=["POST"])
def gerar_grade_motor():
    try:
        # Executa o motor OR-Tools
        resposta = gerar_motor()

        # Se o motor gerou a grade com sucesso ou parcialmente
        if (
            resposta
            and isinstance(resposta, dict)
            and resposta.get("status") in ["ok", "parcial", "sucesso"]
        ):

            grade_id = resposta.get("grade_id")
            grade_gerada = resposta.get("grade")

            if grade_id and isinstance(grade_gerada, dict):
                # Limpa aulas antigas dessa grade se existirem
                GradeAula.query.filter_by(grade_id=grade_id).delete()

                objetos_aulas = []

                for turma_id, dias_turma in grade_gerada.items():
                    if not isinstance(dias_turma, dict):
                        continue

                    for dia_nome, horarios in dias_turma.items():
                        if not isinstance(horarios, list):
                            continue

                        dia_int = mapear_dia_para_int(dia_nome)

                        for numero_aula_index, aula in enumerate(horarios):
                            if not isinstance(aula, dict):
                                continue

                            # Extrai IDs de forma segura
                            t_id = aula.get("turma_id") or turma_id
                            d_id = aula.get("disciplina_id") or aula.get(
                                "disciplina"
                            )
                            p_id = aula.get("professor_id") or aula.get(
                                "professor"
                            )

                            try:
                                t_id = int(t_id) if t_id else None
                                d_id = int(d_id) if d_id else None
                                p_id = int(p_id) if p_id else None
                            except (ValueError, TypeError):
                                pass

                            if t_id and d_id and p_id:
                                nova_aula = GradeAula(
                                    grade_id=grade_id,
                                    turma_id=t_id,
                                    disciplina_id=d_id,
                                    professor_id=p_id,
                                    dia_semana=dia_int,
                                    numero_aula=numero_aula_index + 1,
                                )
                                objetos_aulas.append(nova_aula)

                if objetos_aulas:
                    db.session.add_all(objetos_aulas)
                    db.session.commit()

        return jsonify(resposta), 200

    except Exception as e:
        db.session.rollback()
        return (
            jsonify(
                {
                    "status": "erro",
                    "mensagem": f"Erro ao processar e salvar a grade: {str(e)}",
                }
            ),
            500,
        )


@motor_grade_bp.route("/motor/diagnostico", methods=["GET"])
def diagnostico_motor_route():
    try:
        resposta = diagnostico_motor()
        return jsonify(resposta), 200
    except Exception as e:
        return jsonify({"status": "erro", "mensagem": str(e)}), 500