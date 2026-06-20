import asyncio
from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    session,
    url_for
)
from services.api import (
    login_user,
    register_user
)

auth_bp = Blueprint(
    "auth",
    __name__
)

def get_error_message(response, default):
    try:
        data = response.json()
    except Exception:
        return default
    if isinstance(data, dict):
        detail = data.get("detail", default)
        if isinstance(detail, list):
            return default
        return detail
    return default

@auth_bp.route("/login", methods=["GET", "POST"])
def login_page():
    if session.get("user_id"):
        return redirect(
            url_for("polls.home")
        )
    if request.method == "GET":
        return render_template(
            "login.html",
            email="",
            error=None
        )
    email = request.form.get("email", "").strip()
    senha = request.form.get("senha", "")
    response = asyncio.run(
        login_user(
            email,
            senha
        )
    )
    if response.status_code != 200:
        return render_template(
            "login.html",
            email=email,
            error=get_error_message(
                response,
                "Email ou senha inválidos."
            )
        )
    user = response.json()
    session["user_id"] = user["id"]
    session["user_name"] = user["nome"]
    return redirect(
        url_for("polls.home")
    )

@auth_bp.route("/register", methods=["GET", "POST"])
def register_page():
    if session.get("user_id"):
        return redirect(
            url_for("polls.home")
        )
    if request.method == "GET":
        return render_template(
            "register.html",
            nome="",
            email="",
            error=None
        )
    nome = request.form.get("nome", "").strip()
    email = request.form.get("email", "").strip()
    senha = request.form.get("senha", "")
    response = asyncio.run(
        register_user(
            nome,
            email,
            senha
        )
    )
    if response.status_code != 200:
        return render_template(
            "register.html",
            nome=nome,
            email=email,
            error=get_error_message(
                response,
                "Erro ao criar usuário."
            )
        )
    return redirect(
        url_for("auth.login_page")
    )

@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(
        url_for("auth.login_page")
    )