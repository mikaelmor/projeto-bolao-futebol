import { Link } from "react-router-dom";
import imagemFundo from "../../imagens/Home.png";
import { useNavigate } from "react-router-dom";

const Home = () => {

  const navigate = useNavigate(); 


  return (
   <div className="min-h-screen flex flex-col">
      <div
        style={{ backgroundImage: `url(${imagemFundo})` }}
        className="relative w-full h-[85vh] bg-cover bg-center bg-no-repeat"
      >
        <div className="absolute inset-0 bg-black/40"></div>

    <div className="absolute top-8 right-8 flex gap-8 z-50">
          
         <button
            onClick={() => navigate("/login")}
            className="relative cursor-pointer min-w-[90px] py-4 px-10 text-center inline-flex justify-center items-center text-base uppercase text-white rounded-lg transition-all duration-300 group overflow-hidden"
          >
            <span className="relative z-20 font tracking-widest text-[10px]">Login</span>
            <span className="absolute left-[-75%] top-0 h-full w-[50%] bg-white/20 rotate-12 z-10 blur-lg group-hover:left-[125%] transition-all duration-1000 ease-in-out"></span>
            <span className="absolute top-0 left-0 w-1/2 h-[20%] border-l-2 border-t-2 border-[#D4EDF9] rounded-tl-lg transition-all duration-300"></span>
            <span className="absolute top-0 right-0 w-1/2 h-[60%] border-r-2 border-t-2 border-[#D4EDF9] rounded-tr-lg group-hover:h-[90%] transition-all duration-300"></span>
            <span className="absolute bottom-0 left-0 w-1/2 h-[60%] border-l-2 border-b-2 border-[#D4EDF9] rounded-bl-lg group-hover:h-[90%] transition-all duration-300"></span>
            <span className="absolute bottom-0 right-0 w-1/2 h-[20%] border-r-2 border-b-2 border-[#D4EDF9] rounded-br-lg transition-all duration-300"></span>
          </button>

          
          <button
            onClick={() => navigate("/registro")}
            className="relative cursor-pointer min-w-[120px] py-4 px-10 text-center inline-flex justify-center items-center text-base uppercase text-[#66ff66] rounded-lg transition-all duration-300 group overflow-hidden"
          >
            <span className="relative z-10 font tracking-widest text-[10px]">Registro</span>
            <span className="absolute left-[-75%] top-0 h-full w-[50%] bg-white/10 rotate-12 z-10 blur-lg group-hover:left-[125%] transition-all duration-1000 ease-in-out"></span>
            <span className="absolute top-0 left-0 w-1/2 h-[20%] border-l-2 border-t-2 border-[#66ff66] rounded-tl-lg transition-all duration-300"></span>
            <span className="absolute top-0 right-0 w-1/2 h-[60%] border-r-2 border-t-2 border-[#66ff66] rounded-tr-lg group-hover:h-[90%] transition-all duration-300"></span>
            <span className="absolute bottom-0 left-0 w-1/2 h-[60%] border-l-2 border-b-2 border-[#66ff66] rounded-bl-lg group-hover:h-[90%] transition-all duration-300"></span>
            <span className="absolute bottom-0 right-0 w-1/2 h-[20%] border-r-2 border-b-2 border-[#66ff66] rounded-br-lg transition-all duration-300"></span>
          </button>
        </div>
      </div>

      <div className="flex-grow bg-[#353839] border-t-2 border-[#aec4c3] p-8">
        <div className="max-w-screen-xl mx-auto flex flex-col items-center gap-4">
          <div className="flex gap-12">
            <Link to="/suporte" className="text-black hover:text-white font-sans uppercase text-[16px] tracking-wider transition font-static">Fale Conosco</Link>
          </div>
          <p className="text-[14px] text-gray-400 mt-4 uppercase font-mono font italic">
            Copa do Mundo<span className="text-[#ffffff]"> © 2026 |</span> Jogue com Responsabilidade
          </p>
          <h1 className="text-center text-gray-400 font-normal text-sm leading-relaxed max-w-3xl mt-4">Somos a TheDigitalFootball. Uma empresa que veio diretamente para entreter vocês,amantes por futebol. A Copa do Mundo FIFA trás um grande engajamento social, principalmente entre grupos de amigos que costumam organizar bolões informais para acompanhar os jogos. 
            Entretanto, essas apostas coletivas são comumente feitas de forma desordenada, através de mensagens de texto ou até mesmo em anotações manuais, 
            o que pode gerar erros de cálculo e dificuldade no acompanhamento dos resultados. 
            O projeto busca transformar o bolão informal em uma experiência digital organizada, transparente e interativa, fortalecendo a integração social proporcionada pela Copa do Mundo. </h1>       
        </div>
      </div>

    </div>
  );
};
export default Home;