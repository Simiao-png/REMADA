from models.db import db


class ProfessorSegmento(db.Model):
    __tablename__ = "professor_segmento"

    id = db.Column(db.Integer, primary_key=True)

    professor_id = db.Column(
        db.Integer,
        db.ForeignKey("professores.id", ondelete="CASCADE"),
        nullable=False
    )

    segmento = db.Column(
        db.String(50),
        nullable=False
    )

    professor = db.relationship(
        "Professor",
        back_populates="segmentos"
    )

    __table_args__ = (
        db.UniqueConstraint(
            "professor_id",
            "segmento",
            name="uq_professor_segmento"
        ),
    )

    def __repr__(self):
        return (
            f"<ProfessorSegmento "
            f"professor_id={self.professor_id} "
            f"segmento={self.segmento}>"
        )