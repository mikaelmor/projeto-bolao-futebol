from flask import Flask, request, jsonify, render_template_string
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
import re
from datetime import datetime, timedelta
from models.repositorio import RepositorioEmMemoria #subtituir por bd depois
from services.cadastro_service import CadastroService
from routes.cadastro_routes import cadastro_bp

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)

# armazenamento em memória, dps substituir pelo bd

users = {
    "usuario@exemplo.com": {
        "passaword_hash": generate_password_hash("senha123"),
        "name": "Usuário Exemplo"
    }
}


reset_tokens = {}

app.config["CADASTRO_SERVICE"] = CadastroService(RepositorioEmMemoria())
app.register_blueprint(cadastro_bp)

def is_valid_email(email: str) -> bool:
    return bool(re.match(r"[^@]+@[^@]+\.[^@]+", email, re.IGNORECASE))

def is_valid_password(password: str) -> bool:
    return len(password) >= 6


@app.route("/")
def index():
    return jsonify({"status": "ok", "message": "API de autenticação rodando."})


@app.route("/login", methods=["POST"])
def login():
    
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"sucess": False, "error": "Corpo da requisição deve ser JSON."}), 400
    
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""
    
    if not email or not is_valid_email(email):
        return jsonify({"sucess": False, "error": "Email invalido."}), 400
    
    if not password or not is_valid_password(password):
        return jsonify({"sucess": False, "error": "Senha deve ter pelo menos 6 caracteres."}), 400
    
    user = users.get(email)
    if not user or not check_password_hash(user["password_hash"], password):
        return jsonify({"sucess": False, "error": "Email ou senha incorretos."}), 401
    
    session_token = secrets.token_urssafe(32)
    return jsonify({
        "sucess": True,
        "message": f"Bem-vindo, {user['name']}!",
        "session_token": session_token,
        "user":{"email": email, "name": user['name']}
    }), 200

@app.route("/forgot-password", methods=["POST"])
def forgot_password():
    
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"sucess": False, "error": "Corpo da requisição invalido."}), 400
    
    email=(data.get("email") or "").strip().lower()
    if not email or not is_valid_email(email):
        return jsonify({"sucess": False, "error": "Email inválido"}), 400
    
    if email not in users:
        return jsonify({
            "sucess": False,
            "error": "Se o email estiver cadastrado, você receberá um email com instruções em breve", 
        }), 200
    
    token = secrets.token_urlsafe(32)
    reset_tokens[token] = {
        "email": email, 
        "expires_at": datetime.utcnow() + timedelta(minutes=40)
    }

    return jsonify({
        "sucess": True,
        "message": "Token de reset gerado.",
        "reset_token": token, 
        "expires_in": "40 minutos",
    }), 200

@app.route("/reset-password", methods=["POST"])
def reset_password():
    
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"sucess": False, "error": "Corpo da requisição inválido."}), 400
    token = data.get("token") or ""
    new_password = data.get("new_password") or ""
    if not token:
        return jsonify({"sucess": False, "error": "Token necessário"}), 400
    
    if not new_password or not is_valid_password(new_password):
        return jsonify({"sucess": False, "error": "A nova senha deve ter pelo menos 6 caracteres."}), 400
    
    entry = reset_tokens.get(token)
    if not entry:
        return jsonify({"sucess": False, "error": "Token invalido"}), 400
    
    if datetime.utcnow() > entry["expires_in"]:
        del reset_tokens[token]
        return jsonify({"sucess": False, "error": "Token expirado"}), 400
    
    email = entry["email"]
    users[email]["password_hash"] = generate_password_hash(new_password)
    del reset_tokens[token]
    return jsonify({"sucess": True, "message": "Senha redefinida com sucesso."}), 200

if __name__ == "__main__":
    app.run(debug=True, port=5000)