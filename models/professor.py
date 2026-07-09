from models.db import db


class Professor(db.Model):
    __tablename__ = "professores"

    id = db.Column(db.Integer, primary_key=True)
    escola_id = db.Column(db.Integer, nullable=False)

    nome = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150))
    telefone = db.Column(db.String(30))

    ativo = db.Column(db.Boolean, default=True)
    trabalha_outra_escola = db.Column(db.Boolean, default=False)

    observacoes = db.Column(db.Text)

    criado_em = db.Column(
        db.DateTime,
        server_default=db.func.current_timestamp()
    )

    disciplinas = db.relationship(
        "Disciplina",
        secondary="professor_disciplina",
        lazy="joined"
    )

    def __repr__(self):
        return f"<Professor {self.nome}>"