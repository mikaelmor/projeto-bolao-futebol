import os
import smtplib
from email.message import EmailMessage

from flask import Blueprint, current_app, jsonify, request

from utils.senha import gerar_senha_temporaria, hash_senha


recuperacao_senha_bp = Blueprint(
    "recuperacao_senha",
    __name__,
    url_prefix="/api/recuperacao-senha",
)

SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER", os.getenv("SUPPORT_EMAIL", "suporte.digitalfootball@gmail.com"))
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")


def _repo_usuario():
    return current_app.config["CADASTRO_SERVICE"]._repo


def _enviar_senha_temporaria(destino: str, senha_temporaria: str) -> None:
    if not SMTP_PASSWORD:
        raise RuntimeError("SMTP_PASSWORD nao configurado.")

    email = EmailMessage()
    email["Subject"] = "Recuperacao de senha - GoalPoint"
    email["From"] = SMTP_USER
    email["To"] = destino
    email.set_content(
        "Voce solicitou a recuperacao de senha do GoalPoint.\n\n"
        f"Sua senha temporaria e: {senha_temporaria}\n\n"
        "Entre no sistema com essa senha e altere-a nas configuracoes."
    )

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as smtp:
        smtp.starttls()
        smtp.login(SMTP_USER, SMTP_PASSWORD)
        smtp.send_message(email)


@recuperacao_senha_bp.post("/solicitar")
def solicitar_recuperacao():
    dados = request.get_json(silent=True) or {}
    email = (dados.get("email") or "").strip().lower()

    if not email:
        return jsonify({"erro": "Informe o email cadastrado.", "campo": "email"}), 422

    usuario = _repo_usuario().buscar_por_email(email)
    if not usuario:
        return jsonify({"erro": "Email nao encontrado.", "campo": "email"}), 404

    senha_temporaria = gerar_senha_temporaria()
    usuario.senha_hash = hash_senha(senha_temporaria)
    _repo_usuario().atualizar(usuario)

    try:
        _enviar_senha_temporaria(email, senha_temporaria)
        return jsonify({
            "mensagem": "Senha temporaria enviada para o email cadastrado.",
            "email_enviado": True,
        }), 200
    except Exception as exc:
        return jsonify({
            "mensagem": "Senha temporaria gerada. Configure o SMTP para enviar por email.",
            "email_enviado": False,
            "senha_temporaria": senha_temporaria,
            "detalhe": str(exc),
        }), 200
