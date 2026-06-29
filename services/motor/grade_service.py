from services.motor.carregador import carregar_dados_motor
from services.motor.gerador import gerar_grade
from services.motor.seed import popular_banco, popular_duas_turmas


def diagnostico_motor():

    resultado = carregar_dados_motor()

    motor = gerar_grade(resultado)

    return {
        "status": motor["status"],
        "grade": motor["grade"],
        "nao_alocadas": motor["nao_alocadas"],
        "problemas": motor.get("problemas", [])
    }


def popular_motor():
    return popular_banco()


def popular_motor_duas_turmas():
    return popular_duas_turmas()