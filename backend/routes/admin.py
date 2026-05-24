from flask import Blueprint, current_app, jsonify, request

from models.jogo import ErroJogo
from models.palpite import ErroPalpite
from services.jogo_service import JogoService

admin_bp = Blueprint("admin", __name__, url_prefix="/api/admin")


def _jogo_service() -> JogoService:
    return current_app.config["JOGO_SERVICE"]


def _palpite_service():
    return current_app.config.get("PALPITE_SERVICE")


def _cadastro_service():
    return current_app.config["CADASTRO_SERVICE"]


def _listar_usuarios() -> list[dict]:
    repo = _cadastro_service()._repo
    usuarios = getattr(repo, "_usuarios", {})
    return [usuario.to_dict() for usuario in usuarios.values()]


def _buscar_usuario(id_usuario: int):
    repo = _cadastro_service()._repo
    return repo.buscar_por_id(id_usuario)


def _normalizar_resultado(resultado: str | None) -> str | None:
    mapa = {
        "1": "time_a",
        "x": "empate",
        "2": "time_b",
        "time_a": "time_a",
        "empate": "empate",
        "time_b": "time_b",
    }
    if resultado is None:
        return None
    return mapa.get(str(resultado).strip().lower())


@admin_bp.post("/game/<int:id_jogo>/start")
def start_game(id_jogo: int):
    try:
        jogo = _jogo_service().iniciar_jogo(id_jogo)
        return jsonify(jogo), 200
    except ErroJogo as erro:
        return jsonify(erro.to_dict()), 400


@admin_bp.post("/game/<int:id_jogo>/finish")
def finish_game(id_jogo: int):
    dados = request.get_json(silent=True) or {}
    resultado = _normalizar_resultado(dados.get("winner") or dados.get("resultado"))

    if not resultado:
        return jsonify({"erro": "Informe winner/resultado: 1, X, 2, time_a, empate ou time_b."}), 422

    try:
        jogo = _jogo_service().registrar_resultado(id_jogo, resultado)
        palpites_avaliados = []
        palpite_service = _palpite_service()
        if palpite_service:
            palpites_avaliados = palpite_service.avaliar_palpites_do_jogo(id_jogo)

        return jsonify({
            "jogo": jogo,
            "palpites_avaliados": len(palpites_avaliados),
        }), 200
    except (ErroJogo, ErroPalpite) as erro:
        return jsonify(erro.to_dict()), 400


@admin_bp.get("/users")
def list_users():
    usuarios = _listar_usuarios()
    return jsonify({"total": len(usuarios), "usuarios": usuarios}), 200


@admin_bp.get("/users/<int:id_usuario>/bets")
def user_bets(id_usuario: int):
    usuario = _buscar_usuario(id_usuario)
    if not usuario:
        return jsonify({"erro": "Usuario nao encontrado.", "campo": "id_usuario"}), 404

    palpite_service = _palpite_service()
    if not palpite_service:
        return jsonify({
            "usuario": usuario.to_dict(),
            "palpites": [],
            "total_palpites": 0,
            "acertos": 0,
            "pontuacao_total": 0,
        }), 200

    palpites = palpite_service.palpites_do_usuario(id_usuario)
    pontuacao = palpite_service.pontuacao_total(id_usuario)
    return jsonify({
        "usuario": usuario.to_dict(),
        "palpites": palpites,
        **pontuacao,
    }), 200
