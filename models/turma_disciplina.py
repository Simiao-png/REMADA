from models.db import db


class TurmaDisciplina(db.Model):
    __tablename__ = "turma_disciplina"

    turma_id = db.Column(
        db.Integer,
        db.ForeignKey("turmas.id"),
        primary_key=True
    )

    disciplina_id = db.Column(
        db.Integer,
        db.ForeignKey("disciplinas.id"),
        primary_key=True
    )

    aulas_por_semana = db.Column(
        db.Integer,
        nullable=False,
        default=0
    )

    def __repr__(self):
        return (
            f"<TurmaDisciplina "
            f"{self.turma_id} -> {self.disciplina_id} "
            f"({self.aulas_por_semana} aulas)>"
        )