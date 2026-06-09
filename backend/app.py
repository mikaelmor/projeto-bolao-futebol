#ponto de entrada da aplicação flask


from flask import Flask, request, jsonify, send_from_directory
from flask_socketio import SocketIO
from routes.socket_events import registrar_eventos
from werkzeug.security import generate_password_hash, check_password_hash
import os
import secrets
import re
from datetime import datetime, timedelta
from utils.senha import validar_forca_senha, verificar_senha


def carregar_env_local():
    env_path = os.path.join(os.path.dirname(__file__), ".env")
    if not os.path.exists(env_path):
        return

    with open(env_path, "r", encoding="utf-8") as env_file:
        for linha in env_file:
            linha = linha.strip()
            if not linha or linha.startswith("#") or "=" not in linha:
                continue
            chave, valor = linha.split("=", 1)
            os.environ[chave.strip()] = valor.strip().strip('"').strip("'")


carregar_env_local()

#Módulo de cadastro
from models.repositorio import RepositorioEmMemoria
from services.cadastro_service import CadastroService
from routes.cadastro import cadastro_bp

#Módulo de jogos 
from models.repositorio_jogo import RepositorioJogoEmMemoria
from services.jogo_service import JogoService
from routes.jogos import jogos_bp
from routes.suporte import suporte_bp
from services.simulacao_service import SimulacaoService
from routes.simulacao import simulacao_bp
from routes.configuracoes import configuracoes_bp
from routes.perfil import perfil_bp
from routes.recuperacao_senha import recuperacao_senha_bp

#Módulo palpites
from models.repositorio_palpite import RepositorioPalpiteEmMemoria
from services.palpite_service import PalpiteService
from routes.palpites import palpites_bp

#módulo ranking
from services.ranking_service import RankingService
from routes.ranking import ranking_bp


app = Flask(__name__)
from flask_cors import CORS
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")
app.config["SOCKETIO"] = socketio
registrar_eventos(socketio)
app.secret_key = secrets.token_hex(32)

users = {
    "usuario@exemplo.com": {
        "password_hash": generate_password_hash("senha123"),
        "name": "Usuário Exemplo"
    }
}

reset_tokens = {}
session_tokens = {}

try:
    from models.repositorio_mysql import criar_conexao, RepositorioUsuarioMySQL
    from models.repositorio_mysql import RepositorioJogoMySQL, RepositorioPalpiteMySQL
    from models.repositorio_mysql import criar_schema

    _conn = criar_conexao()
    criar_schema(_conn)
    _repo_usuario = RepositorioUsuarioMySQL(_conn)
    _repo_jogo = RepositorioJogoMySQL(_conn)
    _repo_palpite = RepositorioPalpiteMySQL(_conn)
    print("Banco MySQL conectado.")
except Exception as exc:
    print(f"Banco MySQL indisponivel, usando memoria: {exc}")
    _conn = None
    _repo_usuario = RepositorioEmMemoria()
    _repo_jogo = RepositorioJogoEmMemoria()
    _repo_palpite = RepositorioPalpiteEmMemoria()

#Registro dos módulos
app.config["CADASTRO_SERVICE"] = CadastroService(_repo_usuario)
app.register_blueprint(cadastro_bp)

app.config["DEV_SIMULATION_KEY"] = os.environ.get("GOALPOINT_DEV_KEY", "goalpoint-dev")
app.config["JOGO_SERVICE"] = JogoService(_repo_jogo)
app.register_blueprint(jogos_bp)

app.register_blueprint(suporte_bp)
app.config["SIMULACAO_SERVICE"] = SimulacaoService(app.config["JOGO_SERVICE"])
app.register_blueprint(simulacao_bp)

app.config["PALPITE_SERVICE"] = PalpiteService(_repo_palpite, _repo_jogo)
app.register_blueprint(palpites_bp)

app.config["RANKING_SERVICE"] = RankingService(_repo_palpite, _repo_usuario)
app.register_blueprint(ranking_bp)

app.config["SESSION_TOKENS"] = session_tokens
app.config["USER_SETTINGS"] = {}
app.register_blueprint(configuracoes_bp)
app.register_blueprint(perfil_bp)
app.register_blueprint(recuperacao_senha_bp)


def carregar_jogos_iniciais():
    service = app.config["JOGO_SERVICE"]
    if service.listar_todos():
        return

    hoje = datetime.now()
    jogos = [
        ("Brasil", "Argentina", 14, 30, "Grupo A", 10, 3, 10),
        ("Holanda", "Portugal", 15, 40, "Grupo B", 10, 3, 10),
        ("Catar", "Espanha", 16, 5, "Grupo C", 15, 3, 5),
        ("Ira", "EUA", 16, 35, "Grupo D", 10, 3, 10),
    ]

    for selecao_a, selecao_b, hora, minuto, grupo, pontos_a, pontos_empate, pontos_b in jogos:
        horario = hoje.replace(hour=hora, minute=minuto, second=0, microsecond=0)
        service.criar_jogo(
            fase="grupos",
            data_jogo=horario.date().isoformat(),
            horario=horario.strftime("%H:%M"),
            time_a=selecao_a,
            time_b=selecao_b,
            pontos_time_a=pontos_a,
            pontos_empate=pontos_empate,
            pontos_time_b=pontos_b,
        )


carregar_jogos_iniciais()


def is_valid_email(email: str) -> bool:
    return bool(re.match(r"[^@]+@[^@]+\.[^@]+", email, re.IGNORECASE))

def is_valid_password(password: str) -> bool:
    valido, _ = validar_forca_senha(password)
    return valido


def _buscar_usuario_por_email(email: str):
    return app.config["CADASTRO_SERVICE"]._repo.buscar_por_email(email)


@app.route("/")
def index():
    return jsonify({"status": "ok", "message": "API rodando."})


@app.route("/uploads/profile_pictures/<path:filename>")
def arquivos_foto_perfil(filename):
    return send_from_directory(os.path.join(app.root_path, "uploads", "profile_pictures"), filename)


@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({
        "success": False,
        "error": "Metodo nao permitido para esta URL.",
        "method": request.method,
        "path": request.path,
    }), 405


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return jsonify({
            "success": True,
            "message": "Endpoint de login ativo. Envie email e password via POST.",
        }), 200

    
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"success": False, "error": "Corpo da requisição deve ser JSON."}), 400

    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""

    if not email or not is_valid_email(email):
        return jsonify({"success": False, "error": "Email inválido."}), 400

    if not password or not is_valid_password(password):
        return jsonify({
            "success": False,
            "error": "Senha deve ter pelo menos 5 caracteres, uma letra ou numero e um caractere especial.",
        }), 400

    usuario = _buscar_usuario_por_email(email)
    if usuario:
        senha_correta = verificar_senha(password, usuario.senha_hash)
        nome_usuario = usuario.nome
        usuario_resposta = usuario.to_dict()
    else:
        user = users.get(email)
        senha_correta = bool(user and check_password_hash(user["password_hash"], password))
        nome_usuario = user["name"] if user else None
        usuario_resposta = {"email": email, "name": user["name"]} if user else None

    if not usuario and not users.get(email):
        return jsonify({
            "success": False,
            "error": "Aparentemente voce ainda nao realizou o cadastro.",
        }), 404

    if not senha_correta:
        return jsonify({"success": False, "error": "Email ou senha incorretos."}), 401

    session_token = secrets.token_urlsafe(32)
    session_tokens[session_token] = email
    return jsonify({
        "success": True,
        "message": f"Bem-vindo, {nome_usuario}!",
        "session_token": session_token,
        "user": usuario_resposta,
    }), 200


@app.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    """
    POST /forgot-password
    Body JSON: {"email": "..."}
    """
    if request.method == "GET":
        return jsonify({
            "success": True,
            "message": "Endpoint de recuperacao de senha ativo. Envie email via POST.",
        }), 200

    data = request.get_json(silent=True)
    if not data:
        return jsonify({"success": False, "error": "Corpo da requisição inválido."}), 400

    email = (data.get("email") or "").strip().lower()
    if not email or not is_valid_email(email):
        return jsonify({"success": False, "error": "Email inválido."}), 400

    token = secrets.token_urlsafe(32)
    reset_tokens[token] = {
    "email": email,
    "expires_at": datetime.utcnow() + timedelta(minutes=40)
}

    from routes.suporte import _enviar_email_suporte
    try:
        _enviar_email_suporte(
            f"Você solicitou a recuperação de senha do GoalPoint.\n\nSeu token de recuperação é:\n\n{token}\n\nExpira em 40 minutos."
        )
    except Exception as e:
        print(f"Erro ao enviar email: {e}")

    return jsonify({
        "success": True,
        "message": "Se o email estiver cadastrado, você receberá as instruções em breve.",
    }),200
  


@app.route("/reset-password", methods=["GET", "POST"])
def reset_password():
    if request.method == "GET":
        return jsonify({
            "success": True,
            "message": "Endpoint de redefinicao de senha ativo. Envie token e new_password via POST.",
        }), 200

    data = request.get_json(silent=True)
    if not data:
        return jsonify({"success": False, "error": "Corpo da requisição inválido."}), 400

    token = data.get("token") or ""
    new_password = data.get("new_password") or ""

    if not token:
        return jsonify({"success": False, "error": "Token necessário."}), 400

    if not new_password or not is_valid_password(new_password):
        return jsonify({
            "success": False,
            "error": "A nova senha deve ter pelo menos 5 caracteres, uma letra ou numero e um caractere especial.",
        }), 400

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
    socketio.run(app, debug=True, port=5000, use_reloader=False)
