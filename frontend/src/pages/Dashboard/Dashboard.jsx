import React from 'react'
import "./DB-module.css";
import {useState, useEffect} from 'react'
import {Swiper, SwiperSlide } from 'swiper/react'
import {Autoplay, Pagination, Navigation} from 'swiper/modules';
import { Form, useNavigate } from "react-router-dom";
import { Link } from 'react-router-dom';
import { BsArrowLeftShort} from "react-icons/bs";
import logo from "../../imagens/GoalPoint LOGO.png"


import 'swiper/css';
import 'swiper/css/pagination';
import 'swiper/css/navigation';

import slide_imagem1 from "../../imagens/Messi.webp";
import slide_imagem2 from "../../imagens/Mbappe.webp";
import slide_imagem3 from "../../imagens/babap.webp";


function Dashboard() {

    const navigate = useNavigate();

    return(
               
        <div className="main">
            <div className="w-full flex items-center justify-between px-8 py-4 bg-black/40 backdrop-blur-md">

                <div className="flex items-center gap-1">
                    <img src={logo} alt="logo" className="w-10 h-10 object-contain" />
                    <h1 className="text-white italic font-black tracking-0.2em">
                        GOALPOINT
                    </h1>
                </div>

               <div className="flex items-center gap-[12px] font-style: italic text-white font-mono text-lg ">
                    <Link to="/ranking" 
                    className="hover:text-lime-400 transition">Ranking
                    </Link>
                 
                    <Link to="/curiosidades"className="hover:text-lime-400 transition">
                    Curiosidades
                    </Link>
</div>

            </div>

            <button className="brasil-button"
            onClick={() => navigate("/login")}
            type="button"
            >
        <div className="blob1"></div>
        <div className="inner"> ←
               </div>
            </button>


        <div className='container'>
            <Swiper
            spaceBetween={30}
            centeredSlides= {true}
            loop={true}
            slidesPerView={'auto'}
            autoplay={
            {
                delay: 2400,
                disableOnInteraction: false,
            }
        }
            pagination={{el:'.swiper-pagination',clickable:true}}
            modules={[Autoplay, Navigation, Pagination]}
            className='swiper_container'

            >
                <SwiperSlide>
                    <img src={slide_imagem1} alt="slide_image" />
                </SwiperSlide>
                 <SwiperSlide>
                    <img src={slide_imagem2} alt="slide_image" />
                </SwiperSlide>
                 <SwiperSlide>
                    <img src={slide_imagem3} alt="slide_image" />
                </SwiperSlide>

                <div className="slider-controller">
                    <div className="swiper-button-prev slider-arrow"></div>
                    <div className="swiper-button-next slider-arrow"></div>
                    <div className="swiper-pagination"></div>
                </div>

            </Swiper>
        </div>


        </div>


            
        
    )
}

export default Dashboard