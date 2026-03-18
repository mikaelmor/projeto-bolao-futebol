import React from "react";
import ReactDOM from 'react-dom/client'
import { RouterProvider } from "react-router-dom";
import Router from "./routes"
import './index.css'


const rootElement = document.getElementById("root");
if (!rootElement) throw new Error("Failed to find the root element");

const root = ReactDOM.createRoot(rootElement);

root.render(
  <React.StrictMode>
    <RouterProvider router = {Router}/>
  </React.StrictMode>
)