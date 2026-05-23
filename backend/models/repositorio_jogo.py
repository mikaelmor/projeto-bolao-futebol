"""
models/repositorio_jogo.py
Interface abstrata do repositório de jogos + implementação em memória
"""

from abc import ABC, abstractmethod
from datetime import date
from .jogo import Jogo, StatusJogo


class RepositorioJogo(ABC):

    @abstractmethod
    def salvar(self, jogo: Jogo) -> Jogo:
        ...

    @abstractmethod
    def atualizar(self, jogo: Jogo) -> Jogo:
        ...

    @abstractmethod
    def buscar_por_id(self, id: int) -> Jogo | None:
        ...

    @abstractmethod
    def listar_por_data(self, data: date) -> list[Jogo]:
        ...

    @abstractmethod
    def listar_todos(self) -> list[Jogo]:
        ...


class RepositorioJogoEmMemoria(RepositorioJogo):
    
    def __init__(self):
        self._jogos: dict[int, Jogo] = {}
        self._proximo_id = 1

    def salvar(self, jogo: Jogo) -> Jogo:
        jogo.id_jogo = self._proximo_id
        self._proximo_id += 1
        self._jogos[jogo.id_jogo] = jogo
        return jogo

    def atualizar(self, jogo: Jogo) -> Jogo:
        self._jogos[jogo.id_jogo] = jogo
        return jogo

    def buscar_por_id(self, id_jogo: int) -> Jogo | None:
        return self._jogos.get(id_jogo)

    def listar_por_data(self, data: date) -> list[Jogo]:
        return sorted(
            [j for j in self._jogos.values() if j.data_jogo ==data],
            key=lambda j: j.horario,
        )

    def listar_todos(self) -> list[Jogo]:
        return sorted(self._jogos.values(), key=lambda j: j.horario)