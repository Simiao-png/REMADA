from flask import Flask, render_template
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
from models.professor_segmento import ProfessorSegmento
from routes.configuracao_horaria_routes import configuracao_horaria_bp
from routes.disponibilidade_professor_routes import disponibilidade_professor_bp
from routes.carga_horaria_routes import carga_horaria_bp
from routes.motor_grade_routes import motor_grade_bp
from routes.cadastro_routes import cadastro_bp


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
app.register_blueprint(disponibilidade_professor_bp)
app.register_blueprint(carga_horaria_bp)
app.register_blueprint(motor_grade_bp)
app.register_blueprint(cadastro_bp)


# --- IMPORTS DOS MODELS PARA A DASHBOARD ---
# O Flask precisa conhecer a estrutura para contar as linhas no banco
from models.professor import Professor  # Ajuste o nome do arquivo/classe se for diferente
from models.turma import Turma          # Ex: se seu arquivo for turma.py e a classe Turma
from models.disciplina import Disciplina

@app.route("/")
def dashboard():
    try:
        # Faz a contagem diretamente no PostgreSQL usando o SQLAlchemy
        total_professores = db.session.query(Professor).count()
        total_turmas = db.session.query(Turma).count()
        total_disciplinas = db.session.query(Disciplina).count()
    except Exception as e:
        # Se der erro de banco (ex: tabela ainda não criada ou import errado), 
        # o sistema não cai, ele joga 0 na tela para você diagnosticar
        print(f"Erro ao buscar dados da dashboard: {e}")
        total_professores = 0
        total_turmas = 0
        total_disciplinas = 0

    return render_template(
        "dashboard.html",
        professores=total_professores,
        turmas=total_turmas,
        disciplinas=total_disciplinas
    )

if __name__ == "__main__":
    app.run(debug=True)