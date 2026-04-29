import React from "react";
import {useNavigate} from "react-router-dom";
import { useState, useEffect } from "react";
import uruguai from "../../imagens/1930_uruguai.webp";
import messibg from "../../imagens/Messi_info.webp"
import argentina from "../../imagens/argentina.webp"
import franca from "../../imagens/franca.webp"
import babap from "../../imagens/babap.webp"
import seteaum from "../../imagens/seteaum.png"
import german from "../../imagens/alemanha.webp"
import spain from "../../imagens/espanha.webp"
import andres from "../../imagens/andres_viadao.webp"
import kisidane from "../../imagens/2006 worldcup.png"
import italy from "../../imagens/italia.webp"
import ronaldo from "../../imagens/ronaldo.webp"
import brasil from "../../imagens/brasil.webp"
import "./curiosidades.css"

const Curiosidades = () => {

    const navigate = useNavigate();

    const slides = [
         {
            bg: uruguai,
            text: "A Copa do Mundo surgiu porque o futebol já era popular, mas não tinha um torneio global com jogadores profissionais. No início, as competições eram regionais ou olímpicas, limitadas a atletas amadores. A FIFA, criada em 1904, buscou organizar o esporte e, após tentativas sem sucesso, decidiu em 1928 criar uma competição própria. A primeira edição ocorreu em 1930, no Uruguai, escolhido por sua força no futebol e capacidade de organização, mesmo com poucas seleções devido às dificuldades da época. Com o tempo, a Copa cresceu e se tornou um evento global, influenciando não só o esporte, mas também a economia, a cultura e a política. Países usam o torneio para ganhar visibilidade internacional, enquanto o evento movimenta grandes investimentos e audiência mundial. Hoje, a Copa continua evoluindo, mantendo sua relevância como o principal evento do futebol e um dos maiores do mundo."
        },
          {
            bg: messibg,
            img: argentina,
            text: "A Copa de 2022 foi vencida pela Argentina, liderada por Lionel Messi, que fez uma das campanhas individuais mais completas da história do torneio. Ele foi eleito o melhor jogador da Copa, a chamada Bola de Ouro. Messi não apenas liderou tecnicamente, mas também marcou em todas as fases decisivas, incluindo a final, algo raríssimo na história do torneio . Esse título consolidou sua carreira como uma das maiores do futebol mundial."
        },
        {
            bg: babap,
            img: franca,
            text: "Em 2018, a campeã foi a França, com uma seleção jovem e extremamente rápida. O principal destaque coletivo foi Kylian Mbappé. A França chegou à Copa com uma geração forte que já vinha sendo construída desde 2014, combinando juventude e experiência."
        },
        {
            bg: seteaum,
            img: german,
            text: "Na Copa de 2014, a Alemanha conquistou o título após anos de reconstrução. Mas dentro da equipe campeã, nomes como Thomas Müller e Manuel Neuer foram fundamentais. A Alemanha vinha de um projeto de longo prazo iniciado após o fracasso na Euro 2000, focado em formação de jogadores e modernização tática. Em 2014, esse projeto atingiu o auge. A campanha foi dominante, incluindo a histórica vitória por 7 a 1 sobre o Brasil. "
        },
        {
            bg: andres,
            img: spain,
            text: "A Espanha venceu a Copa de 2010 com um estilo único, baseado na posse de bola e controle do jogo. O símbolo da Espanha foi Andrés Iniesta. A seleção espanhola vinha de um ciclo vitorioso iniciado na Euro 2008 e tinha como base jogadores do Barcelona. Sua trajetória na Copa foi diferente das outras campeãs, com jogos de placar baixo e domínio técnico. "
        },
        {
            bg: kisidane,
            img: italy,
            text: "Em 2006, a Itália foi campeã em uma campanha marcada por solidez defensiva.O melhor jogador do torneio foi Zinedine Zidane , mesmo com a derrota na final. Pela Itália, o grande destaque foi Fabio Cannavaro. A cabeçada de Zinedine Zidane em Marco Materazzi, que resultou em sua expulsão na prorrogação. Mesmo assim, Zidane foi eleito o melhor jogador do torneio. Cannavaro teve atuação histórica, liderando a defesa com desempenho quase impecável, o que lhe rendeu a Bola de Ouro naquele ano."
        },
        {
            bg: ronaldo,
            img: brasil,
            text: "Na Copa de 2002, o Brasil conquistou seu quinto título com uma campanha dominante. O nome que marcou a Copa foi Ronaldo Nazário. O Brasil vinha de uma fase irregular nas eliminatórias, chegando desacreditado. No entanto, durante o torneio, mostrou força ofensiva com o trio Ronaldo, Rivaldo e Ronaldinho.Sua trajetória pessoal de superação foi um dos pontos mais marcantes da história das Copas.  "
        }
    ];

    const [items, setItems] = useState(slides);

    const handleNext = () => {
        setItems((prev) => {
            const newArr = [...prev];
            newArr.push(newArr.shift());
            return newArr;
        });
    };

    const handlePrev = () => {
        setItems((prev) => {
            const newArr = [...prev];
            newArr.unshift(newArr.pop());
            return newArr;
        });
    };


    return (
        
        <div className="carousel">

         <div className="styled-wrapper back-button-position">
                <button className="button" onClick={() => navigate("/dashboard")} type="button">
                    <div className="button-box">
                        <span className="button-elem">
                            <svg viewBox="0 0 46 40" xmlns="http://www.w3.org/2000/svg">
                                <path d="M46 20.038c0-.7-.3-1.5-.8-2.1l-16-17c-1.1-1-3.2-1.4-4.4-.3-1.2 1.1-1.2 3.3 0 4.4l11.3 11.9H3c-1.7 0-3 1.3-3 3s1.3 3 3 3h33.1l-11.3 11.9c-1.2 1.1-1.2 3.3 0 4.4 1.2 1.1 3.3.8 4.4-.3l16-17c.5-.5.8-1.1.8-1.9z" />
                            </svg>
                        </span>
                        <span className="button-elem">
                            <svg viewBox="0 0 46 40">
                                <path d="M46 20.038c0-.7-.3-1.5-.8-2.1l-16-17c-1.1-1-3.2-1.4-4.4-.3-1.2 1.1-1.2 3.3 0 4.4l11.3 11.9H3c-1.7 0-3 1.3-3 3s1.3 3 3 3h33.1l-11.3 11.9c-1.2 1.1-1.2 3.3 0 4.4 1.2 1.1 3.3.8 4.4-.3l16-17c.5-.5.8-1.1.8-1.9z" />
                            </svg>
                        </span>
                    </div>
                </button>
            </div>

            <div className="list">
                {items.map((slide, index) => (
                    <div
                        key={index}
                        className="item"
                        style={{ backgroundImage: `url(${slide.bg})` }}
                    >
                        <div className="content">

                            <img 
                                src={slide.img} 
                                alt=""
                                className="content-image"
                            />

                            <p className="des">{slide.text}</p>

                        </div>
                    </div>
                ))}
            </div>
            <div className="arrows">
                <button onClick={handlePrev}>{"<"}</button>
                <button onClick={handleNext}>{">"}</button>
            </div>
            <div className="timeRunning"></div>

        </div>
    );
};
export default Curiosidades