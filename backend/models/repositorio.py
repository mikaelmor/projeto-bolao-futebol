from abc import ABC, abstractmethod
from .usuario import Usuario

class RepositorioUsuario(ABC):
    #persiste um novo usuario e retorna com id gerado
    @abstractmethod
    def salvar(self, usuario: Usuario) -> Usuario:
        ...

    #retorna o usuario pelo email ou none se ñ encontrado
    @abstractmethod    
    def buscar_por_email(self, email: str) -> Usuario | None: 
        ...

    # retorna o usuario pelo cpf (apenas digitos) ou none 
    @abstractmethod
    def buscar_por_cpf(self, cpf: str) -> Usuario| None:
        ...

    # retorna usuário pelo id ou none
    @abstractmethod
    def buscar_por_id(self, id: int) -> Usuario | None:
        ...

    @abstractmethod
    def atualizar(self, usuario: Usuario) -> Usuario:
        ...

    @abstractmethod
    def listar_todos(self) -> list[Usuario]:
        ...


class RepositorioEmMemoria(RepositorioUsuario):
    def __init__(self):
        self._usuarios: dict[int, Usuario] = {}
        self._proximo_id = 1

    def salvar(self, usuario: Usuario) -> Usuario:
        usuario.id = self._proximo_id
        self._proximo_id += 1
        self._usuarios[usuario.id] = usuario
        return usuario
    
    def buscar_por_email(self, email: str) -> Usuario | None:
        email = email.lower().strip()
        return next((u for u in self._usuarios.values() if u.email == email), None)
    
    def buscar_por_cpf(self, cpf: str) -> Usuario | None:
        import re
        cpf_limpo = re.sub(r"\D", "", cpf)
        return next(
            (u for u in self._usuarios.values() if re.sub(r"\D", "", u.cpf) == cpf_limpo),
            None,
        )
    
    def buscar_por_id(self, id: int) -> Usuario|None:
        return self._usuarios.get(id)

    def atualizar(self, usuario: Usuario) -> Usuario:
        self._usuarios[usuario.id] = usuario
        return usuario

    def listar_todos(self) -> list[Usuario]:
        return list(self._usuarios.values())
