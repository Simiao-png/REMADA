from app import app
from models.db import db
from models.escola import Escola
from models.disciplina import Disciplina

DISCIPLINAS_PADRAO = [
    {"nome": "Língua Portuguesa", "cor": "#e11d48"},
    {"nome": "Matemática", "cor": "#2563eb"},
    {"nome": "História", "cor": "#b45309"},
    {"nome": "Geografia", "cor": "#d97706"},
    {"nome": "Ciências", "cor": "#059669"},
    {"nome": "Física", "cor": "#ea580c"},
    {"nome": "Química", "cor": "#7c3aed"},
    {"nome": "Biologia", "cor": "#15803d"},
    {"nome": "Língua Inglesa", "cor": "#0284c7"},
    {"nome": "Educação Física", "cor": "#16a34a"},
    {"nome": "Arte", "cor": "#db2777"},
    {"nome": "Filosofia", "cor": "#475569"},
    {"nome": "Sociologia", "cor": "#0d9488"},
    {"nome": "Espanhol", "cor": "#3b82f6"},
]

def restaurar_disciplinas():
    with app.app_context():
        # Pega a primeira escola ou a ativa
        escola = Escola.query.first()
        if not escola:
            print("Nenhuma escola encontrada.")
            return

        criadas = 0
        for item in DISCIPLINAS_PADRAO:
            existente = Disciplina.query.filter_by(
                escola_id=escola.id, 
                nome=item["nome"]
            ).first()

            if not existente:
                nova = Disciplina(
                    escola_id=escola.id,
                    nome=item["nome"],
                    cor=item["cor"]
                )
                db.session.add(nova)
                criadas += 1

        db.session.commit()
        print(f"Sucesso! {criadas} disciplinas cadastradas para a escola ID {escola.id}.")

if __name__ == "__main__":
    restaurar_disciplinas()