import { FaEnvelope } from "react-icons/fa"
import { useState } from "react"
import { useNavigate } from "react-router-dom"


const EsqueceuSenha = () => {
    const [email, setEmail] = useState("");
    const navigate = useNavigate();

    const handleSubmit = (event) => {
        event.preventDefault();
        alert("Link de recuperação enviado para: " + email);
    }

    return (
        <div className="Login">
            <div className="styled-wrapper back-button-position">
                <button className="button" onClick={() => navigate("/login")} type="button">
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

            <div className="login-container">
                <form onSubmit={handleSubmit}>
                    <h1>Recuperar Senha</h1>
                    
                    <p style={{ color: 'yellow', textAlign: 'center', marginBottom: '20px', fontSize: '14px' }}>
                        Insira o seu e-mail cadastrado para receber as instruções de recuperação.
                    </p>

                    <div className="input-field">
                        <input 
                            type="email" 
                            placeholder="Seu e-mail"
                            required 
                            onChange={(e) => setEmail(e.target.value)}
                        />
                        <FaEnvelope className="icon"/>
                    </div>

                    <button type="submit">Enviar Instruções</button>

                    <div className="signup-link">
                        <p>Lembrou a senha? <a href="/login" onClick={(e) => { e.preventDefault(); navigate("/login"); }}>Voltar ao Login</a></p>
                    </div>
                </form>
            </div>
        </div>
    )
}

export default EsqueceuSenha;