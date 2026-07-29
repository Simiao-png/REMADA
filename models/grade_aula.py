from models.db import db


class GradeAula(db.Model):
    __tablename__ = "grade_aulas"

    id = db.Column(db.Integer, primary_key=True)

    grade_id = db.Column(
        db.Integer,
        db.ForeignKey("grades.id"),
        nullable=False
    )

    turma_id = db.Column(
        db.Integer,
        db.ForeignKey("turmas.id"),
        nullable=False
    )

    disciplina_id = db.Column(
        db.Integer,
        db.ForeignKey("disciplinas.id"),
        nullable=False
    )

    professor_id = db.Column(
        db.Integer,
        db.ForeignKey("professores.id"),
        nullable=False
    )

    dia_semana = db.Column(
        db.Integer,
        nullable=False
    )

    numero_aula = db.Column(
        db.Integer,
        nullable=False
    )

    criado_em = db.Column(
        db.DateTime,
        server_default=db.func.current_timestamp()
    )

    def __repr__(self):
        return (
            f"<GradeAula Grade {self.grade_id} - "
            f"Turma {self.turma_id} - "
            f"Dia {self.dia_semana} - "
            f"Aula {self.numero_aula}>"
        )