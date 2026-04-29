import React from "react";
import Brasil from "../imagens/escudo_brasil.png";
import Argentina from "../imagens/escudo_argentina.png";
import Qatar from "../imagens/escudo_catar.png";
import Holanda from "../imagens/escudo_holanda.png";
import Ira from "../imagens/escudo_iran.png";
import Portugal from "../imagens/escudo_portugal.png";
import Espanha from "../imagens/escudo_spain.png";
import America from "../imagens/escudo_usa.png";


const Jogos = [
  {
    liga: "Copa do Mundo",
    hora: "14:00",
    time1: "Brasil",
    time2: "Argentina",
    escudo1: Brasil,
    escudo2: Argentina,
    odd1: "10 pontos",
    oddX: "3 pontos",
    odd2: "10 pontos"
  },
  {
    liga: "Copa do Mundo",
    hora: "15:00",
    time1: "Holanda",
    time2: "Portugal",
    escudo1: Holanda,
    escudo2: Portugal,
    odd1: "10 pontos",
    oddX: "3 pontos",
    odd2: "10 pontos"
  },
  {
    liga: "Copa do Mundo",
    hora: "16:05",
    time1: "Catar",
    time2: "Espanha",
    escudo1: Qatar,
    escudo2: Espanha,
    odd1: "15 pontos",
    oddX: "3 pontos",
    odd2: "5 pontos"
  },
  {
    liga: "Copa do Mundo",
    hora: "17:00",
    time1: "Irã",
    time2: "EUA",
    escudo1: Ira,
    escudo2: America,
    odd1: "10 pontos",
    oddX: "3 pontos",
    odd2: "10 pontos"
  }
];

export default function JogoCard() {
  
  return (
    <div className="flex justify-center items-center min-h-screen grid grid-cols-2 gap-6 translate-x-30">
      {Jogos.map((jogo, index) => (
        <div
          key={index}
          className="bg-white rounded-xl shadow-xl/50 p-6 text-center w-full max-w-[350px]"
        >
          <p className="text-sm text-emerald-500" style={{ fontFamily: "sans-serif" }}>
            {jogo.liga}
          </p>

          <p className="text-xs text-olive-950 mt-1" style={{ fontFamily: "Arial" }}>
            Hoje
          </p>
          <p className="text-xl font-bold">{jogo.hora}</p>

          <div className="flex justify-between items-center mt-4">
            <div className="flex flex-col items-center">
              <img src={jogo.escudo1} className="w-18 h-18" alt={jogo.time1} />
              <p className="text-sm mt-1">{jogo.time1}</p>
            </div>

            <span className="text-black font-bold text-xl">X</span>

            <div className="flex flex-col items-center">
              <img src={jogo.escudo2} className="w-18 h-18" alt={jogo.time2} />
              <p className="text-sm mt-1">{jogo.time2}</p>
            </div>
          </div>

          <div className="flex justify-between mt-2">
            <button 
              onClick={() => jogo.id && handlePrediction(jogo.id, "time1")}
              className="relative inline-block text-xs text-center text-olive-950 border-2 border-olive-950 rounded-[10px] transition-all duration-500 ease-out active:scale-90 overflow-hidden group"
            >
              <span className="relative z-10" style={{ fontFamily: "Monospace" }}>
                {jogo.time1} <br /> {jogo.odd1}
              </span>
              <span className="absolute inset-0 bg-green-600 translate-y-full group-hover:translate-y-0 transition-transform duration-500"></span>
            </button>

            <button 
              onClick={() => jogo.id && handlePrediction(jogo.id, "draw")}
              className="relative inline-block text-xs text-center text-olive-950 border-2 border-olive-950 rounded-[10px] transition-all duration-500 ease-out active:scale-90 overflow-hidden group"
            >
                  <span className="relative z-10" style={{ fontFamily: "Monospace" }}>
                    Empate <br /> {jogo.oddX}
                  </span>
                  <span className="absolute inset-0 bg-green-600 translate-y-full group-hover:translate-y-0 transition-transform duration-500"></span>
                </button>

            <button 
              onClick={() => jogo.id && handlePrediction(jogo.id, "time2")}
              className="relative inline-block text-xs text-center text-olive-950 border-2 border-olive-950 rounded-[10px] transition-all duration-500 ease-out active:scale-90 overflow-hidden group"
            >
              <span className="relative z-10" style={{ fontFamily: "Monospace" }}>
                {jogo.time2} <br /> {jogo.odd2}
              </span>
              <span className="absolute inset-0 bg-green-600 translate-y-full group-hover:translate-y-0 transition-transform duration-500"></span>
            </button>
          </div>
        </div>
      ))}
    </div>
  );
}