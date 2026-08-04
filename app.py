import os

from flask import Flask, render_template, request, jsonify, session, redirect
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
from routes.gerar_grade import gerar_grade_bp

from models.disponibilidade_professor import DisponibilidadeProfessor
from models.grade import Grade
from models.grade_aula import GradeAula

from models.professor import Professor
from models.turma import Turma
from models.disciplina import Disciplina
from models.escola import Escola

from models.usuario import Usuario
from routes.auth_routes import auth_bp


app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

app.register_blueprint(auth_bp)

with app.app_context():
    db.create_all()


# ------------------------------------------------------------------
# CONTEXT PROCESSOR (INJETA A ESCOLA EM TODAS AS PAGINAS DO SISTEMA)
# ------------------------------------------------------------------
@app.context_processor
def inject_escola():
    escola_id = session.get("escola_id")
    escola_atual = None

    if escola_id:
        escola_atual = db.session.get(
            Escola,
            escola_id
        )

    return {
        "escola": escola_atual
    }


# ------------------------------------------------------------------
# BLUEPRINTS
# ------------------------------------------------------------------

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
app.register_blueprint(gerar_grade_bp)


# ------------------------------------------------------------------
# HEALTH CHECK
# ------------------------------------------------------------------

@app.route("/health")
def health():
    return {
        "status": "ok",
        "app": "REMADA"
    }, 200


# ------------------------------------------------------------------
# DASHBOARD
# ------------------------------------------------------------------

@app.route("/")
def dashboard():
    escola_id = session.get("escola_id")

    if not escola_id:
        return redirect("/login")

    try:

        # Filtros isolados por escola
        total_professores = db.session.query(Professor).filter_by(escola_id=escola_id).count()
        total_turmas = db.session.query(Turma).filter_by(escola_id=escola_id).count()
        total_disciplinas = db.session.query(Disciplina).filter_by(escola_id=escola_id).count()

        turmas_com_matriz = (
            db.session.query(TurmaDisciplina.turma_id)
            .join(Turma, Turma.id == TurmaDisciplina.turma_id)
            .filter(Turma.escola_id == escola_id)
            .distinct()
            .count()
        )

        turmas_com_professores = (
            db.session.query(ProfessorTurma.turma_id)
            .join(Turma, Turma.id == ProfessorTurma.turma_id)
            .filter(Turma.escola_id == escola_id)
            .distinct()
            .count()
        )

        professores_com_disponibilidade = (
            db.session.query(DisponibilidadeProfessor.professor_id)
            .join(Professor, Professor.id == DisponibilidadeProfessor.professor_id)
            .filter(Professor.escola_id == escola_id)
            .distinct()
            .count()
        )

        percentual_matrizes = (
            round((turmas_com_matriz / total_turmas) * 100)
            if total_turmas > 0 else 0
        )

        percentual_vinculos = (
            round((turmas_com_professores / total_turmas) * 100)
            if total_turmas > 0 else 0
        )

        percentual_disponibilidades = (
            round((professores_com_disponibilidade / total_professores) * 100)
            if total_professores > 0 else 0
        )

        progresso_geral = 0

        if total_professores > 0:
            progresso_geral += 15

        if total_turmas > 0:
            progresso_geral += 15

        if total_disciplinas > 0:
            progresso_geral += 15

        progresso_geral += round(percentual_matrizes * 0.25)
        progresso_geral += round(percentual_vinculos * 0.15)
        progresso_geral += round(percentual_disponibilidades * 0.15)

        progresso_geral = min(progresso_geral, 100)

        turmas_banco = (
            db.session.query(Turma)
            .filter_by(escola_id=escola_id)
            .order_by(Turma.nome)
            .all()
        )

        progresso_turmas = []

        for turma in turmas_banco:

            possui_matriz = (
                db.session.query(TurmaDisciplina)
                .filter(TurmaDisciplina.turma_id == turma.id)
                .first()
                is not None
            )

            possui_professor = (
                db.session.query(ProfessorTurma)
                .filter(ProfessorTurma.turma_id == turma.id)
                .first()
                is not None
            )

            percentual_turma = 0

            if possui_matriz:
                percentual_turma += 50

            if possui_professor:
                percentual_turma += 50

            progresso_turmas.append(
                {
                    "nome": turma.nome,
                    "percentual": percentual_turma,
                    "possui_matriz": possui_matriz,
                    "possui_professor": possui_professor,
                }
            )

        pendencias = []

        if total_professores == 0:
            pendencias.append("Nenhum professor cadastrado.")

        if total_turmas == 0:
            pendencias.append("Nenhuma turma cadastrada.")

        if total_disciplinas == 0:
            pendencias.append("Nenhuma disciplina cadastrada.")

        matrizes_pendentes = total_turmas - turmas_com_matriz

        if matrizes_pendentes > 0:
            pendencias.append(
                f"{matrizes_pendentes} turma(s) sem matriz curricular."
            )

        vinculos_pendentes = total_turmas - turmas_com_professores

        if vinculos_pendentes > 0:
            pendencias.append(
                f"{vinculos_pendentes} turma(s) sem professor vinculado."
            )

        disponibilidades_pendentes = (
            total_professores - professores_com_disponibilidade
        )

        if disponibilidades_pendentes > 0:
            pendencias.append(
                f"{disponibilidades_pendentes} professor(es) sem disponibilidade."
            )

        grades_da_escola = (
            db.session.query(GradeAula.grade_id)
            .join(Turma, Turma.id == GradeAula.turma_id)
            .filter(Turma.escola_id == escola_id)
            .distinct()
            .subquery()
        )

        ultimas_grades = (
            db.session.query(Grade)
            .filter(Grade.id.in_(db.session.query(grades_da_escola.c.grade_id)))
            .order_by(Grade.criado_em.desc())
            .limit(10)
            .all()
        )

    except Exception as e:

        print(f"Erro ao buscar dados da dashboard: {e}")

        total_professores = 0
        total_turmas = 0
        total_disciplinas = 0
        turmas_com_matriz = 0
        professores_com_disponibilidade = 0
        progresso_geral = 0
        progresso_turmas = []
        pendencias = ["Não foi possível carregar o resumo da escola."]
        ultimas_grades = []

    return render_template(
        "dashboard.html",
        professores=total_professores,
        turmas=total_turmas,
        disciplinas=total_disciplinas,
        matrizes=turmas_com_matriz,
        professores_com_disponibilidade=professores_com_disponibilidade,
        progresso_geral=progresso_geral,
        progresso_turmas=progresso_turmas,
        pendencias=pendencias,
        ultimas_grades=ultimas_grades,
    )


# ------------------------------------------------------------------
# VER GRADE SALVA
# ------------------------------------------------------------------

@app.route("/ver-grade")
@app.route("/visualizar-grade")
def tela_ver_grade():
    grade_id = request.args.get("id", type=int)

    if not grade_id:
        return "ID da grade não fornecido.", 400

    grade = Grade.query.get_or_404(grade_id)
    aulas = GradeAula.query.filter_by(grade_id=grade.id).all()

    turmas_dict = {t.id: t.nome for t in Turma.query.all()}
    profs_dict = {p.id: p.nome for p in Professor.query.all()}
    discs_obj = Disciplina.query.all()
    discs_nome_dict = {d.id: d.nome for d in discs_obj}
    discs_cor_dict = {
        d.id: getattr(
            d, "cor", getattr(d, "color", getattr(d, "cor_hex", "#4a90e2"))
        )
        for d in discs_obj
    }

    aulas_lista = []
    grade_dict = {
        "id": grade.id,
        "versao": grade.versao,
        "penalidade": grade.penalidade,
        "tempo_execucao": grade.tempo_execucao,
        "grade": {},
    }

    mapa_dias = {
        1: "segunda",
        2: "terca",
        3: "quarta",
        4: "quinta",
        5: "sexta",
        6: "sabado",
    }

    for a in aulas:
        turma_id_str = str(a.turma_id)
        dia_num = getattr(a, "dia_semana", getattr(a, "dia", 1))
        dia_str = mapa_dias.get(dia_num, "segunda")
        numero_aula = getattr(a, "numero_aula", getattr(a, "aula", 1))

        disc_nome = discs_nome_dict.get(
            a.disciplina_id, f"Disciplina {a.disciplina_id}"
        )
        disc_cor = discs_cor_dict.get(a.disciplina_id, "#4a90e2")
        turma_nome = turmas_dict.get(a.turma_id, f"Turma {a.turma_id}")
        prof_nome = profs_dict.get(a.professor_id, "A definir")

        aulas_lista.append({
            "turma_id": a.turma_id,
            "turma_nome": turma_nome,
            "professor_id": a.professor_id,
            "professor_nome": prof_nome,
            "disciplina_id": a.disciplina_id,
            "disciplina_nome": disc_nome,
            "disciplina_cor": disc_cor,
            "dia_semana": dia_num,
            "numero_aula": numero_aula
        })

        if turma_id_str not in grade_dict["grade"]:
            grade_dict["grade"][turma_id_str] = {}

        if dia_str not in grade_dict["grade"][turma_id_str]:
            grade_dict["grade"][turma_id_str][dia_str] = []

        while len(grade_dict["grade"][turma_id_str][dia_str]) < numero_aula:
            grade_dict["grade"][turma_id_str][dia_str].append(None)

        grade_dict["grade"][turma_id_str][dia_str][numero_aula - 1] = {
            "turma_id": a.turma_id,
            "turma_nome": turma_nome,
            "professor_id": a.professor_id,
            "professor_nome": prof_nome,
            "disciplina_id": a.disciplina_id,
            "disciplina_nome": disc_nome,
            "disciplina_cor": disc_cor,
        }

    return render_template(
        "ver_grade.html", 
        grade_json=grade_dict, 
        aulas_json=aulas_lista,
        grade=grade
    )


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.getenv("PORT", "5000")),
        debug=os.getenv("FLASK_DEBUG", "0") == "1"
    )