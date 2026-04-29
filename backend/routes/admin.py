from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from models.game import Game
from models.bet import Bet
from models.user import User
from datetime import datetime, timedelta

admin_bp = Blueprint("admin", __name__)

def require_admin():
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    if not user or not user.is_admin:
        return None, (jsonify({"error": "Acesso negado"}), 403)
    return user, None

# ── Set countdown timer (game stays "pre" until admin starts it) ──────────────
@admin_bp.route("/game/<int:game_id>/timer", methods=["POST"])
@jwt_required()
def set_timer(game_id):
    _, err = require_admin()
    if err: return err

    data    = request.get_json()
    minutes = data.get("minutes", 5)

    game = Game.query.get_or_404(game_id)
    game.starts_at = datetime.utcnow() + timedelta(minutes=minutes)
    db.session.commit()
    return jsonify(game.to_dict())

# ── Start game (locks betting) ────────────────────────────────────────────────
@admin_bp.route("/game/<int:game_id>/start", methods=["POST"])
@jwt_required()
def start_game(game_id):
    _, err = require_admin()
    if err: return err

    game = Game.query.get_or_404(game_id)
    if game.status != "pre":
        return jsonify({"error": "Jogo não está em pré-jogo"}), 400

    game.status = "live"
    db.session.commit()
    return jsonify(game.to_dict())

# ── Finish game and set winner ────────────────────────────────────────────────
@admin_bp.route("/game/<int:game_id>/finish", methods=["POST"])
@jwt_required()
def finish_game(game_id):
    _, err = require_admin()
    if err: return err

    data   = request.get_json()
    winner = data.get("winner")   # "1" | "X" | "2"

    if winner not in ("1", "X", "2"):
        return jsonify({"error": "Vencedor inválido"}), 400

    game = Game.query.get_or_404(game_id)
    if game.status != "live":
        return jsonify({"error": "Jogo não está ao vivo"}), 400

    game.status = "finished"
    game.winner = winner

    # Award points to winners
    odd_map = {"1": game.odd1, "X": game.oddX, "2": game.odd2}
    reward  = odd_map[winner]

    bets = Bet.query.filter_by(game_id=game_id, settled=False).all()
    for bet in bets:
        bet.settled = True
        if bet.choice == winner:
            bet.won = True
            user = User.query.get(bet.user_id)
            user.points += bet.points_bet + reward   # return stake + winnings
        else:
            bet.won = False

    db.session.commit()
    return jsonify({"game": game.to_dict(), "bets_settled": len(bets)})

# ── List all users (for admin dashboard) ─────────────────────────────────────
@admin_bp.route("/users", methods=["GET"])
@jwt_required()
def list_users():
    _, err = require_admin()
    if err: return err

    users = User.query.all()
    return jsonify([u.to_dict() for u in users])

# ── Get a single user's bet history (for profile modal) ──────────────────────
@admin_bp.route("/users/<int:target_id>/bets", methods=["GET"])
@jwt_required()
def user_bets(target_id):
    _, err = require_admin()
    if err: return err

    user = User.query.get_or_404(target_id)
    bets = Bet.query.filter_by(user_id=target_id).all()

    result = []
    for bet in bets:
        game = Game.query.get(bet.game_id)
        choice_label = {
            "1": game.time1,
            "X": "Empate",
            "2": game.time2,
        }.get(bet.choice, bet.choice)

        result.append({
            "id":         bet.id,
            "game":       f"{game.time1} x {game.time2}",
            "team":       choice_label,
            "choice":     bet.choice,
            "points_bet": bet.points_bet,
            "settled":    bet.settled,
            "won":        bet.won,
        })

    palpites = len(result)
    acertos  = sum(1 for b in result if b["won"])

    return jsonify({
        "user":     user.to_dict(),
        "bets":     result,
        "palpites": palpites,
        "acertos":  acertos,
        "win_rate": round((acertos / palpites * 100)) if palpites > 0 else 0,
    })

# ── Promote a user to admin ───────────────────────────────────────────────────
@admin_bp.route("/promote/<int:user_id>", methods=["POST"])
@jwt_required()
def promote(user_id):
    _, err = require_admin()
    if err: return err

    user = User.query.get_or_404(user_id)
    user.is_admin = True
    db.session.commit()
    return jsonify(user.to_dict())
