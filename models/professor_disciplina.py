from models.db import db


class ProfessorDisciplina(db.Model):
    __tablename__ = "professor_disciplina"

    id = db.Column(db.Integer, primary_key=True)

    professor_id = db.Column(
        db.Integer,
        nullable=False
    )

    disciplina_id = db.Column(
        db.Integer,
        nullable=False
    )

    criado_em = db.Column(
        db.DateTime,
        server_default=db.func.current_timestamp()
    )

    def __repr__(self):
        return f"<ProfessorDisciplina {self.professor_id} -> {self.disciplina_id}>"