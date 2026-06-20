import asyncio
from flask import (
    Blueprint,
    render_template,
    redirect,
    session,
    request,
    url_for
)
from services.api import (
    get_polls,
    create_poll,
    get_poll_by_id,
    get_options_by_poll,
    create_option,
    update_option,
    delete_option,
    vote,
    get_poll_results,
    update_poll,
    delete_poll
)

polls_bp = Blueprint(
    "polls",
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

def load_poll_data(poll_id):
    poll_response = asyncio.run(
        get_poll_by_id(poll_id)
    )
    if poll_response.status_code != 200:
        return None
    poll = poll_response.json()
    options_response = asyncio.run(
        get_options_by_poll(poll_id)
    )
    options = []
    if options_response.status_code == 200:
        options = options_response.json()
    is_owner = (
        poll["usuario_id"] == session["user_id"]
    )
    return poll, options, is_owner

def render_poll_page(poll_id, error=None):
    data = load_poll_data(poll_id)
    if not data:
        return redirect(
            url_for("polls.home")
        )
    poll, options, is_owner = data
    return render_template(
        "poll.html",
        poll=poll,
        options=options,
        is_owner=is_owner,
        error=error
    )

@polls_bp.route("/")
def home():
    if "user_id" not in session:
        return redirect(
            url_for("auth.login_page")
        )
    response = asyncio.run(
        get_polls()
    )
    polls = []
    error = None
    if response.status_code == 200:
        polls = response.json()
    else:
        error = "Erro ao carregar enquetes."
    return render_template(
        "home.html",
        polls=polls,
        error=error
    )

@polls_bp.route("/polls/create", methods=["GET", "POST"])
def create_poll_page():
    if "user_id" not in session:
        return redirect(
            url_for("auth.login_page")
        )
    if request.method == "GET":
        return render_template(
            "create_poll.html",
            titulo="",
            descricao="",
            error=None
        )
    titulo = request.form.get("titulo", "").strip()
    descricao = request.form.get("descricao", "").strip()
    response = asyncio.run(
        create_poll(
            titulo,
            descricao,
            session["user_id"]
        )
    )
    if response.status_code != 200:
        return render_template(
            "create_poll.html",
            titulo=titulo,
            descricao=descricao,
            error=get_error_message(
                response,
                "Erro ao criar enquete."
            )
        )
    poll = response.json()
    return redirect(
        url_for(
            "polls.view_poll",
            poll_id=poll["id"]
        )
    )

@polls_bp.route("/polls/<int:poll_id>")
def view_poll(poll_id):
    if "user_id" not in session:
        return redirect(
            url_for("auth.login_page")
        )
    return render_poll_page(poll_id)

@polls_bp.route("/polls/<int:poll_id>/edit", methods=["GET", "POST"])
def edit_poll_page(poll_id):
    if "user_id" not in session:
        return redirect(
            url_for("auth.login_page")
        )
    poll_response = asyncio.run(
        get_poll_by_id(poll_id)
    )
    if poll_response.status_code != 200:
        return redirect(
            url_for("polls.home")
        )
    poll = poll_response.json()
    if poll["usuario_id"] != session["user_id"]:
        return redirect(
            url_for(
                "polls.view_poll",
                poll_id=poll_id
            )
        )
    if request.method == "GET":
        return render_template(
            "edit_poll.html",
            poll=poll,
            titulo=poll["titulo"],
            descricao=poll["descricao"] or "",
            error=None
        )
    titulo = request.form.get("titulo", "").strip()
    descricao = request.form.get("descricao", "").strip()
    response = asyncio.run(
        update_poll(
            poll_id,
            titulo,
            descricao
        )
    )
    if response.status_code != 200:
        return render_template(
            "edit_poll.html",
            poll=poll,
            titulo=titulo,
            descricao=descricao,
            error=get_error_message(
                response,
                "Erro ao atualizar enquete."
            )
        )
    return redirect(
        url_for(
            "polls.view_poll",
            poll_id=poll_id
        )
    )

@polls_bp.route("/polls/<int:poll_id>/delete", methods=["POST"])
def delete_poll_page(poll_id):
    if "user_id" not in session:
        return redirect(
            url_for("auth.login_page")
        )
    poll_response = asyncio.run(
        get_poll_by_id(poll_id)
    )
    if poll_response.status_code != 200:
        return redirect(
            url_for("polls.home")
        )
    poll = poll_response.json()
    if poll["usuario_id"] != session["user_id"]:
        return redirect(
            url_for(
                "polls.view_poll",
                poll_id=poll_id
            )
        )
    response = asyncio.run(
        delete_poll(poll_id)
    )
    if response.status_code != 200:
        return render_poll_page(
            poll_id,
            error=get_error_message(
                response,
                "Erro ao excluir enquete."
            )
        )
    return redirect(
        url_for("polls.home")
    )

@polls_bp.route("/polls/<int:poll_id>/options/create", methods=["POST"])
def create_option_page(poll_id):
    if "user_id" not in session:
        return redirect(
            url_for("auth.login_page")
        )
    data = load_poll_data(poll_id)
    if not data:
        return redirect(
            url_for("polls.home")
        )
    poll, _, is_owner = data
    if not is_owner:
        return redirect(
            url_for(
                "polls.view_poll",
                poll_id=poll_id
            )
        )
    texto = request.form.get("texto", "").strip()
    if not texto:
        return render_poll_page(
            poll_id,
            error="Informe uma opção."
        )
    response = asyncio.run(
        create_option(
            texto,
            poll_id
        )
    )
    if response.status_code != 200:
        return render_poll_page(
            poll_id,
            error=get_error_message(
                response,
                "Erro ao criar opção."
            )
        )
    return redirect(
        url_for(
            "polls.view_poll",
            poll_id=poll_id
        )
    )

@polls_bp.route("/polls/<int:poll_id>/options/<int:option_id>/edit", methods=["POST"])
def edit_option_page(poll_id, option_id):
    if "user_id" not in session:
        return redirect(
            url_for("auth.login_page")
        )
    data = load_poll_data(poll_id)
    if not data:
        return redirect(
            url_for("polls.home")
        )
    poll, _, is_owner = data
    if not is_owner:
        return redirect(
            url_for(
                "polls.view_poll",
                poll_id=poll_id
            )
        )
    texto = request.form.get("texto", "").strip()
    if not texto:
        return render_poll_page(
            poll_id,
            error="Informe um texto para a opção."
        )
    response = asyncio.run(
        update_option(
            option_id,
            texto
        )
    )
    if response.status_code != 200:
        return render_poll_page(
            poll_id,
            error=get_error_message(
                response,
                "Erro ao atualizar opção."
            )
        )
    return redirect(
        url_for(
            "polls.view_poll",
            poll_id=poll_id
        )
    )

@polls_bp.route("/polls/<int:poll_id>/options/<int:option_id>/delete", methods=["POST"])
def delete_option_page(poll_id, option_id):
    if "user_id" not in session:
        return redirect(
            url_for("auth.login_page")
        )
    data = load_poll_data(poll_id)
    if not data:
        return redirect(
            url_for("polls.home")
        )
    poll, _, is_owner = data
    if not is_owner:
        return redirect(
            url_for(
                "polls.view_poll",
                poll_id=poll_id
            )
        )
    response = asyncio.run(
        delete_option(option_id)
    )
    if response.status_code != 200:
        return render_poll_page(
            poll_id,
            error=get_error_message(
                response,
                "Erro ao excluir opção."
            )
        )
    return redirect(
        url_for(
            "polls.view_poll",
            poll_id=poll_id
        )
    )

@polls_bp.route("/polls/<int:poll_id>/vote", methods=["POST"])
def vote_page(poll_id):
    if "user_id" not in session:
        return redirect(
            url_for("auth.login_page")
        )
    data = load_poll_data(poll_id)
    if not data:
        return redirect(
            url_for("polls.home")
        )
    _, _, is_owner = data
    if is_owner:
        return render_poll_page(
            poll_id,
            error="O dono da enquete não pode votar."
        )
    option_id = request.form.get("opcao_id")
    if not option_id:
        return render_poll_page(
            poll_id,
            error="Selecione uma opção para votar."
        )
    try:
        option_id = int(option_id)
    except ValueError:
        return render_poll_page(
            poll_id,
            error="Opção inválida."
        )
    response = asyncio.run(
        vote(
            session["user_id"],
            poll_id,
            option_id
        )
    )
    if response.status_code != 200:
        return render_poll_page(
            poll_id,
            error=get_error_message(
                response,
                "Erro ao registrar voto."
            )
        )
    return redirect(
        url_for(
            "polls.results_page",
            poll_id=poll_id
        )
    )

@polls_bp.route("/polls/<int:poll_id>/results")
def results_page(poll_id):
    if "user_id" not in session:
        return redirect(
            url_for("auth.login_page")
        )
    response = asyncio.run(
        get_poll_results(poll_id)
    )
    if response.status_code != 200:
        return redirect(
            url_for("polls.home")
        )
    return render_template(
        "results.html",
        results=response.json()
    )