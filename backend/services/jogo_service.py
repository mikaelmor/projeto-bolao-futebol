"""
services/jogo_service.py
Serviço de partidas da Copa, alinhado ao mysql
"""

from datetime import date, datetime, time

from models.jogo import (
    DadosJogoInvalidos,
    FaseJogo,
    Jogo,
    JogoBloqueado,
    JogoJaFinalizado,
    JogoNaoEncontrado,
    ResultadoFinal,
    StatusJogo,
)
from models.repositorio_jogo import RepositorioJogo

FASES_VALIDAS = {f.value for f in FaseJogo}
RESULTADOS_VALIDOS = {r.value for r in ResultadoFinal}

class JogoService:
    def __init__(self, repositorio: RepositorioJogo):
        self._repo = repositorio

    #Criação

    def criar_jogo(
        self,
        fase: str,
        data_jogo: str,
        horario: str,
        time_a: str,
        time_b: str,
        pontos_time_a: int,
        pontos_empate: int,
        pontos_time_b: int,
    ) -> dict:
        """
        Cadastra uma nova partida da Copa manualmente. Fases ('quartas', 'semifinal') // data_jogo ('YYYY-MM-dd) // horário ('HH:MM")
 
        """
        time_a, time_b = time_a.strip(), time_b.strip()
        self._validar_criacao(fase, data_jogo, horario, time_a, time_b, pontos_time_a, pontos_empate, pontos_time_b)

        jogo = Jogo(
            fase=FaseJogo(fase),
            data_jogo=date.fromisoformat(data_jogo),
            horario=self._parse_horario(horario),
            time_a=time_a,
            time_b=time_b,
            pontos_time_a=int(pontos_time_a),
            pontos_empate=int(pontos_empate),
            pontos_time_b=int(pontos_time_b),
        )
        return self._repo.salvar(jogo).to_dict()

    #Consultas

    def jogos_do_dia(self, data: date | None = None) -> list[dict]:
        """Retorna partidas de uma data. Se não informada, usa hoje"""
        data = data or date.today()
        return [j.to_dict() for j in self._repo.listar_por_data(data)]

    def buscar_jogo(self, id_jogo: int) -> dict:
        jogo = self._repo.buscar_por_id(id_jogo)
        if not jogo:
            raise JogoNaoEncontrado()
        return jogo.to_dict()

    def listar_todos(self) -> list[dict]:
        return [j.to_dict() for j in self._repo.listar_todos()]


    #Atualização
    def atualizar_jogo(self, id_jogo: int, dados: dict) -> dict:
        """
        Atualiza campos permitidos de uma partida agendada
        """
        jogo = self._repo.buscar_por_id(id_jogo)
        if not jogo:
            raise JogoNaoEncontrado()
        if jogo.status == StatusJogo.EM_ANDAMENTO:
            raise JogoBloqueado()
        if jogo.status == StatusJogo.FINALIZADO:
            raise JogoJaFinalizado()

        if "time_a" in dados:
            jogo.time_a = dados["time_a"].strip()
        if "time_b" in dados:
            jogo.time_b = dados["time_b"].strip()
        if "fase" in dados:
            if dados["fase"] not in FASES_VALIDAS:
                raise DadosJogoInvalidos(f"Fase inválida. Use: {','.join(FASES_VALIDAS)}", campo="fase")
            jogo.fase = FaseJogo(dados["fase"])
        if "data_jogo" in dados:
            try:
                jogo.data_jogo = date.fromisoformat(dados["data_jogo"])
            except ValueError:
                raise DadosJogoInvalidos("Formato de data inválido. Use YYYY-MM-DD", campo="data_jogo")
        if "horario" in dados:
            jogo.horario = self._parse_horario(dados["horario"])
        if "pontos_time_a" in dados:
            jogo.pontos_time_a = int(dados["pontos_time_a"])
        if "pontos_empate" in dados:
            jogo.pontos_empate = int(dados["pontos_empate"])
        if "pontos_time_b" in dados:
            jogo.pontos_time_b = int(dados["pontos_time_b"])

        return self._repo.atualizar(jogo).to_dict()

    def iniciar_jogo(self, id_jogo: int) -> dict:
        # muda status para em andamento e bloqueia palpites
        jogo = self._repo.buscar_por_id(id_jogo)
        if not jogo:
            raise JogoNaoEncontrado()
        if jogo.status == StatusJogo.FINALIZADO:
            raise JogoJaFinalizado()
        if jogo.status == StatusJogo.CANCELADO:
            raise JogoBloqueado()
        if jogo.status != StatusJogo.EM_ANDAMENTO:
            jogo.status = StatusJogo.EM_ANDAMENTO
        return self._repo.atualizar(jogo).to_dict()

    def registrar_resultado(self, id_jogo: int, resultado: str) -> dict:
        if resultado not in RESULTADOS_VALIDOS:
            raise DadosJogoInvalidos(
                f"Resultado inválido. Use: {','.join(RESULTADOS_VALIDOS)}", campo="resultado"
            )

        jogo = self._repo.buscar_por_id(id_jogo)
        if not jogo:
            raise JogoNaoEncontrado()
        if jogo.status == StatusJogo.FINALIZADO:
            raise JogoJaFinalizado()

        jogo.resultado_final = ResultadoFinal(resultado)
        jogo.status = StatusJogo.FINALIZADO
        return self._repo.atualizar(jogo).to_dict()
       
    def cancelar_jogo(self, id_jogo: int) -> dict:
        jogo = self._repo.buscar_por_id(id_jogo)
        if not jogo:
            raise JogoNaoEncontrado()
        if jogo.status == StatusJogo.CANCELADO:
            raise JogoJaFinalizado()
        jogo.status = StatusJogo.CANCELADO
        return self._repo.atualizar(jogo).to_dict()

    @staticmethod
    def _parse_horario(horario_str: str) -> time:
        for fmt in ("%H:%M:%S", "%H:%M"):
            try:
                return datetime.strptime(horario_str, fmt).time()
            except ValueError:
                continue
        raise DadosJogoInvalidos(
            "Formato de horário inválido. Use HH:MM ou HH:MM:SS", campo="horario"
        )

    @staticmethod
    def _validar_criacao(fase, data_jogo, horario, time_a, time_b, pts_a, pts_emp, pts_b):
        if fase not in FASES_VALIDAS: 
            raise DadosJogoInvalidos(F"Fase inválida. Use: {','.join(FASES_VALIDAS)}", campo="fase")
        
        if not time_a: 
            raise DadosJogoInvalidos("Nome do time a é obrigatório.", campo="time_a")
        
        if not time_b: 
            raise DadosJogoInvalidos("Nome do time b é obrigatório", campo="time_b")
        
        if time_a.lower() == time_b.lower():
            raise DadosJogoInvalidos("Os times não podem ser iguais", campo="time_b")
        try:
            date.fromisoformat(data_jogo)
        except (ValueError, TypeError):
            raise DadosJogoInvalidos("Formato de data inválido, use YYYY-MM-DD", campo="data_jogo")
        for val, campo in [(pts_a, "pontos_time_a"), (pts_emp, "pontos_empate"), (pts_b, "pontos_time_b")]:
            if int(val) < 0:
                raise DadosJogoInvalidos("Pontuação não pode ser negativa", campo=campo)