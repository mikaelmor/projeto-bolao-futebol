import React, { useState } from 'react';
import './Suporte.css';
import { useNavigate } from 'react-router-dom';


const Suporte = () => {
  const [perguntaAberta, setPerguntaAberta] = useState(null);
  const [mensagemUsuario, setMensagemUsuario] = useState("");
  const navigate = useNavigate();

  const faqData = [
    { pergunta: "Como faço para participar do bolão?", resposta: "Para participar do bolão, o usuário deve realizar um cadastro na plataforma GoalPoint e acessar sua conta através do login. Após entrar no sistema, os jogos disponíveis serão exibidos na página inicial, permitindo que o usuário visualize as partidas e realize seus palpites." },
    { pergunta: "Como faço um palpite em um jogo?", resposta: "O usuário deve acessar a página de palpites, selecionar uma das opções de resultado da partida, podendo escolher vitória de um dos times ou empate." },
    { pergunta: "Como funciona a pontuação do bolão?", resposta: "A pontuação é definida de acordo com a dificuldade do palpite realizado. Considerados mais prováveis geram menos pontos, enquanto palpites corretos em resultados menos prováveis geram mais pontos. Empates possuem uma pontuação específica definida pelo sistema." },
    { pergunta: "Posso alterar meu palpite depois de enviá-lo?", resposta: "Os palpites podem ser alterados somente antes do início da partida.Os palpites podem ser alterados somente antes do início da partida. Após o começo do jogo, o sistema bloqueia alterações para garantir a integridade do bolão." },
    { pergunta: "Onde posso acompanhar minha pontuação?", resposta: "A pontuação pode ser acompanhada na página de ranking, onde os usuários são classificados de acordo com os pontos acumulados ao longo das partidas." },
    { pergunta: "O que acontece se eu não fizer um palpite?", resposta: "Caso não realize o palpite, o usuário não receberá pontos referentes àquele jogo, e a partida será considerada como não participada pelo sistema. " }
  ];

  const toggleFAQ = (index) => {
    setPerguntaAberta(perguntaAberta === index ? null : index);
  };

  const enviarDuvida = async () => {
    try {
      const response = await fetch('http://localhost:8000/enviar-duvida', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ mensagem: mensagemUsuario })
      });
      if (response.ok) {
        alert("Mensagem enviada com sucesso!");
        setMensagemUsuario("");
      }
    } catch (error) {
      console.error("Erro ao enviar:", error);
    }
  };

  return (

    <div className="suporte-container">
      <h1 className="faq-title">Perguntas Frequentes</h1>
      <div className="styled-wrapper back-button-position">
                <button className="button" onClick={() => navigate("/")} type="button">
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
      <div className="faq-list">
        {faqData.map((item, index) => (
          <div key={index} className="faq-item">
            <div className="faq-header">
              <span>{item.pergunta}</span>
              
              <button 
                onClick={() => toggleFAQ(index)}
                className={`group cursor-pointer outline-none duration-300 ${perguntaAberta === index ? 'rotate-45' : ''}`}
              >
                <svg xmlns="http://www.w3.org/2000/svg" width="40px" height="40px" viewBox="0 0 24 24" className="stroke-zinc-400 fill-none group-hover:fill-zinc-200 duration-300">
                  <path d="M12 22C17.5 22 22 17.5 22 12C22 6.5 17.5 2 12 2C6.5 2 2 6.5 2 12C2 17.5 6.5 22 12 22Z" strokeWidth="1.5"></path>
                  <path d="M8 12H16" strokeWidth="1.5"></path>
                  <path d="M12 16V8" strokeWidth="1.5"></path>
                </svg>
              </button>
            </div>
            {perguntaAberta === index && (
              <div className="faq-answer">
                <p>{item.resposta}</p>
              </div>
            )}
          </div>
        ))}
      </div>

      <div className="contato-section">
        <h3>Ainda tem dúvidas?</h3>
        <p>E-mail: suporte.digitalfootball@gmail.com | Tel: (75) 99162-0921</p>
        <input 
          type="text" 
          placeholder="Digite sua dúvida aqui..." 
          value={mensagemUsuario}
          onChange={(e) => setMensagemUsuario(e.target.value)}
          className="input-duvida"
        />
        <button className="btn-retro" onClick={enviarDuvida}>Enviar Mensagem</button>
      </div>
    </div>
  );
};

export default Suporte;