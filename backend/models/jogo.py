from dataclasses import dataclass, field
from datetime import datetime, date
from enum import Enum


class StatusJogo(str, Enum):
    AGENDADO     = "agendado"      
    EM_ANDAMENTO = "em_andamento"
    ENCERRADO    = "encerrado"
    CANCELADO    = "cancelado"


@dataclass
class Jogo:
    selecao_a: str             # primeira seleção 
    selecao_b: str             # segunda seleção
    horario: datetime          # data e hora da partida
    fase: str                  # Fase de Grupos
    estadio: str               # local da partida 
    id: int | None = None
    status: StatusJogo = StatusJogo.AGENDADO
    grupo: str | None = None   

    # preenchidos após o encerramento
    placar_a: int | None = None
    placar_b: int | None = None

    criado_em: datetime = field(default_factory=datetime.utcnow)
    @property
    def vencedor(self) -> str | None:
        #Retorna o nome da seleção vencedora, empate ou None se não encerrado
        if self.status != StatusJogo.ENCERRADO:
            return None
        if self.placar_a > self.placar_b:
            return self.selecao_a
        if self.placar_b > self.placar_a:
            return self.selecao_b
        return "empate"

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "selecao_a": self.selecao_a,
            "selecao_b": self.selecao_b,
            "horario": self.horario.isoformat(),
            "fase": self.fase,
            "estadio": self.estadio,
            "grupo": self.grupo,
            "status": self.status.value,
            "placar": self._placar_dict(),
            "vencedor": self.vencedor,
            "criado_em": self.criado_em.isoformat(),
        }

    def _placar_dict(self) -> dict | None:
        if self.placar_a is None:
            return None
        return {
            "selecao_a": self.placar_a,
            "selecao_b": self.placar_b,
            "display": f"{self.selecao_a} {self.placar_a} x {self.placar_b} {self.selecao_b}",
        }


class ErroJogo(Exception):
    def __init__(self, mensagem: str, campo: str | None = None):
        super().__init__(mensagem)
        self.mensagem = mensagem
        self.campo = campo

    def to_dict(self) -> dict:
        return {"erro": self.mensagem, "campo": self.campo}


class JogoNaoEncontrado(ErroJogo):
    def __init__(self):
        super().__init__("Jogo não encontrado.", campo="id")


class JogoJaEncerrado(ErroJogo):
    def __init__(self):
        super().__init__("Este jogo já foi encerrado e não pode ser alterado.", campo="status")


class DadosJogoInvalidos(ErroJogo):
    pass