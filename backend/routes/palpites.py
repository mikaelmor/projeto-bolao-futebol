#routes/palpites.py

from flask import Blueprint, jsonify, request
from models.jogo import ErroJogo
from models.palpite import ErroPalpite

palpites_bp = Blueprint("palpites", __name__, url_prefix="/api/palpites")

def _get_service():
    from flask import current_app
    return current_app.config["PALPITE_SERVICE"]

@palpites_bp.post("/")
def criar_palpite():
    """
    Registra um palpite.
    Body JSON:
        id_usuario : int
        id_jogo    : int
        escolha    : "time_a" | "empate" | "time_b"
    """
    dados = request.get_json(silent=True) or {}
    ausentes = [c for c in ["id_usuario", "id_jogo", "escolha"] if dados.get(c) is None]
    if ausentes:
        return jsonify({"erro": "Campos obrigatórios ausentes.", "campos": ausentes}), 422
    try:
        palpite = _get_service().salvar_palpite(
            id_usuario=int(dados["id_usuario"]),
            id_jogo=int(dados["id_jogo"]),
            escolha=dados["escolha"],
        )
        return jsonify({"mensagem": "Palpite registrado com sucesso.", "palpite": palpite}), 201
    except (ErroPalpite, ErroJogo) as e:
        return jsonify(e.to_dict()), 400


@palpites_bp.delete("/")
def remover_palpite():
    dados = request.get_json(silent=True) or {}
    ausentes = [c for c in ["id_usuario", "id_jogo"] if dados.get(c) is None]
    if ausentes:
        return jsonify({"erro": "Campos obrigatÃ³rios ausentes.", "campos": ausentes}), 422

    try:
        palpite = _get_service().remover_palpite_do_jogo(
            id_usuario=int(dados["id_usuario"]),
            id_jogo=int(dados["id_jogo"]),
        )
        return jsonify({"mensagem": "Palpite removido com sucesso.", "palpite": palpite}), 200
    except (ErroPalpite, ErroJogo) as e:
        return jsonify(e.to_dict()), 400

@palpites_bp.patch("/<int:id_palpite>")
def editar_palpite(id_palpite: int):
    """
    Edita a escolha de um palpite (bloqueado se a partida já começou)
    Body JSON:
        id_usuario : int
        escolha    : "time_a" | "empate" | "time_b"
    """
    dados = request.get_json(silent=True) or {}
    if not dados.get("id_usuario") or not dados.get("escolha"):
        return jsonify({"erro": "Informe id_usuario e a nova escolha."}), 422
    try:
        palpite = _get_service().editar_palpite(
            id_palpite=id_palpite,
            id_usuario=int(dados["id_usuario"]),
            nova_escolha=dados["escolha"],
        )
        return jsonify({"mensagem": "Palpite atualizado.", "palpite": palpite}), 200
    except (ErroPalpite, ErroJogo) as e:
        return jsonify(e.to_dict()), 400


@palpites_bp.get("/usuario/<int:id_usuario>")
def palpites_do_usuario(id_usuario: int):
    #Todos os palpites de um usuário com detalhes de cada partida
    palpites = _get_service().palpites_do_usuario(id_usuario)
    return jsonify({"id_usuario": id_usuario, "total": len(palpites), "palpites": palpites}), 200

@palpites_bp.get("/usuario/<int:id_usuario>/pontuacao")
def pontuacao(id_usuario: int):
    #Pontuação total do usuário 
    return jsonify(_get_service().pontuacao_total(id_usuario)), 200

@palpites_bp.get("/<int:id_palpite>")
def buscar_palpite(id_palpite: int):
    id_usuario = request.args.get("id_usuario", type=int)
    if not id_usuario:
        return jsonify({"erro": "Informe o parâmetro id_usuario."}), 422
    try:
        return jsonify(_get_service().buscar_palpite(id_palpite, id_usuario)), 200
    except ErroPalpite as e:
        return jsonify(e.to_dict()), 404

@palpites_bp.post("/avaliar/<int:id_jogo>")
def avaliar_palpites(id_jogo: int):
    """
    Avalia e pontua todos os palpites de uma partida finalizada. Chamar logo após POST /api/jogos/<id>/resultado.
    """
    avaliados = _get_service().avaliar_palpites_do_jogo(id_jogo)
    return jsonify({
        "mensagem": f"{len(avaliados)} palpite(s) avaliado(s).",
        "palpites": avaliados,
    }), 200
