import { createBrowserRouter } from "react-router-dom";
import Home from "./pages/Home";
import Login from "./pages/Login/Login";
import AnimatedLayout from "./layout/Animated-Layout";
import Registro from "./pages/Registro/Register";
import Dashboard from "./pages/Dashboard/Dashboard";
import Suporte from "./pages/FalemConosco";
import EsqueceuSenha from "./pages/Esqueceu-Senha";







const routes = createBrowserRouter([
 {
  element: < AnimatedLayout/>,
  children: [
 { path: "/", element: <Home /> },
 { path: "/login", element: <Login /> },
 { path: "/registro", element: <Registro />},
 { path: "/dashboard", element: < Dashboard />},
 { path: "/suporte", element: < Suporte />},
  { path: "/esqueceu-senha", element: < EsqueceuSenha />},
  ],
 }
]);

export default routes;