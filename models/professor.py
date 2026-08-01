from models.db import db


class Professor(db.Model):
    __tablename__ = "professores"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    escola_id = db.Column(
        db.Integer,
        nullable=False
    )

    nome = db.Column(
        db.String(150),
        nullable=False
    )

    disciplina_principal_id = db.Column(
        db.Integer,
        db.ForeignKey("disciplinas.id"),
        nullable=True
    )

    limite_aulas_semana = db.Column(
        db.Integer,
        nullable=True
    )

    ativo = db.Column(
        db.Boolean,
        default=True,
        nullable=False
    )

    trabalha_outra_escola = db.Column(
        db.Boolean,
        default=False,
        nullable=False
    )

    observacoes = db.Column(
        db.Text
    )

    criado_em = db.Column(
        db.DateTime,
        server_default=db.func.current_timestamp()
    )

    disciplina_principal = db.relationship(
        "Disciplina",
        foreign_keys=[disciplina_principal_id],
        lazy="joined"
    )

    disciplinas = db.relationship(
        "Disciplina",
        secondary="professor_disciplina",
        lazy="joined"
    )

    segmentos = db.relationship(
        "ProfessorSegmento",
        cascade="all, delete-orphan",
        lazy="joined"
    )

    def __repr__(self):
        return f"<Professor {self.nome}>"