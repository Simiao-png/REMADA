from models.db import db


class ConfiguracaoHoraria(db.Model):
    __tablename__ = "configuracao_horaria"

    id = db.Column(db.Integer, primary_key=True)

    escola_id = db.Column(db.Integer, nullable=False)

    segmento = db.Column(
    db.String(50),
    nullable=False,
    default="geral"
)

    nome = db.Column(db.String(100), nullable=False)
    aulas_por_dia = db.Column(db.Integer, nullable=False)
    duracao_aula_minutos = db.Column(db.Integer, nullable=False)
    duracao_intervalo_minutos = db.Column(db.Integer, nullable=False)

    tem_aula_segunda = db.Column(db.Boolean, default=True)
    tem_aula_terca = db.Column(db.Boolean, default=True)
    tem_aula_quarta = db.Column(db.Boolean, default=True)
    tem_aula_quinta = db.Column(db.Boolean, default=True)
    tem_aula_sexta = db.Column(db.Boolean, default=True)
    tem_aula_sabado = db.Column(db.Boolean, default=False)

    ativo = db.Column(db.Boolean, default=True)

    criado_em = db.Column(
        db.DateTime,
        server_default=db.func.current_timestamp()
    )

    def __repr__(self):
        return f"<ConfiguracaoHoraria {self.nome}>"