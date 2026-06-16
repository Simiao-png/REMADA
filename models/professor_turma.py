from models.db import db


class ProfessorTurma(db.Model):
    __tablename__ = "professor_turma"

    professor_id = db.Column(
        db.Integer,
        db.ForeignKey("professores.id"),
        primary_key=True
    )

    turma_id = db.Column(
        db.Integer,
        db.ForeignKey("turmas.id"),
        primary_key=True
    )

    def __repr__(self):
        return f"<ProfessorTurma {self.professor_id} -> {self.turma_id}>"