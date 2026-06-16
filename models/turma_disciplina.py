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

    def __repr__(self):
        return f"<TurmaDisciplina {self.turma_id} -> {self.disciplina_id}>"