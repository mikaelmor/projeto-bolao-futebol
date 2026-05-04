"""
models/repositorio_jogo.py
Interface abstrata do repositório de jogos + implementação em memória
"""

from abc import ABC, abstractmethod
from datetime import date
from .jogo import Jogo, StatusJogo


class RepositorioJogo(ABC):
    """
    Contrato de persistência para Jogo
    Implementar essa classe p/ cada banco de dados
    """

    @abstractmethod
    def salvar(self, jogo: Jogo) -> Jogo:
        """Persiste um novo jogo e retorna com ID gerado"""
        ...

    @abstractmethod
    def atualizar(self, jogo: Jogo) -> Jogo:
        """Atualiza um jogo existente"""
        ...

    @abstractmethod
    def buscar_por_id(self, id: int) -> Jogo | None:
        ...

    @abstractmethod
    def listar_por_data(self, data: date) -> list[Jogo]:
        """Retorna todos os jogos de uma data específica, ordenados por horário"""
        ...

    @abstractmethod
    def listar_todos(self) -> list[Jogo]:
        ...


#Implementação em memória

class RepositorioJogoEmMemoria(RepositorioJogo):
    """Repositório temporário em memória — usar até o banco estar pronto."""

    def __init__(self):
        self._jogos: dict[int, Jogo] = {}
        self._proximo_id = 1

    def salvar(self, jogo: Jogo) -> Jogo:
        jogo.id = self._proximo_id
        self._proximo_id += 1
        self._jogos[jogo.id] = jogo
        return jogo

    def atualizar(self, jogo: Jogo) -> Jogo:
        self._jogos[jogo.id] = jogo
        return jogo

    def buscar_por_id(self, id: int) -> Jogo | None:
        return self._jogos.get(id)

    def listar_por_data(self, data: date) -> list[Jogo]:
        jogos_do_dia = [
            j for j in self._jogos.values()
            if j.horario.date() == data
        ]
        return sorted(jogos_do_dia, key=lambda j: j.horario)

    def listar_todos(self) -> list[Jogo]:
        return sorted(self._jogos.values(), key=lambda j: j.horario)