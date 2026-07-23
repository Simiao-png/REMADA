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

    disciplina_id = db.Column(
        db.Integer,
        db.ForeignKey("disciplinas.id"),
        primary_key=True
    )

    criado_em = db.Column(
        db.DateTime,
        server_default=db.func.current_timestamp()
    )

    def __repr__(self):
        return (
            f"<ProfessorTurma "
            f"{self.professor_id} -> "
            f"{self.turma_id} -> "
            f"{self.disciplina_id}>"
        )