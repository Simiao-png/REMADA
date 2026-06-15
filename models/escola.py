from models.db import db


class Escola(db.Model):
    __tablename__ = "escolas"

    id = db.Column(db.Integer, primary_key=True)

    nome = db.Column(db.String(150), nullable=False)
    cidade = db.Column(db.String(100))
    estado = db.Column(db.String(50))

    ativo = db.Column(db.Boolean, default=True)

    criado_em = db.Column(
        db.DateTime,
        server_default=db.func.current_timestamp()
    )

    def __repr__(self):
        return f"<Escola {self.nome}>"