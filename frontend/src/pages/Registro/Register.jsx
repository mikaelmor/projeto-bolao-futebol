import { FaUser, FaLock, FaLockOpen, FaEnvelope, FaIdCard } from "react-icons/fa";
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { registerUser } from "../../services/api";

const formatCpf = (value) => {
    const cpfNumbers = value.replace(/\D/g, "").slice(0, 11);

    if (cpfNumbers.length <= 3) {
        return cpfNumbers;
    }

    if (cpfNumbers.length <= 6) {
        return `${cpfNumbers.slice(0, 3)}.${cpfNumbers.slice(3)}`;
    }

    if (cpfNumbers.length <= 9) {
        return `${cpfNumbers.slice(0, 3)}.${cpfNumbers.slice(3, 6)}.${cpfNumbers.slice(6)}`;
    }

    return `${cpfNumbers.slice(0, 3)}.${cpfNumbers.slice(3, 6)}.${cpfNumbers.slice(6, 9)}-${cpfNumbers.slice(9)}`;
};

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

    const handleChange = (event) => {
        const { name, value } = event.target;
        const fieldValue = name === "cpf" ? formatCpf(value) : value;

        setFormData((prevData) => ({
            ...prevData,
            [name]: fieldValue
        }));
    };

    const handleSubmit = async (event) => {
        event.preventDefault();

        if (formData.password !== formData.confirmPassword) {
            alert("As senhas nao conferem.");
            return;
        }

        try {
            await registerUser({
                nome: `${formData.nome} ${formData.sobrenome}`,
                email: formData.email,
                cpf: formData.cpf,
                senha: formData.password,
            });

            navigate("/login");
        } catch (error) {
            alert(error.message);
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
                        <input
                            type="text"
                            name="cpf"
                            placeholder="CPF"
                            required
                            value={formData.cpf}
                            onChange={handleChange}
                            inputMode="numeric"
                            maxLength={14}
                        />
                        <FaIdCard className="icon" />
                    </div>

                    <div className="input-field">
                        <input 
                    type={showPassword ? "text" : "password"}
                    name="password" 
                    placeholder="Senha" 
                    required
                    minLength={5}
                    pattern="^(?=.*[A-Za-z0-9])(?=.*[!@#$%&*]).{5,}$"
                    title="A senha deve ter pelo menos 5 caracteres, uma letra ou numero e um caractere especial (!@#$%&*)"
                    onChange={handleChange} 
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
                    minLength={5}
                    pattern="^(?=.*[A-Za-z0-9])(?=.*[!@#$%&*]).{5,}$"
                    title="A senha deve ter pelo menos 5 caracteres, uma letra ou numero e um caractere especial (!@#$%&*)"
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
