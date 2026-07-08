from flask import Blueprint, request, render_template
from services.professor_service import (
    listar_professores,
    buscar_professor,
    criar_professor,
    atualizar_professor,
    deletar_professor
)

professor_bp = Blueprint("professor", __name__)

# --- ROTA PARA A INTERFACE WEB ---
@professor_bp.route("/professores/tela", methods=["GET"])
def tela_professores():
    resposta = listar_professores()
    professores_dados = []
    
    # Extrai os dados do formato de resposta do service
    if hasattr(resposta, "get_json"):
        professores_dados = resposta.get_json()
    elif isinstance(resposta, list):
        professores_dados = resposta
        
    return render_template("professores.html", professores=professores_dados)


# --- ROTAS DA API (MANTIDAS COMO ESTAVAM) ---
@professor_bp.route("/professores", methods=["GET"])
def listar():
    return listar_professores()

@professor_bp.route("/professores/<int:id>", methods=["GET"])
def buscar(id):
    return buscar_professor(id)

@professor_bp.route("/professores", methods=["POST"])
def criar():
    return criar_professor(request.get_json())

@professor_bp.route("/professores/<int:id>", methods=["PUT"])
def atualizar(id):
    return atualizar_professor(id, request.get_json())

@professor_bp.route("/professores/<int:id>", methods=["DELETE"])
def deletar(id):
    return deletar_professor(id)