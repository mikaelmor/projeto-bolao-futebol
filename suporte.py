from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Duvida(BaseModel):
    mensagem: str

    CONTACT_EMAIL = "suporte.digitalfootball@gmail.com"

    @app.post("/enviar-duvida")
    async def enviar_duvida(duvida: Duvida):
        if not duvida.mensagem:
            raise HTTPException(status_code=400, detail="A mensagem não pode estar vazia. ")
        