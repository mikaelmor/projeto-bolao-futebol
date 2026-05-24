from dataclasses import dataclass, field
from datetime import datetime, date, time
from enum import Enum


class StatusJogo(str, Enum):
    DISPONIVEL   = "disponivel"    # aberto para palpites
    EM_ANDAMENTO = "em_andamento"  # palpites bloqueados
    FINALIZADO   = "finalizado"
    CANCELADO    = "cancelado"
 
 
class FaseJogo(str, Enum):
    GRUPOS         = "grupos"
    OITAVAS        = "oitavas"
    QUARTAS        = "quartas"
    SEMIFINAL      = "semifinal"
    TERCEIRO_LUGAR = "terceiro_lugar"
    FINAL          = "final"
 
 
class ResultadoFinal(str, Enum):
    TIME_A = "time_a"
    EMPATE = "empate"
    TIME_B = "time_b"
 
 
@dataclass
class Jogo:
    fase: FaseJogo
    data_jogo: date
    horario: time
    time_a: str
    time_b: str
    pontos_time_a: int       # pontos ganhos se acertar vitória do time A
    pontos_empate: int       # pontos ganhos se acertar empate
    pontos_time_b: int       # pontos ganhos se acertar vitória do time B
    id_jogo: int | None = None
    status: StatusJogo = StatusJogo.DISPONIVEL
    resultado_final: ResultadoFinal | None = None
 
 
    @property
    def aberto_para_palpites(self) -> bool:
        return self.status == StatusJogo.DISPONIVEL
 
    def pontos_para(self, escolha: str) -> int:
        """Retorna quantos pontos o usuário ganha se acertar aquela escolha"""
        if escolha == "time_a":
            return self.pontos_time_a
        if escolha == "time_b":
            return self.pontos_time_b
        return self.pontos_empate
 
    def to_dict(self) -> dict:
        return {
            "id_jogo": self.id_jogo,
            "fase": self.fase.value,
            "data_jogo": self.data_jogo.isoformat(),
            "horario": self.horario.strftime("%H:%M"),
            "time_a": self.time_a,
            "time_b": self.time_b,
            "status": self.status.value,
            "resultado_final": self.resultado_final.value if self.resultado_final else None,
            "pontuacao": {
                "time_a": self.pontos_time_a,
                "empate": self.pontos_empate,
                "time_b": self.pontos_time_b,
            },
            "aberto_para_palpites": self.aberto_para_palpites,
        }
 
 
#Erros de validação 
 
class ErroJogo(Exception):
    def __init__(self, mensagem: str, campo: str | None = None):
        super().__init__(mensagem)
        self.mensagem = mensagem
        self.campo = campo
 
    def to_dict(self) -> dict:
        return {"erro": self.mensagem, "campo": self.campo}
 
 
class JogoNaoEncontrado(ErroJogo):
    def __init__(self):
        super().__init__("Partida não encontrada.", campo="id_jogo")
 
 
class JogoJaFinalizado(ErroJogo):
    def __init__(self):
        super().__init__("Esta partida já foi finalizada.", campo="status")
 
 
class JogoBloqueado(ErroJogo):
    def __init__(self):
        super().__init__(
            "Esta partida já começou. Não é possível alterar palpites.", campo="status"
        )
 
 
class DadosJogoInvalidos(ErroJogo):
    pass
