from flask import Blueprint, jsonify

from services.motor.grade_service import (
    diagnostico_motor,
    gerar_motor,
    popular_motor,
    popular_motor_duas_turmas
)


motor_grade_bp = Blueprint(
    "motor_grade",
    __name__,
    url_prefix="/motor"
)


@motor_grade_bp.route("/diagnostico", methods=["GET"])
def rota_diagnostico():
    return jsonify(
        diagnostico_motor()
    ), 200


@motor_grade_bp.route("/gerar", methods=["POST"])
def gerar():
    resultado = gerar_motor()

    status_http = 200

    if resultado.get("status") == "erro":
        status_http = 422

    return jsonify(
        resultado
    ), status_http


@motor_grade_bp.route("/popular", methods=["POST"])
def popular():
    return jsonify(
        popular_motor()
    ), 201


@motor_grade_bp.route(
    "/popular-duas-turmas",
    methods=["POST"]
)
def popular_duas_turmas():
    return jsonify(
        popular_motor_duas_turmas()
    ), 201