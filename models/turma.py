from models.db import db


class Turma(db.Model):
    __tablename__ = "turmas"

    id = db.Column(db.Integer, primary_key=True)

    escola_id = db.Column(db.Integer, nullable=False)
    configuracao_horaria_id = db.Column(db.Integer, nullable=False)

    nome = db.Column(db.String(50), nullable=False)
    serie = db.Column(db.String(50), nullable=False)
    turno = db.Column(db.String(30), nullable=False)

    ativo = db.Column(db.Boolean, default=True)

    criado_em = db.Column(
        db.DateTime,
        server_default=db.func.current_timestamp()
    )

    def __repr__(self):
        return f"<Turma {self.nome}>"