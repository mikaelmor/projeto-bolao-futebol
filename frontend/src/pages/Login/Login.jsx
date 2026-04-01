import {FaUser, FaLock} from "react-icons/fa"
import { useState } from "react"
import { useNavigate } from "react-router-dom"
import './Login.css'


const Login = ()=> {

    const[username,setUsername] = useState("");
    const [password,setPassword] = useState("");
    const navigate = useNavigate();

    const handleSubmit = (event) => {
        event.preventDefault();

      alert("Enviando os dados:" + username + " - " + password);
    }   

    return(
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

        <div className="login-container">
        <form onSubmit={handleSubmit}>
            <h1>Acesse o GoalPoint</h1>   
            <div className="input-field">
            <input type="email" 
            placeholder="E-mail"
            required 
            onChange={(e) => setUsername (e.target.value)}/>
            <FaUser className="icon"/>
            </div>
             <div className="input-field">
            <input 
            type="password"
            placeholder="Senha" 
            onChange={(e) => setPassword (e.target.value)}/>
             <FaLock className="icon"/>
             </div>

            <div className="recall-forget">
                <label>
                    <input type="checkbox" />
                    Lembre de mim 
                </label>
                <a href="/esqueceu-senha" onClick={(e) => { e.preventDefault(); navigate("/esqueceu-senha"); }}>Esqueceu a senha ?</a>
            </div>

           <button href="/dashboard" onClick={(e) => { e.preventDefault(); navigate("/dashboard"); }} >Entrar</button>

            <div className="signup-link">
                <p>Não tem uma conta ? <a href="/registro" onClick={(e) => { e.preventDefault(); navigate("/registro")  ;}}>Registrar</a></p>
            </div>

        </form>
        </div>

        </div>
    )
}
export default Login