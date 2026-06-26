from flask import Flask
from config import Config
from models.db import db

from routes.professor_routes import professor_bp
from routes.escola_routes import escola_bp
from routes.disciplina_routes import disciplina_bp
from routes.turma_routes import turma_bp
from routes.professor_disciplina_routes import professor_disciplina_bp
from routes.professor_turma_routes import professor_turma_bp
from models.professor_turma import ProfessorTurma
from routes.turma_disciplina_routes import turma_disciplina_bp
from models.turma_disciplina import TurmaDisciplina
from routes.configuracao_horaria_routes import configuracao_horaria_bp

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

# Blueprints
app.register_blueprint(professor_bp)
app.register_blueprint(escola_bp)
app.register_blueprint(disciplina_bp)
app.register_blueprint(turma_bp)
app.register_blueprint(professor_disciplina_bp)
app.register_blueprint(professor_turma_bp)
app.register_blueprint(turma_disciplina_bp)
app.register_blueprint(configuracao_horaria_bp)


@app.route("/")
def home():
    return "Sistema de Grade Horária conectado ao PostgreSQL!"


if __name__ == "__main__":
    app.run(debug=True)