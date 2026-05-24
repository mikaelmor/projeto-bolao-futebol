from pathlib import Path

from flask import Blueprint, current_app, jsonify, request
from werkzeug.utils import secure_filename


perfil_bp = Blueprint("perfil", __name__, url_prefix="/api/perfil")


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


@perfil_bp.get("/me")
def buscar_perfil():
    usuario = _usuario_logado()
    if not usuario:
        return jsonify({"erro": "Usuario nao autenticado."}), 401

    pontuacao = {
        "pontuacao_total": 0,
        "total_palpites": 0,
        "acertos": 0,
    }
    historico = []

    palpite_service = current_app.config.get("PALPITE_SERVICE")
    if palpite_service and usuario.id is not None:
        pontuacao = palpite_service.pontuacao_total(usuario.id)
        historico = palpite_service.palpites_do_usuario(usuario.id)

    posicao = None
    ranking_service = current_app.config.get("RANKING_SERVICE")
    if ranking_service and usuario.id is not None:
        for linha in ranking_service.ranking_geral():
            if linha["id_usuario"] == usuario.id:
                posicao = linha["posicao"]
                break

    return jsonify({
        "usuario": usuario.to_dict(),
        "email": usuario.email,
        "nome": usuario.nome,
        "foto_perfil_url": usuario.foto_perfil_url,
        "cadastro": usuario.criado_em.strftime("%d/%m/%Y"),
        "pontos": pontuacao.get("pontuacao_total", 0),
        "palpites": pontuacao.get("total_palpites", 0),
        "acertos": pontuacao.get("acertos", 0),
        "posicao": posicao,
        "historico": historico,
    }), 200


@perfil_bp.post("/foto")
def salvar_foto_perfil():
    usuario = _usuario_logado()
    if not usuario:
        return jsonify({"erro": "Usuario nao autenticado."}), 401

    arquivo = request.files.get("foto")
    if not arquivo or not arquivo.filename:
        return jsonify({"erro": "Envie uma imagem no campo foto."}), 400

    if not (arquivo.mimetype or "").startswith("image/"):
        return jsonify({"erro": "O arquivo enviado precisa ser uma imagem."}), 400

    extensao = Path(secure_filename(arquivo.filename)).suffix.lower() or ".png"
    nome_arquivo = f"usuario_{usuario.id}{extensao}"
    pasta_upload = Path(current_app.root_path) / "uploads" / "profile_pictures"
    pasta_upload.mkdir(parents=True, exist_ok=True)

    arquivo.save(pasta_upload / nome_arquivo)

    usuario.foto_perfil_url = f"/uploads/profile_pictures/{nome_arquivo}"
    current_app.config["CADASTRO_SERVICE"]._repo.atualizar(usuario)

    return jsonify({
        "mensagem": "Foto de perfil atualizada com sucesso.",
        "foto_perfil_url": usuario.foto_perfil_url,
    }), 200
