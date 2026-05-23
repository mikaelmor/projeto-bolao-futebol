"""
models/palpite.py
Nomenclatura alinhada ao banco MySQL (time_a / time_b / empate)
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

from models.jogo import Jogo, ResultadoFinal


class EscolhaPalpite(str, Enum):
    TIME_A = "time_a"
    EMPATE = "empate"
    TIME_B = "time_b"


@dataclass
class Palpite:
    id_usuario: int
    id_jogo: int
    escolha: EscolhaPalpite
    id_palpite: int | None = None
    data_palpite: datetime = field(default_factory=datetime.utcnow)
    acertou: bool | None = None     # None = pendente, True/False após finalizar
    pontos_ganhos: int = 0

    def avaliar(self, jogo: Jogo) -> None:
        #Avalia o palpite após a partida finalizar e atribui os pontos
        if jogo.resultado_final is None:
            return
        acertou = self.escolha.value == jogo.resultado_final.value
        self.acertou = acertou
        self.pontos_ganhos = jogo.pontos_para(self.escolha.value) if acertou else 0

    def to_dict(self) -> dict:
        return {
            "id_palpite": self.id_palpite,
            "id_usuario": self.id_usuario,
            "id_jogo": self.id_jogo,
            "escolha": self.escolha.value,
            "data_palpite": self.data_palpite.isoformat(),
            "acertou": self.acertou,
            "pontos_ganhos": self.pontos_ganhos,
        }


#Erros de validação

class ErroPalpite(Exception):
    def __init__(self, mensagem: str, campo: str | None = None):
        super().__init__(mensagem)
        self.mensagem = mensagem
        self.campo = campo

    def to_dict(self) -> dict:
        return {"erro": self.mensagem, "campo": self.campo}


class PalpiteNaoEncontrado(ErroPalpite):
    def __init__(self):
        super().__init__("Palpite não encontrado.", campo="id_palpite")


class PalpiteBloqueado(ErroPalpite):
    def __init__(self):
        super().__init__(
            "A partida já começou. Não é possível criar ou alterar palpites.",
            campo="status",
        )


class PalpiteDuplicado(ErroPalpite):
    def __init__(self):
        super().__init__(
            "Você já fez um palpite para esta partida. Use a edição para alterá-lo.",
            campo="id_jogo",
        )


class EscolhaInvalida(ErroPalpite):
    def __init__(self):
        opcoes = ", ".join(o.value for o in EscolhaPalpite)
        super().__init__(f"Escolha inválida. Use: {opcoes}", campo="escolha")