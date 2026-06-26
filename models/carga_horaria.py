from models.db import db


class CargaHoraria(db.Model):
    __tablename__ = "carga_horaria"

    id = db.Column(db.Integer, primary_key=True)

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

    quantidade_aulas_semana = db.Column(db.Integer, nullable=False)

    permite_aula_dupla = db.Column(db.Boolean, default=True)
    permite_aula_tripla = db.Column(db.Boolean, default=False)
    exige_distribuicao_semanal = db.Column(db.Boolean, default=False)
    quantidade_minima_dias_semana = db.Column(db.Integer, default=1)

    criado_em = db.Column(
        db.DateTime,
        server_default=db.func.current_timestamp()
    )

    def __repr__(self):
        return f"<CargaHoraria Turma {self.turma_id} - Disciplina {self.disciplina_id}>"