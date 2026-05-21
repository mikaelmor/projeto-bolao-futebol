#routes/ranking.py
# #ranking geral GoalPoint

from flask import Blueprint, jsonify
from services.ranking_service import RankingService

ranking_bp = Blueprint("ranking", __name__, url_prefix="/api/ranking")


def _get_service() -> RankingService:
    from flask import current_app
    return current_app.config["RANKING_SERVICE"]


@ranking_bp.get("/")
def ranking_geral():
    """
    Retorna o ranking geral de todos os usuários ordenado por pontuação.
    Resposta:
        [
          { "posicao": 1, "nome": "Maria", "pontuacao_total": 28,
            "acertos": 3, "total_palpites": 4 },
          ...
        ]
    """
    ranking = _get_service().ranking_geral()
    return jsonify({
        "total_participantes": len(ranking),
        "ranking": ranking,
    }), 200