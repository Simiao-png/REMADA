from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from models.db import db
from models.escola import Escola
from models.usuario import Usuario

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        senha = request.form.get("senha")

        usuario = Usuario.query.filter_by(email=email).first()

        if usuario and usuario.checar_senha(senha):
            session["usuario_id"] = usuario.id
            session["usuario_nome"] = usuario.nome
            session["escola_id"] = usuario.escola_id
            return redirect(url_for("dashboard"))
        else:
            flash("E-mail ou senha incorretos. Tente novamente.", "danger")

    return render_template("login.html")


@auth_bp.route("/cadastrar-escola", methods=["POST"])
def cadastrar_escola():
    try:
        nome_escola = request.form.get("nome_escola")
        nome_responsavel = request.form.get("nome_responsavel")
        email = request.form.get("email")
        senha = request.form.get("senha")

        if Usuario.query.filter_by(email=email).first():
            flash("Este e-mail já está cadastrado. Faça login.", "warning")
            return redirect(url_for("auth.login"))

        nova_escola = Escola(nome=nome_escola)
        db.session.add(nova_escola)
        db.session.commit()

        novo_usuario = Usuario(
            nome=nome_responsavel,
            email=email,
            escola_id=nova_escola.id,
        )
        novo_usuario.set_senha(senha)

        db.session.add(novo_usuario)
        db.session.commit()

        session["usuario_id"] = novo_usuario.id
        session["usuario_nome"] = novo_usuario.nome
        session["escola_id"] = nova_escola.id

        return redirect(url_for("dashboard"))

    except Exception as e:
        db.session.rollback()
        flash(f"Erro ao criar conta: {str(e)}", "danger")
        return redirect(url_for("auth.login"))


@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))