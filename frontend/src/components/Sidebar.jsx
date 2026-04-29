import { useNavigate } from "react-router-dom";
import { useState } from "react";



const Sidebar = () => {

    const navigate = useNavigate()
    const [openMenu, setOpenMenu] = useState(false);

    return (

                     <div className="sidebar">
                        <button onClick={() => setOpenMenu(!openMenu)}
                            className="bg-transparent border-none text-white text-[20px] cursor-pointer transform transition-duration-200 hover:scale-110"
                            >☰</button>


                           <div className={`absolute top-[30px] right-0 w-[160px] bg-white rounded-lg p-[10px] flex flex-col gap-[10px] transform transition-all durantion-300 ease-out ${openMenu ? "translate-x-0 opacity-100" : "translate-x-5 opacity-0 pointer-events-none"}`}>
                                     <button
                                        onClick={() => navigate("/perfil")}
                                        className="group flex items-center justify-start w-[30px] h-[30px] rounded-full bg-emerald-900 overflow-hidden transition-all duration-300 shadow-md hover:w-[140px] hover:rounded-[40px]"
                                            >
                                        <div className="flex items-center justify-center w-full transition-all duration-300 group-hover:w-[30%] group-hover:pl-[20px]">
                                        <svg viewBox="0 0 24 24" className="w-[20px] fill-white">
                                        <path d="M12 12c2.7 0 5-2.3 5-5s-2.3-5-5-5-5 2.3-5 5 2.3 5 5 5zm0 2c-3.3 0-10 1.7-10 5v3h20v-3c0-3.3-6.7-5-10-5z"/>
                                            </svg>
                                            </div>
                                    <span className="absolute right-17 opacity-0 text-white text-sm font-semibold pr-[10px] transition-all duration-300 group-hover:opacity-100 text-right w-[70%]">
                                            Perfil
                                        </span>
                                    </button>


                                         <button
                                            onClick={() => navigate("/configurações")}
                                            className="group flex items-center justify-start w-[30px] h-[30px] rounded-full bg-emerald-900 overflow-hidden transition-all duration-300 shadow-md hover:w-[160px] hover:rounded-[40px]"
                                                >
                                                    <div className="flex items-center justify-center w-full transition-all duration-300 group-hover:w-[30%] group-hover:pl-[20px]">
                                                        <svg viewBox="0 0 24 24" className="w-[20px] fill-white">
                                                        <path d="M19.14 12.94a7.07 7.07 0 000-1.88l2.03-1.58a.5.5 0 00.12-.64l-1.92-3.32a.5.5 0 00-.6-.22l-2.39.96a7.28 7.28 0 00-1.63-.95l-.36-2.54a.5.5 0 00-.5-.42h-3.84a.5.5 0 00-.5.42l-.36 2.54c-.58.23-1.12.54-1.63.95l-2.39-.96a.5.5 0 00-.6.22L2.71 8.84a.5.5 0 00.12.64l2.03 1.58a7.07 7.07 0 000 1.88L2.83 14.52a.5.5 0 00-.12.64l1.92 3.32a.5.5 0 00.6.22l2.39-.96c.51.41 1.05.72 1.63.95l.36 2.54a.5.5 0 00.5.42h3.84a.5.5 0 00.5-.42l.36-2.54c.58-.23 1.12-.54 1.63-.95l2.39.96a.5.5 0 00.6-.22l1.92-3.32a.5.5 0 00-.12-.64l-2.03-1.58zM12 15.5A3.5 3.5 0 1112 8a3.5 3.5 0 010 7.5z"/>
                                                        </svg>
                                                            </div>
                                                            <span className="absolute right-4 opacity-0 text-white text-sm font-semibold pr-[10px] transition-all duration-300 group-hover:opacity-100 text-right w-[70%]">
                                                Configurações
                                            </span>
                                            </button>


                                    <button
                                    onClick={() => navigate("/")}
                                    className="group flex items-center justify-start w-[30px] h-[30px] rounded-full bg-emerald-900 overflow-hidden transition-all duration-300 shadow-md hover:w-[125px] hover:rounded-[40px] active:translate-x-[2px] active:translate-y-[2px]"
>                                   <div className="flex items-center justify-center w-full transition-all duration-300 group-hover:w-[30%] group-hover:pl-[20px]">
                                    <svg viewBox="0 0 512 512" className="w-[17px] fill-white">
                                    <path d="M377.9 105.9L500.7 228.7c7.2 7.2 11.3 17.1 11.3 27.3s-4.1 20.1-11.3 27.3L377.9 406.1c-6.4 6.4-15 9.9-24 9.9c-18.7 0-33.9-15.2-33.9-33.9l0-62.1-128 0c-17.7 0-32-14.3-32-32l0-64c0-17.7 14.3-32 32-32l128 0 0-62.1c0-18.7 15.2-33.9 33.9-33.9c9 0 17.6 3.6 24 9.9zM160 96L96 96c-17.7 0-32 14.3-32 32l0 256c0 17.7 14.3 32 32 32l64 0c17.7 0 32 14.3 32 32s-14.3 32-32 32l-64 0c-53 0-96-43-96-96L0 128C0 75 43 32 96 32l64 0c17.7 0 32 14.3 32 32s-14.3 32-32 32z"/>
                                    </svg>
                                        </div>
                                    <span className="absolute right-9 w-0 opacity-0 text-white text-[14px] font-semibold transition-all duration-300 group-hover:w-[70%] group-hover:opacity-100 group-hover:pr-[10px]">
                                Sair
                                </span>

                                        </button>
                                 </div>
                          </div>   
                                  
    );
}

export default Sidebar