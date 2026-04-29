from flask import Flask, request, jsonify, render_template_string
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
import re
from flask_cors import CORS
from datetime import datetime, timedelta
from models.repositorio import RepositorioEmMemoria #subtituir por bd depois
from services.cadastro_service import CadastroService
from routes.cadastro_routes import cadastro_bp


app = Flask(__name__)
app.secret_key = secrets.token_hex(32)

# armazenamento em memória, dps substituir pelo bd

users = {
    "usuario@exemplo.com": {
        "password_hash": generate_password_hash("senha123"),
        "name": "Usuário Exemplo"
    }
}

CORS(app, origins=["http://localhost:5173"])

games_db = {
    "brasil_vs_argentina": {
        "id": "brasil_vs_argentina",
        "time1": "Brasil",
        "time2": "Argentina",
        "scheduled_time": "2026-06-10T14:00:00",  
        "status": "upcoming",
        "result": None  
    },
    "holanda_vs_portugal": {
        "id": "holanda_vs_portugal",
        "time1": "Holanda",
        "time2": "Portugal",
        "scheduled_time": "2026-06-10T15:00:00",
        "status": "upcoming",
        "result": None
    },
    "catar_vs_espanha": {
        "id": "catar_vs_espanha",
        "time1": "Catar",
        "time2": "Espanha",
        "scheduled_time": "2026-06-10T16:05:00",
        "status": "upcoming",
        "result": None
    },
    "ira_vs_eua": {
        "id": "ira_vs_eua",
        "time1": "Irã",
        "time2": "EUA",
        "scheduled_time": "2026-06-10T17:00:00",
        "status": "upcoming",
        "result": None
    }
}

user_predictions = {}
sessions = {}
reset_tokens = {}

def get_current_user_from_token():
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return None
    token = auth_header.split(" ")[1]
    email = sessions.get(token)
    return email

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
    
    session_token = secrets.token_urlsafe(32)
    sessions[session_token] = email
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
    
    if datetime.utcnow() > entry["expires_at"]:
        del reset_tokens[token]
        return jsonify({"sucess": False, "error": "Token expirado"}), 400
    
    email = entry["email"]
    users[email]["password_hash"] = generate_password_hash(new_password)
    del reset_tokens[token]
    return jsonify({"sucess": True, "message": "Senha redefinida com sucesso."}), 200

@app.route("/api/games", methods=["GET"])
def get_games():
    
    """Return all games with status and the user's prediction (if logged in)."""
    user_email = get_current_user_from_token()
    games_list = []
    for game_id, game in games_db.items():
        game_data = {
            "id": game_id,
            "time1": game["time1"],
            "time2": game["time2"],
            "scheduled_time": game["scheduled_time"],
            "status": game["status"],
            "result": game["result"],
            "user_prediction": user_predictions.get(user_email, {}).get(game_id) if user_email else None
        }
        
        games_list.append(game_data)
    return jsonify({"success": True, "games": games_list})

@app.route("/api/predict", methods=["POST"])
def make_prediction():
    """Submit or change a prediction for a game (only allowed if game is upcoming)."""
    user_email = get_current_user_from_token()
    if not user_email:
        return jsonify({"success": False, "error": "Unauthorized"}), 401

    data = request.get_json()
    if not data:
        return jsonify({"success": False, "error": "Invalid request"}), 400

    game_id = data.get("game_id")
    prediction = data.get("prediction")  # 'time1', 'draw', 'time2'

    if game_id not in games_db:
        return jsonify({"success": False, "error": "Game not found"}), 404

    game = games_db[game_id]
    if game["status"] != "upcoming":
        return jsonify({"success": False, "error": "Game already started or finished. Predictions locked."}), 403

    if prediction not in ["time1", "draw", "time2"]:
        return jsonify({"success": False, "error": "Invalid prediction"}), 400

    # Store prediction
    if user_email not in user_predictions:
        user_predictions[user_email] = {}
    user_predictions[user_email][game_id] = prediction

    return jsonify({"success": True, "message": "Prediction saved!"})

# Optional: Admin endpoint to start a game (manual simulation)
@app.route("/api/admin/start-game", methods=["POST"])
def start_game():
    # In a real app you'd check for admin role
    data = request.get_json()
    game_id = data.get("game_id")
    if game_id not in games_db:
        return jsonify({"success": False, "error": "Game not found"}), 404
    games_db[game_id]["status"] = "live"
    return jsonify({"success": True, "message": f"Game {game_id} is now LIVE"})

@app.route("/api/admin/finish-game", methods=["POST"])
def finish_game():
    data = request.get_json()
    game_id = data.get("game_id")
    result = data.get("result")  # 'time1', 'draw', 'time2'
    if game_id not in games_db:
        return jsonify({"success": False, "error": "Game not found"}), 404
    games_db[game_id]["status"] = "finished"
    games_db[game_id]["result"] = result
    return jsonify({"success": True, "message": "Game finished"})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
