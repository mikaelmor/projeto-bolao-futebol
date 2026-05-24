import { useNavigate } from "react-router-dom";
import React from "react";
import { useEffect, useState } from "react";
import ButtonConfig from "../../ui/ButtonConfig";
import { fetchUserSettings, saveUserSettings } from "../../services/api";

const Configurações = () => {

    const navigate = useNavigate()

     const [form, setForm] = useState({
    nome: "",
    email: "",
    senhaAtual: "",
    novaSenha: "",
    confirmarSenha: "",
    favorito: "Brasil",
    notificacoes: true,
  });

   const [saved, setSaved] = useState(false);

  useEffect(() => {
    const carregarConfiguracoes = async () => {
      try {
        const data = await fetchUserSettings();
        setForm((prev) => ({
          ...prev,
          nome: data.nome || "",
          email: data.email || "",
          favorito: data.favorito || "Brasil",
          notificacoes: data.notificacoes ?? true,
        }));
      } catch (error) {
        alert(error.message);
        navigate("/login");
      }
    };

    carregarConfiguracoes();
  }, [navigate]);

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;

    setForm({
      ...form,
      [name]: type === "checkbox" ? checked : value,
    });
  };

  const handleSave = async () => {
    try {
      const data = await saveUserSettings({
        nome: form.nome,
        email: form.email,
        senhaAtual: form.senhaAtual,
        novaSenha: form.novaSenha,
        confirmarSenha: form.confirmarSenha,
        favorito: form.favorito,
      });

      localStorage.setItem("user", JSON.stringify({
        nome: data.configuracoes.nome,
        email: data.configuracoes.email,
      }));

      setForm((prev) => ({
        ...prev,
        nome: data.configuracoes.nome,
        senhaAtual: "",
        novaSenha: "",
        confirmarSenha: "",
      }));
      setSaved(true);
      setTimeout(() => setSaved(false), 2000);
    } catch (error) {
      alert(error.message);
    }
  };

  return (
    <div className="min-h-screen text-white p-4 sm:p-6 md:p-10 relative overflow-y-auto overflow-x-hidden bg-[#020617] flex justify-center pt-8 md:pt-25">

  <div className="absolute top-0 left-0 w-full h-[300px] bg-blue-500 opacity-20 blur-[120px]" />
  <div className="absolute bottom-0 left-0 w-[300px] h-[300px] bg-green-400 opacity-20 blur-[120px]" />
  <div className="absolute right-0 top-0 w-[400px] h-full bg-blue-400 opacity-10 blur-[150px]" />

      <div className="relative z-10 w-full max-w-4xl mx-auto space-y-6 md:translate-y-10">

        <h1 className="text-2xl font-bold tracking-wide">
          Configurações
        </h1>

        {saved && (
          <div className="bg-lime-500/20 border border-lime-400 text-lime-100 p-3 rounded-lg">
            alterações realizadas com sucesso
          </div>
        )}

       
        <div className="bg-white/5 backdrop-blur-md border-4 border-white/10 p-6 rounded-xl shadow-[0_0_30px_rgba(255,255,255,0.05)] space-y-3 hover:border-lime-400 transition">
          <h2 className="font-semibold">Conta</h2>

          <input
            name="nome"
            value={form.nome}
            onChange={handleChange}
            placeholder="Nome"
            className="w-full p-2 rounded bg-black/40 focus:outline-none focus:ring-2 focus:ring-lime-400 transition"
           style={{fontFamily : "sans-serif"}}/>

          <input
            name="email"
            value={form.email}
            readOnly
            placeholder="Email"
            className="w-full p-2 rounded bg-black/40 focus:outline-none focus:ring-2 focus:ring-lime-400 transition"
           style={{fontFamily : "sans-serif"}}/>
           
        </div>

       
        <div className="bg-white/5 backdrop-blur-md border-3 border-white/10 p-7 rounded-xl shadow-[0_0_30px_rgba(255,255,255,0.05)] space-y-3 hover:border-blue-400 transition">
          <h2 className="font-semibold">Segurança</h2>

          <input
            type="password"
            name="senhaAtual"
            value={form.senhaAtual}
            onChange={handleChange}
            placeholder="Senha atual"
            className="w-full p-2 rounded bg-black/40 focus:outline-none focus:ring-2 focus:ring-blue-400"
          />

          <input
            type="password"
            name="novaSenha"
            value={form.novaSenha}
            onChange={handleChange}
            placeholder="Nova senha"
            className="w-full p-2 rounded bg-black/40 focus:outline-none focus:ring-2 focus:ring-blue-400"
          />

          <input
            type="password"
            name="confirmarSenha"
            value={form.confirmarSenha}
            onChange={handleChange}
            placeholder="Confirmar senha"
            className="w-full p-2 rounded bg-black/40 focus:outline-none focus:ring-2 focus:ring-blue-400"
          />
        </div>

        
        <div className="bg-white/5 backdrop-blur-md border-3 border-white/10 p-6 rounded-xl shadow-[0_0_30px_rgba(255,255,255,0.05)] space-y-3 hover:border-green-400 transition">
          <h2 className="font-semibold" >Preferências</h2>

          <select
            name="favorito"
            value={form.favorito}
            onChange={handleChange}
            className="w-full p-2 rounded bg-black/40"
           style={{fontFamily : "sans-serif"}}>
            <option>Brasil</option>
            <option>Argentina</option>
            <option>França</option>
          </select>

          
        </div>

                
            <div className="flex flex-wrap gap-3">

                <ButtonConfig onClick={handleSave}>
                    Salvar
                </ButtonConfig>

                <ButtonConfig onClick={() => navigate("/dashboard")}
                  variant="danger">
                    Voltar
                    </ButtonConfig>

            </div>

      </div>
    </div>
  );
  
}

export default Configurações
