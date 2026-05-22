"""
services/jogo_service.py
Serviço de partidas da Copa, lógica de negócio para criação, consulta e atualização
"""

from datetime import date, datetime

from models.jogo import (
    DadosJogoInvalidos,
    Jogo,
    JogoJaEncerrado,
    JogoNaoEncontrado,
    StatusJogo,
)
from models.repositorio_jogo import RepositorioJogo


class JogoService:
    def __init__(self, repositorio: RepositorioJogo):
        self._repo = repositorio

    #Criação

    def criar_jogo(
        self,
        selecao_a: str,
        selecao_b: str,
        horario: str,
        fase: str,
        estadio: str,
        grupo: str | None = None,
    ) -> dict:
        """
        Cadastra uma nova partida da Copa manualmente.

        horario : string ISO 8601 ex: "2026-06-10T20:00:00"
        fase: ex "Fase de Grupos"
        estadio
        grupo 
        """
        selecao_a, selecao_b, fase, estadio = self._sanitizar(
            selecao_a, selecao_b, fase, estadio
        )
        self._validar_criacao(selecao_a, selecao_b, horario, fase, estadio)

        jogo = Jogo(
            selecao_a=selecao_a,
            selecao_b=selecao_b,
            horario=datetime.fromisoformat(horario),
            fase=fase,
            estadio=estadio,
            grupo=grupo.strip() if grupo else None,
        )
        return self._repo.salvar(jogo).to_dict()

    #Consultas

    def jogos_do_dia(self, data: date | None = None) -> list[dict]:
        """Retorna partidas de uma data. Se não informada, usa hoje"""
        data = data or date.today()
        return [j.to_dict() for j in self._repo.listar_por_data(data)]

    def buscar_jogo(self, id: int) -> dict:
        jogo = self._repo.buscar_por_id(id)
        if not jogo:
            raise JogoNaoEncontrado()
        return jogo.to_dict()

    def listar_todos(self) -> list[dict]:
        return [j.to_dict() for j in self._repo.listar_todos()]

    def iniciar_jogo(self, id: int) -> dict:
        jogo = self._repo.buscar_por_id(id)
        if not jogo:
            raise JogoNaoEncontrado()
        if jogo.status == StatusJogo.ENCERRADO:
            raise JogoJaEncerrado()

        jogo.status = StatusJogo.EM_ANDAMENTO
        jogo.placar_a = 0
        jogo.placar_b = 0
        return self._repo.atualizar(jogo).to_dict()

    def atualizar_placar_parcial(self, id: int, placar_a: int, placar_b: int) -> dict:
        jogo = self._repo.buscar_por_id(id)
        if not jogo:
            raise JogoNaoEncontrado()
        if jogo.status == StatusJogo.ENCERRADO:
            raise JogoJaEncerrado()

        jogo.placar_a = placar_a
        jogo.placar_b = placar_b
        return self._repo.atualizar(jogo).to_dict()

    #Atualizaçao

    def atualizar_jogo(self, id: int, dados: dict) -> dict:
        """
        Atualiza campos permitidos de uma partida agendada
        Campos editáveis: selecao_a, selecao_b, horario, fase, estadio, grupo
        """
        jogo = self._repo.buscar_por_id(id)
        if not jogo:
            raise JogoNaoEncontrado()
        if jogo.status == StatusJogo.ENCERRADO:
            raise JogoJaEncerrado()

        if "selecao_a" in dados:
            jogo.selecao_a = dados["selecao_a"].strip()
        if "selecao_b" in dados:
            jogo.selecao_b = dados["selecao_b"].strip()
        if "fase" in dados:
            jogo.fase = dados["fase"].strip()
        if "estadio" in dados:
            jogo.estadio = dados["estadio"].strip()
        if "grupo" in dados:
            jogo.grupo = dados["grupo"].strip() if dados["grupo"] else None
        if "horario" in dados:
            try:
                jogo.horario = datetime.fromisoformat(dados["horario"])
            except ValueError:
                raise DadosJogoInvalidos("Formato de horário inválido. Use ISO 8601.", campo="horario")

        return self._repo.atualizar(jogo).to_dict()

    def registrar_resultado(self, id: int, placar_a: int, placar_b: int) -> dict:
        """
        Registra o placar final e encerra a partida
        Será usado pelo módulo de palpites para calcular pontuações
        """
        jogo = self._repo.buscar_por_id(id)
        if not jogo:
            raise JogoNaoEncontrado()
        if jogo.status == StatusJogo.ENCERRADO:
            raise JogoJaEncerrado()

        if placar_a < 0 or placar_b < 0:
            raise DadosJogoInvalidos("Placar não pode ser negativo.", campo="placar")

        jogo.placar_a = placar_a
        jogo.placar_b = placar_b
        jogo.status = StatusJogo.ENCERRADO

        return self._repo.atualizar(jogo).to_dict()

    def cancelar_jogo(self, id: int) -> dict:
        jogo = self._repo.buscar_por_id(id)
        if not jogo:
            raise JogoNaoEncontrado()
        if jogo.status == StatusJogo.ENCERRADO:
            raise JogoJaEncerrado()

        jogo.status = StatusJogo.CANCELADO
        return self._repo.atualizar(jogo).to_dict()

    #Helpers internos
    @staticmethod
    def _sanitizar(selecao_a, selecao_b, fase, estadio):
        return selecao_a.strip(), selecao_b.strip(), fase.strip(), estadio.strip()

    @staticmethod
    def _validar_criacao(selecao_a, selecao_b, horario, fase, estadio):
        if not selecao_a:
            raise DadosJogoInvalidos("Nome da seleção A é obrigatório.", campo="selecao_a")
        if not selecao_b:
            raise DadosJogoInvalidos("Nome da seleção B é obrigatório.", campo="selecao_b")
        if selecao_a.lower() == selecao_b.lower():
            raise DadosJogoInvalidos("As seleções não podem ser iguais.", campo="selecao_b")
        if not fase:
            raise DadosJogoInvalidos("Fase do torneio é obrigatória.", campo="fase")
        if not estadio:
            raise DadosJogoInvalidos("Estádio é obrigatório.", campo="estadio")
        try:
            datetime.fromisoformat(horario)
        except (ValueError, TypeError):
            raise DadosJogoInvalidos(
                "Formato de horário inválido. Use ISO 8601 — ex: 2026-06-10T20:00:00",
                campo="horario",
            )
