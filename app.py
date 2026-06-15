from flask import Flask
from config import Config
from models.db import db

from routes.professor_routes import professor_bp
from routes.escola_routes import escola_bp
from routes.disciplina_routes import disciplina_bp
from routes.turma_routes import turma_bp

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

# Blueprints
app.register_blueprint(professor_bp)
app.register_blueprint(escola_bp)
app.register_blueprint(disciplina_bp)
app.register_blueprint(turma_bp)


@app.route("/")
def home():
    return "Sistema de Grade Horária conectado ao PostgreSQL!"


if __name__ == "__main__":
    app.run(debug=True)