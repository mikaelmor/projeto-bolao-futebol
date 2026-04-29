import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

const Profile = () => {

  const navigate = useNavigate();
  const [image, setImage] = useState(null);

  const handleImageUpload = (e) => {
    const file = e.target.files[0];
    
    if(file){
      setImage(URL.createObjectURL(file))
    }
  }

   return (
    <div className="min-h-screen bg-gradient-to-br from-black via-green-900 to-black text-white flex px-10 py-8 gap-10">
     
      <div className="w-1/3 flex flex-col gap-8">
       <button
      onClick={() => navigate("/dashboard")}
      className="relative w-[56px] h-[56px] bg-transparent cursor-pointer overflow-hidden border-0 group"
        >

  
  <span className="absolute inset-[7px] rounded-full border-4 border-[#f0eeef] transition-all duration-500 group-hover:opacity-0 group-hover:scale-75"></span>

  
  <span className="absolute inset-[7px] rounded-full border-4 border-[#96daf0] scale-[1.3] opacity-0 transition-all duration-500 group-hover:opacity-100 group-hover:scale-100"></span>

  
  <div className="absolute inset-0 flex items-center justify-center translate-y-1 transition-transform duration-400 group-hover:-translate-x-[56px]">
    
    <svg
      viewBox="40 40 46 40"
      className="w-[20px] h-[20px] rotate-180 fill-[#f0eeef]"
    >
      <path d="M46 20.038c0-.7-.3-1.5-.8-2.1l-16-17c-1.1-1-3.2-1.4-4.4-.3-1.2 1.1-1.2 3.3 0 4.4l11.3 11.9H3c-1.7 0-3 1.3-3 3s1.3 3 3 3h33.1l-11.3 11.9c-1 1-1.2 3.3 0 4.4 1.2 1.1 3.3.8 4.4-.3l16-17c.5-.5.8-1.1.8-1.9z" />
    </svg>

    <svg
      viewBox="0 0 46 40"
      className="w-[20px] h-[20px] rotate-180 fill-[#f0eeef]"
    >
      <path d="M46 20.038c0-.7-.3-1.5-.8-2.1l-16-17c-1.1-1-3.2-1.4-4.4-.3-1.2 1.1-1.2 3.3 0 4.4l11.3 11.9H3c-1.7 0-3 1.3-3 3s1.3 3 3 3h33.1l-11.3 11.9c-1 1-1.2 3.3 0 4.4 1.2 1.1 3.3.8 4.4-.3l16-17c.5-.5.8-1.1.8-1.9z" />
    </svg>

  </div>


</button>
        <div className="bg-white/10 backdrop-blur-md rounded-2xl p-8 flex flex-col items-center gap-6 shadow-lg">
          <div className="w-36 h-36 rounded-full bg-gray-300 overflow-hidden flex items-center justify-center">
            {image ? (
              <img src={image} alt="profile" className="w-full h-full object-cover" />
            ) : (
              <span className="text-black">Picture</span>
            )}
          </div>

          <h2 className="text-2xl font-bold">Nome Sobrenome</h2>
          <p className="text-sm text-gray-300">Cadastro: 01/01/2025</p>
        </div>
      </div>

      
      <div className="w-2/3 flex flex-col gap-8">

       
        <div className="grid grid-cols-4 gap-6">
          <div className="bg-white/10 p-6 rounded-xl text-center shadow-md">
            <h3 className="text-3xl font-bold">120</h3>
            <p className="mt-2">Pontos</p>
          </div>
          <div className="bg-white/10 p-6 rounded-xl text-center shadow-md">
            <h3 className="text-3xl font-bold">45</h3>
            <p className="mt-2">Palpites</p>
          </div>
          <div className="bg-white/10 p-6 rounded-xl text-center shadow-md">
            <h3 className="text-3xl font-bold">3º</h3>
            <p className="mt-2">Posição</p>
          </div>
          <div className="bg-white/10 p-6 rounded-xl text-center shadow-md">
            <h3 className="text-3xl font-bold">30</h3>
            <p className="mt-2">Acertos</p>
          </div>
        </div>

        
        <div className="bg-white/10 p-6 rounded-xl shadow-md">
          <p className="text-lg" style={{fontFamily : "sans-serif"}}>Email: usuario@email.com</p>
        </div>

       
        <div className="bg-white/10 p-6 rounded-xl shadow-md">
          <h3 className="mb-4 font-bold text-lg">Histórico de Palpites</h3>
          <ul className="space-y-3 text-sm">
            <li>Brasil 2 x 1 Argentina</li>
            <li>França 3 x 0 Alemanha</li>
            <li>Real Madrid 1 x 1 Barcelona</li>
          </ul>
        </div>

        
        <div>
          <label className="bg-lime-700 px-6 py-3 rounded-xl cursor-pointer hover:scale-105 transition inline-block font-light text-olive-300"
           style={{fontFamily : "Arial"}} >
            Adicionar imagem
            <input
              type="file"
              accept="image/*"
              onChange={handleImageUpload}
              className="hidden"
            />
          </label>
        </div>
      </div>
    </div>

   )
};

export default Profile;