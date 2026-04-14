import { FaUser, FaLock, FaLockOpen, FaEnvelope, FaIdCard } from "react-icons/fa";
import { useState } from "react";
import { useNavigate } from "react-router-dom";


const Registro = () => {
    const [formData, setFormData] = useState({
        nome: "",
        sobrenome: "",
        email: "",
        cpf: "",
        password: "",
        confirmPassword: ""
    });

    const [showPassword, setShowPassword] = useState(false);
    const [showConfirmPassword, setShowConfirmPassword] = useState(false);

    const navigate = useNavigate();

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({ ...prev, [name]: value }));
    };

    const handleSubmit = async (event) => {
    event.preventDefault();

    if (formData.password !== formData.confirmPassword) {
        alert("As senhas não coincidem!");
        return;
    }

    try {
        const response = await fetch("http://localhost:5173/api/cadastro/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                nome: formData.nome,
                sobrenome: formData.sobrenome,
                email: formData.email,
                cpf: formData.cpf,
                senha: formData.password,
                confirmar_senha: formData.confirmPassword
            })
        });

        const data = await response.json();

        if (!response.ok) {
            alert(data.erro || "Erro ao cadastrar");
            return;
        }

        alert("Cadastro realizado com sucesso");
        navigate("/login");

    } catch (error) {
        console.error(error);
        alert("Erro ao conectar com o servidor");
    }
};

    return (
        <div className="Login">
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

            <div className="login-container register-mode">
                <form onSubmit={handleSubmit}>
                    <h1>Crie sua conta</h1>

                    <div className="input-field">
                        <input type="text" name="nome" placeholder="Nome" required onChange={handleChange} />
                        <FaUser className="icon" />
                    </div>

                    <div className="input-field">
                        <input type="text" name="sobrenome" placeholder="Sobrenome" required onChange={handleChange} />
                        <FaUser className="icon" />
                    </div>

                    <div className="input-field">
                        <input type="email" name="email" placeholder="E-mail" required onChange={handleChange} />
                        <FaEnvelope className="icon" />
                    </div>

                    <div className="input-field">
                        <input type="text" name="cpf" placeholder="CPF" required onChange={handleChange} />
                        <FaIdCard className="icon" />
                    </div>

                    <div className="input-field">
                        <input 
                    type={showPassword ? "text" : "password"}
                    name="password" 
                    placeholder="Senha" 
                    required onChange={handleChange} 
                    />
                    {showPassword ? (
                     <FaLockOpen 
                    className="icon" 
                    onClick={() => setShowPassword(false)} 
                    style={{ cursor: "pointer" }}
                    />
                    ) : (
                    <FaLock 
                    className="icon" 
                    onClick={() => setShowPassword(true)} 
                     style={{ cursor: "pointer" }}
                        />
                    )}
                    </div>
                   
                   <div className="input-field">
                    <input 
                    type={showConfirmPassword ? "text" : "password"}
                    name="confirmPassword" 
                    placeholder="Confirmar Senha" 
                    required 
                    onChange={handleChange} 
                    />
                    {showConfirmPassword ? (
                     <FaLockOpen 
                    className="icon" 
                    onClick={() => setShowConfirmPassword(false)} 
                    style={{ cursor: "pointer" }}
                    />
                    ) : (
                    <FaLock 
                    className="icon" 
                    onClick={() => setShowConfirmPassword(true)} 
                    style={{ cursor: "pointer" }}
                    />
                        )}
                   </div>
                    
                    <button type="submit">Cadastrar</button>

                    <div className="signup-link">
                        <p>Já tem uma conta? <a href="/login" onClick={(e) => { e.preventDefault(); navigate("/login"); }}>Entrar</a></p>
                    </div>
                </form>
            </div>
        </div>
    );
};

export default Registro;