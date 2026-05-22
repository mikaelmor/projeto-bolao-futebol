from flask import Blueprint, current_app, jsonify, request

from models.jogo import ErroJogo
from services.simulacao_service import SimulacaoService


simulacao_bp = Blueprint("simulacao", __name__, url_prefix="/api/simulacao")


def _get_service() -> SimulacaoService:
    return current_app.config["SIMULACAO_SERVICE"]


def _validar_dev_key():
    dev_key = current_app.config.get("DEV_SIMULATION_KEY")
    if request.headers.get("X-Dev-Key") != dev_key:
        return jsonify({"erro": "Controle permitido apenas para o desenvolvedor."}), 403
    return None


@simulacao_bp.get("/jogos")
def listar_jogos_simulados():
    return jsonify({"jogos": _get_service().listar_jogos()}), 200


@simulacao_bp.post("/jogos/<int:jogo_id>/palpite")
def registrar_palpite(jogo_id: int):
    dados = request.get_json(silent=True) or {}

    try:
        palpite = _get_service().registrar_palpite(
            jogo_id=jogo_id,
            usuario_id=dados.get("usuario_id"),
            escolha=dados.get("escolha"),
        )
        return jsonify({"mensagem": "Palpite registrado.", "palpite": palpite}), 200
    except ErroJogo as e:
        return jsonify(e.to_dict()), 400


@simulacao_bp.delete("/jogos/<int:jogo_id>/palpite")
def remover_palpite(jogo_id: int):
    dados = request.get_json(silent=True) or {}

    try:
        palpite = _get_service().remover_palpite(
            jogo_id=jogo_id,
            usuario_id=dados.get("usuario_id"),
        )
        return jsonify({"mensagem": "Palpite removido.", "palpite": palpite}), 200
    except ErroJogo as e:
        return jsonify(e.to_dict()), 400


@simulacao_bp.post("/jogos/<int:jogo_id>/iniciar")
def iniciar_jogo_simulado(jogo_id: int):
    erro = _validar_dev_key()
    if erro:
        return erro

    dados = request.get_json(silent=True) or {}
    duracao = dados.get("duracao_segundos", 120)

    try:
        jogo = _get_service().iniciar(jogo_id, duracao)
        return jsonify({"mensagem": "Simulacao iniciada.", "jogo": jogo}), 200
    except ErroJogo as e:
        return jsonify(e.to_dict()), 400


@simulacao_bp.post("/jogos/<int:jogo_id>/finalizar")
def finalizar_jogo_simulado(jogo_id: int):
    erro = _validar_dev_key()
    if erro:
        return erro

    try:
        jogo = _get_service().finalizar(jogo_id)
        return jsonify({"mensagem": "Simulacao finalizada.", "jogo": jogo}), 200
    except ErroJogo as e:
        return jsonify(e.to_dict()), 400


@simulacao_bp.patch("/jogos/<int:jogo_id>/duracao")
def atualizar_duracao_simulada(jogo_id: int):
    erro = _validar_dev_key()
    if erro:
        return erro

    dados = request.get_json(silent=True) or {}

    try:
        jogo = _get_service().atualizar_duracao(jogo_id, dados.get("duracao_segundos"))
        return jsonify({"mensagem": "Duracao atualizada.", "jogo": jogo}), 200
    except ErroJogo as e:
        return jsonify(e.to_dict()), 400
