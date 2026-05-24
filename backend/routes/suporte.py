import os
import smtplib
from email.message import EmailMessage

from flask import Blueprint, jsonify, request


suporte_bp = Blueprint("suporte", __name__, url_prefix="/api/suporte")

CONTACT_EMAIL = os.getenv("SUPPORT_EMAIL", "suporte.digitalfootball@gmail.com")
SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER", CONTACT_EMAIL)
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")


def _enviar_email_suporte(mensagem: str) -> None:
    if not SMTP_PASSWORD:
        raise RuntimeError("SMTP_PASSWORD nao configurado.")

    email = EmailMessage()
    email["Subject"] = "Nova duvida enviada pelo GoalPoint"
    email["From"] = SMTP_USER
    email["To"] = CONTACT_EMAIL
    email.set_content(
        "Uma nova mensagem foi enviada pela pagina de suporte do GoalPoint.\n\n"
        f"Mensagem:\n{mensagem}"
    )

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as smtp:
        smtp.starttls()
        smtp.login(SMTP_USER, SMTP_PASSWORD)
        smtp.send_message(email)


@suporte_bp.post("/enviar-duvida")
def enviar_duvida():
    dados = request.get_json(silent=True) or {}
    mensagem = (dados.get("mensagem") or "").strip()

    if not mensagem:
        return jsonify({"erro": "A mensagem nao pode estar vazia."}), 400

    try:
        _enviar_email_suporte(mensagem)
    except Exception as exc:
        return jsonify({
            "erro": "Nao foi possivel enviar o email de suporte.",
            "detalhe": str(exc),
        }), 503

    return jsonify({
        "mensagem": "Duvida enviada com sucesso.",
        "destino": CONTACT_EMAIL,
    }), 200
