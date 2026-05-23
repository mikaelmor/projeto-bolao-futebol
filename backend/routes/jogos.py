# routes/jogos.py   
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
    Lista partidas. Parâmetro opcional ?data=YYYY-MM-DD filtra por data.Sem parâmetro, retorna todas as partidas cadastradas.
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
@jogos_bp.get("/<int:id_jogo>")
def buscar_jogo(id_jogo: int):
    try:
        return jsonify(_get_service().buscar_jogo(id_jogo)), 200
    except ErroJogo as e:
        return jsonify(e.to_dict()), 404


#POST /api/jogos/ 
@jogos_bp.post("/")
def criar_jogo():
    """
    Cadastrar uma nova partida da Copa manualmente
    Body JSON:
        fase - 'quartas', 'semifinal', 'final'
        data jogo - yyyy-mm-dd
        horario hh:mm
        time_a - str
        time_b - str
        pontos_times_a - int
        pontos empate - int
        pontos_time b - int
    """
    dados = request.get_json(silent=True) or {}

    obrigatorios = ["fase", "data_jogo", "horario", "time_a", "time_b", "pontos_time_a", "pontos_empate", "pontos_time_b"]
    ausentes = [c for c in obrigatorios if not dados.get(c)]
    if ausentes:
        return jsonify({"erro": "Campos obrigatórios ausentes.", "campos": ausentes}), 422

    try:
        jogo = _get_service().criar_jogo(
            fase=dados["fase"],
            data_jogo=dados["data_jogo"],
            horario=dados["horario"],
            time_a=dados["time_a"],
            time_b=dados["time_b"],
            pontos_time_a=dados["pontos_time_a"],
            pontos_empate=dados["pontos_empate"],
            pontos_time_b=dados["pontos_time_b"],
           
        )
        return jsonify({"mensagem": "Partida cadastrada com sucesso.", "jogo": jogo}), 201
    except ErroJogo as e:
        return jsonify(e.to_dict()), 400


#PATCH /api/jogos/<id>
@jogos_bp.patch("/<int:id_jogo>")
def atualizar_jogo(id_jogo: int):
    """
    Atualiza campos de uma partida agendada (não funciona em partidas encerradas).Envie apenas os campos que deseja alterar.
    """
    dados = request.get_json(silent=True) or {}
    if not dados:
        return jsonify({"erro": "Nenhum dado enviado para atualização."}), 400

    try:
        jogo = _get_service().atualizar_jogo(id_jogo, dados)
        return jsonify({"mensagem": "Partida atualizada.", "jogo": jogo}), 200
    except ErroJogo as e:
        return jsonify(e.to_dict()), 400

@jogos_bp.post("/<int:id_jogo>/iniciar")
def iniciar_jogo(id_jogo: int):
    """Muda status para em_andamento — bloqueia novos palpites."""
    try:
        return jsonify(_get_service().iniciar_jogo(id_jogo)), 200
    except ErroJogo as e:
        return jsonify(e.to_dict()), 400

#POST /api/jogos/<id>/resultado 
@jogos_bp.post("/<int:id>/resultado")
def registrar_resultado(id_jogo: int):
    
    dados = request.get_json(silent=True) or {}
    if not dados.get("resultado"):
        return jsonify({"erro": "Informe o campo resultado: time_a | empate | time_b"}), 422
    try:
        jogo = _get_service().registrar_resultado(id_jogo, dados["resultado"])
        return jsonify({"mensagem": "Resultado registrado.", "jogo": jogo}), 200
    except ErroJogo as e:
        return jsonify(e.to_dict()), 400

#PATCH /api/jogos/<id>/cancelar
@jogos_bp.patch("/<int:id>/cancelar")
def cancelar_jogo(id_jogo: int):
    try:
        return jsonify(_get_service().cancelar_jogo(id_jogo)), 200
    except ErroJogo as e:
        return jsonify(e.to_dict()), 400