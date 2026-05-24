from flask import Blueprint, current_app, jsonify, request

from utils.senha import hash_senha, validar_forca_senha, verificar_senha


configuracoes_bp = Blueprint("configuracoes", __name__, url_prefix="/api/configuracoes")


def _usuario_logado():
    auth_header = request.headers.get("Authorization", "")
    token = auth_header.removeprefix("Bearer ").strip()
    if not token:
        token = request.headers.get("X-Session-Token", "").strip()

    email = current_app.config.get("SESSION_TOKENS", {}).get(token)
    if not email:
        return None

    repo = current_app.config["CADASTRO_SERVICE"]._repo
    return repo.buscar_por_email(email)


@configuracoes_bp.get("/me")
def buscar_configuracoes():
    usuario = _usuario_logado()
    if not usuario:
        return jsonify({"erro": "Usuario nao autenticado."}), 401

    preferencias = current_app.config.setdefault("USER_SETTINGS", {}).get(usuario.email, {})
    return jsonify({
        "nome": usuario.nome,
        "email": usuario.email,
        "favorito": preferencias.get("favorito", "Brasil"),
        "notificacoes": preferencias.get("notificacoes", True),
    }), 200


@configuracoes_bp.put("/me")
def salvar_configuracoes():
    usuario = _usuario_logado()
    if not usuario:
        return jsonify({"erro": "Usuario nao autenticado."}), 401

    dados = request.get_json(silent=True) or {}
    email_enviado = (dados.get("email") or usuario.email).strip().lower()
    if email_enviado != usuario.email:
        return jsonify({"erro": "O email da conta nao pode ser diferente do email logado."}), 400

    nome = (dados.get("nome") or usuario.nome).strip()
    if len(nome) < 2:
        return jsonify({"erro": "Nome deve ter pelo menos 2 caracteres.", "campo": "nome"}), 400

    senha_atual = dados.get("senhaAtual") or ""
    nova_senha = dados.get("novaSenha") or ""
    confirmar_senha = dados.get("confirmarSenha") or ""

    if senha_atual or nova_senha or confirmar_senha:
        if not senha_atual:
            return jsonify({"erro": "Informe a senha atual para alterar a senha.", "campo": "senhaAtual"}), 400
        if not verificar_senha(senha_atual, usuario.senha_hash):
            return jsonify({"erro": "Senha atual incorreta.", "campo": "senhaAtual"}), 400
        if nova_senha != confirmar_senha:
            return jsonify({"erro": "A nova senha e a confirmacao nao conferem.", "campo": "confirmarSenha"}), 400

        senha_valida, mensagem = validar_forca_senha(nova_senha)
        if not senha_valida:
            return jsonify({"erro": mensagem, "campo": "novaSenha"}), 400

        usuario.senha_hash = hash_senha(nova_senha)

    usuario.nome = nome
    current_app.config["CADASTRO_SERVICE"]._repo.atualizar(usuario)

    preferencias = current_app.config.setdefault("USER_SETTINGS", {})
    preferencias[usuario.email] = {
        "favorito": dados.get("favorito") or "Brasil",
        "notificacoes": bool(dados.get("notificacoes", True)),
    }

    return jsonify({
        "mensagem": "alterações realizadas com sucesso",
        "configuracoes": {
            "nome": usuario.nome,
            "email": usuario.email,
            **preferencias[usuario.email],
        },
    }), 200
