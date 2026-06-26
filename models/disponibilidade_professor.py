from models.db import db


class DisponibilidadeProfessor(db.Model):
    __tablename__ = "disponibilidade_professor"

    id = db.Column(db.Integer, primary_key=True)

    professor_id = db.Column(db.Integer, nullable=False)
    dia_semana = db.Column(db.String(20), nullable=False)
    numero_aula = db.Column(db.Integer, nullable=False)
    disponivel = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f"<DisponibilidadeProfessor {self.professor_id} - {self.dia_semana} - Aula {self.numero_aula}>"