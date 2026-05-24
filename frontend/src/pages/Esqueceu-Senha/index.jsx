import { FaEnvelope } from "react-icons/fa";
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { forgotPassword } from "../../services/api";

const EsqueceuSenha = () => {
    const [email, setEmail] = useState("");
    const [loading, setLoading] = useState(false);
    const [mensagem, setMensagem] = useState("");
    const [erro, setErro] = useState("");
    const [senhaTemporaria, setSenhaTemporaria] = useState("");
    const navigate = useNavigate();

    const handleSubmit = async (event) => {
        event.preventDefault();
        setLoading(true);
        setMensagem("");
        setErro("");
        setSenhaTemporaria("");

        try {
            const data = await forgotPassword(email);
            setMensagem(data.mensagem || "Recuperacao solicitada com sucesso.");
            if (data.senha_temporaria) {
                setSenhaTemporaria(data.senha_temporaria);
            }
        } catch (error) {
            setErro(error.message || "Nao foi possivel recuperar a senha.");
        } finally {
            setLoading(false);
        }
    };

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

                    <p style={{ color: "yellow", textAlign: "center", marginBottom: "20px", fontSize: "14px" }}>
                        Insira o seu e-mail cadastrado para receber as instrucoes de recuperacao.
                    </p>

                    <div className="input-field">
                        <input
                            type="email"
                            placeholder="Seu e-mail"
                            required
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                        />
                        <FaEnvelope className="icon" />
                    </div>

                    {mensagem && (
                        <p style={{ color: "#86efac", textAlign: "center", marginBottom: 12, fontSize: 14 }}>
                            {mensagem}
                        </p>
                    )}

                    {senhaTemporaria && (
                        <p style={{ color: "yellow", textAlign: "center", marginBottom: 12, fontSize: 14 }}>
                            Senha temporaria: <strong>{senhaTemporaria}</strong>
                        </p>
                    )}

                    {erro && (
                        <p style={{ color: "#fca5a5", textAlign: "center", marginBottom: 12, fontSize: 14 }}>
                            {erro}
                        </p>
                    )}

                    <button type="submit" disabled={loading}>
                        {loading ? "Enviando..." : "Enviar Instrucoes"}
                    </button>

                    <div className="signup-link">
                        <p>Lembrou a senha? <a href="/login" onClick={(e) => { e.preventDefault(); navigate("/login"); }}>Voltar ao Login</a></p>
                    </div>
                </form>
            </div>
        </div>
    );
};

export default EsqueceuSenha;
