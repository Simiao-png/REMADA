from werkzeug.security import check_password_hash, generate_password_hash
from models.db import db


class Usuario(db.Model):
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha_hash = db.Column(db.String(255), nullable=False)
    escola_id = db.Column(
        db.Integer, db.ForeignKey("escolas.id"), nullable=True
    )

    # Relacionamento para acessar os dados da escola direto pelo usuario
    escola = db.relationship("Escola", backref="usuarios")

    def set_senha(self, senha):
        self.senha_hash = generate_password_hash(senha)

    def checar_senha(self, senha):
        return check_password_hash(self.senha_hash, senha)