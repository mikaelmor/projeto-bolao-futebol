import React, { useEffect, useMemo, useRef, useState } from "react";
import { fetchSimulatedGames, removeGamePrediction, submitGamePrediction } from "../services/api";
import Brasil from "../imagens/escudo_brasil.png";
import Argentina from "../imagens/escudo_argentina.png";
import Qatar from "../imagens/escudo_catar.png";
import Holanda from "../imagens/escudo_holanda.png";
import Ira from "../imagens/escudo_iran.png";
import Portugal from "../imagens/escudo_portugal.png";
import Espanha from "../imagens/escudo_spain.png";
import America from "../imagens/escudo_usa.png";


const escudos = {
  Brasil,
  Argentina,
  Catar: Qatar,
  Holanda,
  Ira,
  Portugal,
  Espanha,
  EUA: America,
};

const getOrCreateUsuarioId = () => {
  const storageKey = "goalpoint_usuario_simulacao";
  const storedId = localStorage.getItem(storageKey);

  if (storedId) {
    return storedId;
  }

  const newId = crypto.randomUUID ? crypto.randomUUID() : `${Date.now()}-${Math.random()}`;
  localStorage.setItem(storageKey, newId);
  return newId;
};

const formatTime = (isoDate) => {
  if (!isoDate) {
    return "--:--";
  }

  return new Date(isoDate).toLocaleTimeString("pt-BR", {
    hour: "2-digit",
    minute: "2-digit",
  });
};

export default function JogoCard({ searchTerm }) {
  const [jogos, setJogos] = useState([]);
  const [palpites, setPalpites] = useState(() => {
    return JSON.parse(localStorage.getItem("goalpoint_palpites") || "{}");
  });
  const [erro, setErro] = useState("");
  const [highlightedGameId, setHighlightedGameId] = useState(null);
  const cardRefs = useRef({});

  const usuarioId = useMemo(() => getOrCreateUsuarioId(), []);

  const carregarJogos = async () => {
    try {
      const data = await fetchSimulatedGames();
      setJogos(data.jogos || []);
      setErro("");
    } catch (error) {
      setErro(error.message);
    }
  };

  useEffect(() => {
    carregarJogos();
    const intervalId = setInterval(carregarJogos, 2000);

    return () => clearInterval(intervalId);
  }, []);

  useEffect(() => {
    const term = (searchTerm || "").trim().toLowerCase();
    if (!term || jogos.length === 0) {
      return;
    }

    const jogoEncontrado = jogos.find((jogo) => {
      const selecaoA = jogo.selecao_a.toLowerCase();
      const selecaoB = jogo.selecao_b.toLowerCase();
      return selecaoA.includes(term) || selecaoB.includes(term);
    });

    if (jogoEncontrado && cardRefs.current[jogoEncontrado.id]) {
      setHighlightedGameId(jogoEncontrado.id);
      cardRefs.current[jogoEncontrado.id].scrollIntoView({
        behavior: "smooth",
        block: "center",
      });
      const timeoutId = setTimeout(() => setHighlightedGameId(null), 1600);
      return () => clearTimeout(timeoutId);
    }
  }, [searchTerm, jogos]);

  const handlePrediction = async (jogoId, escolha) => {
    try {
      const isSamePrediction = palpites[jogoId] === escolha;

      if (isSamePrediction) {
        await removeGamePrediction({ jogoId, usuarioId });

        setPalpites((prevPalpites) => {
          const nextPalpites = { ...prevPalpites };
          delete nextPalpites[jogoId];
          localStorage.setItem("goalpoint_palpites", JSON.stringify(nextPalpites));
          return nextPalpites;
        });

        await carregarJogos();
        return;
      }

      await submitGamePrediction({ jogoId, usuarioId, escolha });

      setPalpites((prevPalpites) => {
        const nextPalpites = {
          ...prevPalpites,
          [jogoId]: escolha,
        };
        localStorage.setItem("goalpoint_palpites", JSON.stringify(nextPalpites));
        return nextPalpites;
      });

      await carregarJogos();
    } catch (error) {
      alert(error.message);
    }
  };

  const buttonClass = (jogoId, escolha) => {
    const selected = palpites[jogoId] === escolha;
    return `relative inline-block text-xs text-center text-olive-950 border-2 border-olive-950 rounded-[10px] transition-all duration-500 ease-out active:scale-90 overflow-hidden group ${selected ? "bg-green-600 text-white" : ""}`;
  };

  if (erro) {
    return (
      <div className="flex justify-center items-center min-h-screen">
        <div className="bg-white rounded-xl shadow-xl/50 p-6 text-center w-full max-w-[350px]">
          <p className="text-sm text-red-700 font-bold">Erro ao carregar jogos</p>
          <p className="text-xs mt-2">{erro}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="flex justify-center items-center min-h-screen grid grid-cols-1 lg:grid-cols-2 gap-6 px-4 py-8 lg:translate-x-30">
      {jogos.map((jogo) => {
        const isLocked = jogo.status !== "agendado";
        const placarA = jogo.placar?.selecao_a ?? 0;
        const placarB = jogo.placar?.selecao_b ?? 0;
        const placar = jogo.status === "agendado" ? "X" : `${placarA} x ${placarB}`;

        return (
          <div
            key={jogo.id}
            ref={(element) => {
              cardRefs.current[jogo.id] = element;
            }}
            className={`bg-white rounded-xl shadow-xl/50 p-6 text-center w-full max-w-[350px] transition-all duration-300 ${highlightedGameId === jogo.id ? "ring-4 ring-lime-400 scale-[1.02]" : ""}`}
          >
            <p className="text-sm text-emerald-500" style={{ fontFamily: "sans-serif" }}>
              {jogo.fase || "Copa do Mundo"}
            </p>

            <p className="text-xs text-olive-950 mt-1" style={{ fontFamily: "Arial" }}>
              Hoje
            </p>
            <p className="text-xl font-bold">{formatTime(jogo.horario)}</p>

            {jogo.status === "em_andamento" && (
              <p className="text-xs text-red-600 font-bold mt-1">
                Ao vivo {jogo.simulacao?.minuto ?? 0}'
              </p>
            )}

            {jogo.status === "encerrado" && (
              <p className="text-xs text-emerald-700 font-bold mt-1">
                Encerrado
              </p>
            )}

            <div className="flex justify-between items-center mt-4">
              <div className="flex flex-col items-center">
                <img src={escudos[jogo.selecao_a]} className="w-18 h-18" alt={jogo.selecao_a} />
                <p className="text-sm mt-1">{jogo.selecao_a}</p>
              </div>

              <span className="text-black font-bold text-xl">{placar}</span>

              <div className="flex flex-col items-center">
                <img src={escudos[jogo.selecao_b]} className="w-18 h-18" alt={jogo.selecao_b} />
                <p className="text-sm mt-1">{jogo.selecao_b}</p>
              </div>
            </div>

            <div className="flex justify-between gap-2 mt-2">
              <button
                disabled={isLocked}
                onClick={() => handlePrediction(jogo.id, "time1")}
                className={`${buttonClass(jogo.id, "time1")} disabled:opacity-60 disabled:cursor-not-allowed`}
              >
                <span className="relative z-10" style={{ fontFamily: "Monospace" }}>
                  {jogo.selecao_a} <br /> 10 pontos
                </span>
                <span className="absolute inset-0 bg-green-600 translate-y-full group-hover:translate-y-0 transition-transform duration-500"></span>
              </button>

              <button
                disabled={isLocked}
                onClick={() => handlePrediction(jogo.id, "draw")}
                className={`${buttonClass(jogo.id, "draw")} disabled:opacity-60 disabled:cursor-not-allowed`}
              >
                <span className="relative z-10" style={{ fontFamily: "Monospace" }}>
                  Empate <br /> 3 pontos
                </span>
                <span className="absolute inset-0 bg-green-600 translate-y-full group-hover:translate-y-0 transition-transform duration-500"></span>
              </button>

              <button
                disabled={isLocked}
                onClick={() => handlePrediction(jogo.id, "time2")}
                className={`${buttonClass(jogo.id, "time2")} disabled:opacity-60 disabled:cursor-not-allowed`}
              >
                <span className="relative z-10" style={{ fontFamily: "Monospace" }}>
                  {jogo.selecao_b} <br /> 10 pontos
                </span>
                <span className="absolute inset-0 bg-green-600 translate-y-full group-hover:translate-y-0 transition-transform duration-500"></span>
              </button>
            </div>
          </div>
        );
      })}
    </div>
  );
}
