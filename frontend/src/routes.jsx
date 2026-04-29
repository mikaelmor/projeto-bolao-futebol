import { createBrowserRouter } from "react-router-dom";
import Home from "./pages/Home";
import Login from "./pages/Login/Login";
import AnimatedLoader from "./layout/Animated-Loader.jsx";
import Registro from "./pages/Registro/Register";
import Dashboard from "./pages/Dashboard/Dashboard";
import Suporte from "./pages/FalemConosco";
import EsqueceuSenha from "./pages/Esqueceu-Senha";
import Ranking from "./pages/Ranking/Ranking";
import Curiosidades from "./pages/Curiosidades/WorldCup-History";
import Profile from "./pages/Perfil_do_Usuario/Profile";
import Configurações from "./pages/Configurações";
import Sidebar from "./components/Sidebar.jsx";







const routes = createBrowserRouter([
 {
  element: < AnimatedLoader/>,
  children: [
 { path: "/", element: <Home /> },
 { path: "/login", element: <Login /> },
 { path: "/registro", element: <Registro />},
 { path: "/dashboard", element: < Dashboard />},
 { path: "/suporte", element: < Suporte />},
 { path: "/esqueceu-senha", element: < EsqueceuSenha />},
 { path: "/curiosidades", element: < Curiosidades />},
 { path: "/ranking", element: < Ranking />},
 { path: "/perfil", element: < Profile />},
 { path: "/configurações", element: < Configurações/>},
  ],
 }
]);

export default routes;