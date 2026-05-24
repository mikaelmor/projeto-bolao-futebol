"""
models/repositorio_palpite.py
Interface abstrata + implementação em memória do repositório de palpites
"""

from abc import ABC, abstractmethod
from .palpite import Palpite


class RepositorioPalpite(ABC):

    @abstractmethod
    def salvar(self, palpite: Palpite) -> Palpite: ...

    @abstractmethod
    def atualizar(self, palpite: Palpite) -> Palpite: ...

    @abstractmethod
    def buscar_por_id(self, id_palpite: int) -> Palpite | None: ...

    @abstractmethod
    def buscar_por_usuario_e_jogo(self, id_usuario: int, id_jogo: int) -> Palpite | None: ...

    @abstractmethod
    def excluir_por_usuario_e_jogo(self, id_usuario: int, id_jogo: int) -> Palpite | None: ...

    @abstractmethod
    def listar_por_usuario(self, id_usuario: int) -> list[Palpite]: ...

    @abstractmethod
    def listar_por_jogo(self, id_jogo: int) -> list[Palpite]: ...

    @abstractmethod
    def listar_todos(self) -> list[Palpite]:
        """Retorna todos os palpites — usado pelo ranking geral."""
        ...


# Implementação em memória

class RepositorioPalpiteEmMemoria(RepositorioPalpite):

    def __init__(self):
        self._palpites: dict[int, Palpite] = {}
        self._proximo_id = 1

    def salvar(self, palpite: Palpite) -> Palpite:
        palpite.id_palpite = self._proximo_id
        self._proximo_id += 1
        self._palpites[palpite.id_palpite] = palpite
        return palpite

    def atualizar(self, palpite: Palpite) -> Palpite:
        self._palpites[palpite.id_palpite] = palpite
        return palpite

    def buscar_por_id(self, id_palpite: int) -> Palpite | None:
        return self._palpites.get(id_palpite)

    def buscar_por_usuario_e_jogo(self, id_usuario: int, id_jogo: int) -> Palpite | None:
        return next(
            (p for p in self._palpites.values()
             if p.id_usuario == id_usuario and p.id_jogo == id_jogo),
            None,
        )

    def excluir_por_usuario_e_jogo(self, id_usuario: int, id_jogo: int) -> Palpite | None:
        palpite = self.buscar_por_usuario_e_jogo(id_usuario, id_jogo)
        if palpite:
            self._palpites.pop(palpite.id_palpite, None)
        return palpite

    def listar_por_usuario(self, id_usuario: int) -> list[Palpite]:
        return sorted(
            [p for p in self._palpites.values() if p.id_usuario == id_usuario],
            key=lambda p: p.data_palpite,
            reverse=True,
        )

    def listar_por_jogo(self, id_jogo: int) -> list[Palpite]:
        return [p for p in self._palpites.values() if p.id_jogo == id_jogo]

    def listar_todos(self) -> list[Palpite]:
        return list(self._palpites.values())
