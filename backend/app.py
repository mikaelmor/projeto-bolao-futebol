from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
import re
from datetime import datetime, timedelta

#Módulo de cadastro
from models.repositorio import RepositorioEmMemoria
from services.cadastro_service import CadastroService
from routes.cadastro import cadastro_bp
#Módulo de jogos 
from models.repositorio_jogo import RepositorioJogoEmMemoria
from services.jogo_service import JogoService
from routes.jogos import jogos_bp


app = Flask(__name__)
app.secret_key = secrets.token_hex(32)

#Armazenamento em memória (substituir pelo BD) 
users = {
    "usuario@exemplo.com": {
        "password_hash": generate_password_hash("senha123"),
        "name": "Usuário Exemplo"
    }
}

reset_tokens = {}

#Registro dos módulos
app.config["CADASTRO_SERVICE"] = CadastroService(RepositorioEmMemoria())
app.register_blueprint(cadastro_bp)

app.config["JOGO_SERVICE"] = JogoService(RepositorioJogoEmMemoria())
app.register_blueprint(jogos_bp)


def is_valid_email(email: str) -> bool:
    return bool(re.match(r"[^@]+@[^@]+\.[^@]+", email, re.IGNORECASE))

def is_valid_password(password: str) -> bool:
    return len(password) >= 6


@app.route("/")
def index():
    return jsonify({"status": "ok", "message": "API rodando."})


@app.route("/login", methods=["POST"])
def login():
    """
    POST /login
    Body JSON: {"email": "...", "password": "..."}
    """
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"success": False, "error": "Corpo da requisição deve ser JSON."}), 400

    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""

    if not email or not is_valid_email(email):
        return jsonify({"success": False, "error": "Email inválido."}), 400

    if not password or not is_valid_password(password):
        return jsonify({"success": False, "error": "Senha deve ter pelo menos 6 caracteres."}), 400

    user = users.get(email)
    if not user or not check_password_hash(user["password_hash"], password):
        return jsonify({"success": False, "error": "Email ou senha incorretos."}), 401

    session_token = secrets.token_urlsafe(32)
    return jsonify({
        "success": True,
        "message": f"Bem-vindo, {user['name']}!",
        "session_token": session_token,
        "user": {"email": email, "name": user["name"]}
    }), 200


@app.route("/forgot-password", methods=["POST"])
def forgot_password():
    """
    POST /forgot-password
    Body JSON: {"email": "..."}
    """
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"success": False, "error": "Corpo da requisição inválido."}), 400

    email = (data.get("email") or "").strip().lower()
    if not email or not is_valid_email(email):
        return jsonify({"success": False, "error": "Email inválido."}), 400

    if email not in users:
        return jsonify({
            "success": True,
            "message": "Se o email estiver cadastrado, você receberá as instruções em breve.",
        }), 200

    token = secrets.token_urlsafe(32)
    reset_tokens[token] = {
        "email": email,
        "expires_at": datetime.utcnow() + timedelta(minutes=40)
    }

    return jsonify({
        "success": True,
        "message": "Token de reset gerado.",
        "reset_token": token,
        "expires_in": "40 minutos",
    }), 200


@app.route("/reset-password", methods=["POST"])
def reset_password():
    """
    POST /reset-password
    Body JSON: {"token": "...", "new_password": "..."}
    """
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"success": False, "error": "Corpo da requisição inválido."}), 400

    token = data.get("token") or ""
    new_password = data.get("new_password") or ""

    if not token:
        return jsonify({"success": False, "error": "Token necessário."}), 400

    if not new_password or not is_valid_password(new_password):
        return jsonify({"success": False, "error": "A nova senha deve ter pelo menos 6 caracteres."}), 400

    entry = reset_tokens.get(token)
    if not entry:
        return jsonify({"success": False, "error": "Token inválido."}), 400

    if datetime.utcnow() > entry["expires_at"]:
        del reset_tokens[token]
        return jsonify({"success": False, "error": "Token expirado."}), 400

    email = entry["email"]
    users[email]["password_hash"] = generate_password_hash(new_password)
    del reset_tokens[token]

    return jsonify({"success": True, "message": "Senha redefinida com sucesso."}), 200


if __name__ == "__main__":
    app.run(debug=True, port=5000)