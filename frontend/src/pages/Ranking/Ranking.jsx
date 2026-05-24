import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { fetchRanking } from "../../services/api";
import "../../styles/ranking.css";

const MEDALS = ["1", "2", "3"];
const MEDAL_CLASSES = ["first", "second", "third"];

function Avatar({ name, src, size = 58, className = "card-avatar" }) {
  const initials = (name || "?").slice(0, 2).toUpperCase();

  if (src) {
    return (
      <img
        src={src}
        alt={name}
        className={className}
        style={{ width: size, height: size }}
      />
    );
  }

  return (
    <div
      className={className}
      style={{ width: size, height: size, fontSize: size * 0.35 }}
    >
      {initials}
    </div>
  );
}

function PodiumCard({ user, rank }) {
  return (
    <div className={`card ${MEDAL_CLASSES[rank]}`}>
      <div className="blob" />
      <div className="bg">
        <p className="card-medal">{MEDALS[rank]}</p>
        <Avatar name={user.username} src={user.avatarUrl} size={rank === 0 ? 68 : 58} />
        <p className="card-name">{user.username}</p>
        <p className="card-points">
          <span>{user.points}</span> pts
        </p>
      </div>
    </div>
  );
}

export default function Ranking() {
  const navigate = useNavigate();
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const carregarRanking = async () => {
      try {
        setLoading(true);
        const data = await fetchRanking();
        const ranking = (data.ranking || []).map((user) => ({
          id: user.id_usuario,
          position: user.posicao,
          username: user.nome,
          points: user.pontuacao_total,
          hits: user.acertos,
          predictions: user.total_palpites,
          avatarUrl: user.foto_perfil_url,
        }));

        setUsers(ranking);
        setError("");
      } catch (err) {
        setError(err.message || "Nao foi possivel carregar o ranking.");
      } finally {
        setLoading(false);
      }
    };

    carregarRanking();
  }, []);

  const top3 = users.slice(0, 3);
  const rest = users.slice(3);
  const podiumOrder = [top3[1], top3[0], top3[2]].filter(Boolean);
  const podiumRanks = [1, 0, 2];

  return (
    <div className="ranking-page">
      <button className="back-btn" onClick={() => navigate(-1)}>
        Voltar
      </button>

      <h1 className="ranking-title">RANKING</h1>
      <p className="ranking-subtitle">Copa do Mundo - Classificacao Geral</p>

      {loading && <p className="ranking-status">Carregando ranking...</p>}
      {error && <p className="ranking-status ranking-error">{error}</p>}
      {!loading && !error && users.length === 0 && (
        <p className="ranking-status">Nenhum palpite pontuado ainda.</p>
      )}

      {!loading && !error && users.length > 0 && (
        <>
          <div className="podium-row">
            {podiumOrder.map((user, i) => (
              <PodiumCard key={user.id} user={user} rank={podiumRanks[i]} />
            ))}
          </div>

          <div className="ranking-list">
            {rest.map((user, i) => (
              <div key={user.id} className="rank-row">
                <span className="rank-number">{user.position || i + 4}</span>
                <Avatar name={user.username} src={user.avatarUrl} size={40} className="rank-avatar" />
                <span className="rank-name">{user.username}</span>
                <span className="rank-points">
                  <span>{user.points}</span> pts
                </span>
              </div>
            ))}
          </div>
        </>
      )}
    </div>
  );
}
