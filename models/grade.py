from models.db import db


class Grade(db.Model):
    __tablename__ = "grades"

    id = db.Column(db.Integer, primary_key=True)

    escola_id = db.Column(
        db.Integer,
        nullable=False
    )

    versao = db.Column(
        db.Integer,
        nullable=False
    )

    status = db.Column(
        db.String(20),
        nullable=False,
        default="ATIVA"
    )

    solver_status = db.Column(
        db.String(20),
        nullable=False
    )

    penalidade = db.Column(
        db.Float,
        nullable=True
    )

    tempo_execucao = db.Column(
        db.Float,
        nullable=True
    )

    total_aulas = db.Column(
        db.Integer,
        nullable=False,
        default=0
    )

    criado_em = db.Column(
        db.DateTime,
        server_default=db.func.current_timestamp()
    )

    aulas = db.relationship(
        "GradeAula",
        backref="grade",
        lazy=True,
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Grade Escola {self.escola_id} - Versão {self.versao}>"