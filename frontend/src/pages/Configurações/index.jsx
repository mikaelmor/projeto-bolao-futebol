import { useNavigate } from "react-router-dom";
import React from "react";
import { useEffect, useState } from "react";
import ButtonConfig from "../../ui/ButtonConfig";
import CheckboxConfig from "../../ui/CheckboxConfig";

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
    const savedUser = localStorage.getItem("user_data");
    if (savedUser) {
      const parsed = JSON.parse(savedUser);
      setForm((prev) => ({
        ...prev,
        nome: parsed.nome || "",
        email: parsed.email || "",
      }));
    }
  }, []);

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;

    setForm({
      ...form,
      [name]: type === "checkbox" ? checked : value,
    });
  };

  const handleSave = () => {
    const userData = {
      nome: form.nome,
      email: form.email,
      favorito: form.favorito,
    };

    localStorage.setItem("user_data", JSON.stringify(userData));

    setSaved(true);
    setTimeout(() => setSaved(false), 2000);
  };

  return (
    <div className="min-h-screen text-white p-6 md:p-10 relative overflow-hidden bg-[#020617] flex justify-center pt-25">

  <div className="absolute top-0 left-0 w-full h-[300px] bg-blue-500 opacity-20 blur-[120px]" />
  <div className="absolute bottom-0 left-0 w-[300px] h-[300px] bg-green-400 opacity-20 blur-[120px]" />
  <div className="absolute right-0 top-0 w-[400px] h-full bg-blue-400 opacity-10 blur-[150px]" />

      <div className="relative z-10 max-w-4xl mx-auto space-y-6 translate-y-26">

        <h1 className="text-2xl font-bold tracking-wide">
          Configurações
        </h1>

       
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
            onChange={handleChange}
            placeholder="Email"
            className="w-full p-2 rounded bg-black/40 focus:outline-none focus:ring-2 focus:ring-lime-400 transition"
           style={{fontFamily : "sans-serif"}}/>
           
        </div>

       
        <div className="bg-white/5 backdrop-blur-md border-3 border-white/10 p-7 rounded-xl shadow-[0_0_30px_rgba(255,255,255,0.05)] space-y-3 hover:border-blue-400 transition">
          <h2 className="font-semibold">Segurança</h2>

          <input
            type="password"
            placeholder="Senha atual"
            className="w-full p-2 rounded bg-black/40 focus:outline-none focus:ring-2 focus:ring-blue-400"
          />

          <input
            type="password"
            placeholder="Nova senha"
            className="w-full p-2 rounded bg-black/40 focus:outline-none focus:ring-2 focus:ring-blue-400"
          />

          <input
            type="password"
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

          <CheckboxConfig
            checked={form.notificacoes}
            onChange={(e) =>
            setForm({ ...form, notificacoes: e.target.checked })
            }
            label="Notificações"
           />
        </div>

                
            <div className="flex gap-3">

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