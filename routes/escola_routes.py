from flask import Blueprint, request, render_template
from services.escola_service import (
    listar_escolas,
    buscar_escola,
    criar_escola,
    atualizar_escola,
    deletar_escola
)

escola_bp = Blueprint("escola", __name__)

# --- ROTA PARA A INTERFACE WEB ---
@escola_bp.route("/escolas/tela", methods=["GET"], endpoint="tela_escolas")
def tela_escolas():
    resposta = listar_escolas()
    escolas_dados = []
    
    if hasattr(resposta, "get_json"):
        escolas_dados = resposta.get_json()
    elif isinstance(resposta, list):
        escolas_dados = resposta
        
    # Como queremos os dados de "UMA" escola para o perfil:
    # Se houver alguma escola no banco, pegamos a primeira (#0). Caso contrário, None.
    escola_selecionada = escolas_dados[0] if escolas_dados else None
    
    return render_template("escolas.html", escola=escola_selecionada)


# --- ROTAS DA API (MANTIDAS EXATAMENTE COMO ESTAVAM) ---
@escola_bp.route("/escolas", methods=["GET"])
def listar():
    return listar_escolas()

@escola_bp.route("/escolas/<int:id>", methods=["GET"])
def buscar(id):
    return buscar_escola(id)

@escola_bp.route("/escolas", methods=["POST"])
def criar():
    return criar_escola(request.get_json())

@escola_bp.route("/escolas/<int:id>", methods=["PUT"])
def atualizar(id):
    return atualizar_escola(id, request.get_json())

@escola_bp.route("/escolas/<int:id>", methods=["DELETE"])
def deletar(id):
    return deletar_escola(id)