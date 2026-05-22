from flask import Blueprint, jsonify, request


suporte_bp = Blueprint("suporte", __name__, url_prefix="/api/suporte")

CONTACT_EMAIL = "suporte.digitalfootball@gmail.com"


@suporte_bp.post("/enviar-duvida")
def enviar_duvida():
    dados = request.get_json(silent=True) or {}
    mensagem = (dados.get("mensagem") or "").strip()

    if not mensagem:
        return jsonify({"erro": "A mensagem nao pode estar vazia."}), 400

    return jsonify({
        "mensagem": "Duvida enviada com sucesso.",
        "destino": CONTACT_EMAIL,
        "duvida": mensagem,
    }), 200
