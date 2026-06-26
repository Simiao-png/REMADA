from flask import Blueprint, jsonify

from services.motor.grade_service import (
    diagnostico_motor,
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
    return jsonify(diagnostico_motor()), 200


@motor_grade_bp.route("/popular", methods=["POST"])
def popular():
    return jsonify(popular_motor()), 201


@motor_grade_bp.route("/popular-duas-turmas", methods=["POST"])
def popular_duas_turmas():
    return jsonify(popular_motor_duas_turmas()), 201