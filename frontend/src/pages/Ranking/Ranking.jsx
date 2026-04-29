import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import "../../styles/ranking.css";


const MOCK_USERS = [
  { id: 1, username: "Rodrigo",  points: 340 },
  { id: 2, username: "Camila",   points: 290 },
  { id: 3, username: "Lucas",    points: 255 },
  { id: 4, username: "Fernanda", points: 210 },
  { id: 5, username: "Pedro",    points: 180 },
  { id: 6, username: "Juliana",  points: 150 },
  { id: 7, username: "Diego",    points: 120 },
  { id: 8, username: "Ana",      points: 95  },
];

const MEDALS = ["🥇", "🥈", "🥉"];
const MEDAL_CLASSES = ["first", "second", "third"];


function Initials({ name, size = 58 }) {
  const initials = name.slice(0, 2).toUpperCase();
  return (
    <div
      className="card-avatar"
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
        <Initials name={user.username} size={rank === 0 ? 68 : 58} />
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

  useEffect(() => {
    /* ── Swap this block for your real API call ────────────────────────
       Example:
       const token = localStorage.getItem("token");
       fetch("http://localhost:5000/api/admin/users", {
         headers: { Authorization: `Bearer ${token}` }
       })
         .then(r => r.json())
         .then(data => {
           const sorted = [...data].sort((a, b) => b.points - a.points);
           setUsers(sorted);
         });
    ─────────────────────────────────────────────────────────────────── */
    const sorted = [...MOCK_USERS].sort((a, b) => b.points - a.points);
    setUsers(sorted);
  }, []);

  const top3 = users.slice(0, 3);
  const rest = users.slice(3);

  
  const podiumOrder = [top3[1], top3[0], top3[2]].filter(Boolean);
  const podiumRanks  = [1, 0, 2];

  return (
    <div className="ranking-page">
     
      <button className="back-btn" onClick={() => navigate(-1)}>
        ← Voltar
      </button>

      
      <h1 className="ranking-title">RANKING</h1>
      <p className="ranking-subtitle">Copa do Mundo — Classificação Geral</p>

      
      <div className="podium-row">
        {podiumOrder.map((user, i) => (
          <PodiumCard key={user.id} user={user} rank={podiumRanks[i]} />
        ))}
      </div>

     
      <div className="ranking-list">
        {rest.map((user, i) => (
          <div key={user.id} className="rank-row">
            <span className="rank-number">{i + 4}</span>
            <div className="rank-avatar">{user.username.slice(0, 2).toUpperCase()}</div>
            <span className="rank-name">{user.username}</span>
            <span className="rank-points"><span>{user.points}</span> pts</span>
          </div>
        ))}
      </div>
    </div>
  );
}
