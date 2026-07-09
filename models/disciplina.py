from models.db import db


class Disciplina(db.Model):
    __tablename__ = "disciplinas"

    id = db.Column(db.Integer, primary_key=True)
    escola_id = db.Column(db.Integer, nullable=False)

    nome = db.Column(db.String(100), nullable=False)
    cor = db.Column(db.String(7), default="#2563EB")
    ativo = db.Column(db.Boolean, default=True)

    criado_em = db.Column(
        db.DateTime,
        server_default=db.func.current_timestamp()
    )

    def __repr__(self):
        return f"<Disciplina {self.nome}>"