# routes/jogos.py   blueprint Flask com os endpoints do módulo de partidas da Copa do mundo

from datetime import date

from flask import Blueprint, jsonify, request

from models.jogo import ErroJogo
from services.jogo_service import JogoService

jogos_bp = Blueprint("jogos", __name__, url_prefix="/api/jogos")


def _get_service() -> JogoService:
    from flask import current_app
    return current_app.config["JOGO_SERVICE"]


#GET/api/jogos/hoje
@jogos_bp.get("/hoje")
def jogos_hoje():
    #Retorna todas as partidas do dia atual
    jogos = _get_service().jogos_do_dia()
    return jsonify({
        "data": date.today().isoformat(),
        "total": len(jogos),
        "partidas": jogos,
    }), 200


#GET /api/jogos/?data=YYYY-MM-DD
@jogos_bp.get("/")
def listar_jogos():
    """
    Lista partidas. Parâmetro opcional ?data=YYYY-MM-DD filtra por data.
    Sem parâmetro, retorna todas as partidas cadastradas.
    """
    data_param = request.args.get("data")
    service = _get_service()

    if data_param:
        try:
            data = date.fromisoformat(data_param)
        except ValueError:
            return jsonify({"erro": "Formato de data inválido. Use YYYY-MM-DD."}), 400
        jogos = service.jogos_do_dia(data)
        return jsonify({"data": data_param, "total": len(jogos), "partidas": jogos}), 200

    jogos = service.listar_todos()
    return jsonify({"total": len(jogos), "partidas": jogos}), 200


#GET /api/jogos/<id>
@jogos_bp.get("/<int:id>")
def buscar_jogo(id: int):
    try:
        return jsonify(_get_service().buscar_jogo(id)), 200
    except ErroJogo as e:
        return jsonify(e.to_dict()), 404


#POST /api/jogos/ 
@jogos_bp.post("/")
def criar_jogo():
    """
    Cadastrar uma nova partida da Copa manualmente

    Body JSON:
        selecao_a : str  — ex: "Brasil"
        selecao_b : str  — ex: "Argentina"
        horario   : str  — ISO 8601, ex: "2026-06-10T20:00:00"
        fase      : str  — ex: "Fase de Grupos", "Semifinal", "Final"
        estadio   : str  — ex: "MetLife Stadium, EUA"
        grupo     : str  — opcional, ex: "Grupo C"
    """
    dados = request.get_json(silent=True) or {}

    obrigatorios = ["selecao_a", "selecao_b", "horario", "fase", "estadio"]
    ausentes = [c for c in obrigatorios if not dados.get(c)]
    if ausentes:
        return jsonify({"erro": "Campos obrigatórios ausentes.", "campos": ausentes}), 422

    try:
        jogo = _get_service().criar_jogo(
            selecao_a=dados["selecao_a"],
            selecao_b=dados["selecao_b"],
            horario=dados["horario"],
            fase=dados["fase"],
            estadio=dados["estadio"],
            grupo=dados.get("grupo"),
        )
        return jsonify({"mensagem": "Partida cadastrada com sucesso.", "jogo": jogo}), 201
    except ErroJogo as e:
        return jsonify(e.to_dict()), 400


#PATCH /api/jogos/<id>
@jogos_bp.patch("/<int:id>")
def atualizar_jogo(id: int):
    """
    Atualiza campos de uma partida agendada (não funciona em partidas encerradas).
    Envie apenas os campos que deseja alterar.
    """
    dados = request.get_json(silent=True) or {}
    if not dados:
        return jsonify({"erro": "Nenhum dado enviado para atualização."}), 400

    try:
        jogo = _get_service().atualizar_jogo(id, dados)
        return jsonify({"mensagem": "Partida atualizada.", "jogo": jogo}), 200
    except ErroJogo as e:
        return jsonify(e.to_dict()), 400


#POST /api/jogos/<id>/resultado 
@jogos_bp.post("/<int:id>/resultado")
def registrar_resultado(id: int):
    """
    Registra o placar final e encerra a partida.
    Quando o módulo de palpites estiver pronto, esse endpoint
    também vai disparar o cálculo de pontuação dos usuários.

    Body JSON:
        placar_a : int  — gols da seleção A
        placar_b : int  — gols da seleção B
    """
    dados = request.get_json(silent=True) or {}

    if "placar_a" not in dados or "placar_b" not in dados:
        return jsonify({"erro": "Informe placar_a e placar_b."}), 422

    try:
        jogo = _get_service().registrar_resultado(
            id=id,
            placar_a=int(dados["placar_a"]),
            placar_b=int(dados["placar_b"]),
        )
        return jsonify({"mensagem": "Resultado registrado.", "jogo": jogo}), 200
    except ErroJogo as e:
        return jsonify(e.to_dict()), 400


#PATCH /api/jogos/<id>/cancelar
@jogos_bp.patch("/<int:id>/cancelar")
def cancelar_jogo(id: int):
    try:
        jogo = _get_service().cancelar_jogo(id)
        return jsonify({"mensagem": "Partida cancelada.", "jogo": jogo}), 200
    except ErroJogo as e:
        return jsonify(e.to_dict()), 400