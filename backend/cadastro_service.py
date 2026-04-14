import re
from models.usuario import(
    CPFInvalido,
    EmailInvalido,
    SenhaFraca,
    Usuario,
    UsuarioJaExiste,
    _validar_cpf,   
)

from models.repositorio import RepositorioUsuario
from utils.senha import gerar_senha_temporaria, hash_senha, validar_forca_senha

_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

class CadastroService:
    def __init__(self, repositorio: RepositorioUsuario):
        self._repo = repositorio

    def cadastrar(self, nome: str, sobrenome: str, email: str, cpf: str, senha: str) -> dict:
        nome, email, cpf = self._sanitizar(nome, email, cpf)   
        self._validar_campos(nome, email, cpf, senha)
        self._verificar_duplicidade(email, cpf)

        usuario = Usuario(
            nome=nome,
            sobrenome=sobrenome,
            email=email, 
            cpf=cpf,
            senha_hash=hash_senha(senha),
        )
        usuario = self._repo.salvar(usuario)
        return usuario.to_dict()
    
    def cadastrar_com_senha_gerada(self, nome: str, email: str, cpf: str) -> dict:
        nome, email, cpf = self._sanitizar(nome, email, cpf)
        self._validar_campos(nome, email, cpf, senha=None)
        self._verificar_duplicidade(email, cpf)
        senha_temporaria = gerar_senha_temporaria(tamanho=10)
        usuario = Usuario(
            nome=nome,
            email=email,
            cpf=cpf,
            senha_hash=hash_senha(senha_temporaria),
        )
        usuario = self._repo.salvar(usuario)
        resultado = usuario.to_dict()
        resultado["senha_temporaria"] = senha_temporaria
        return resultado
    
    @staticmethod
    def _sanitizar(nome: str, email: str, cpf: str) -> tuple[str, str, str]:
        nome = nome.strip()
        email = email.strip().lower()
        cpf = re.sub(r"\D", "", cpf.strip)
        return nome, email, cpf
    
    def _validar_campos(self, nome: str, email: str, cpf:str, senha: str | None):
        if not nome or len(nome)<2:
            from models.usuario import ErroCadastro
            raise ErroCadastro("Nome deve ter pelo menos 2 caracteres.", campo="nome")
        
        if not _EMAIL_RE.match(email):
            raise EmailInvalido()
        
        if not _validar_cpf(cpf):
            raise CPFInvalido()
        
        if senha is not None:
            valido, msg = validar_forca_senha(senha)
            if not valido:
                raise SenhaFraca()
            
    def _verificar_duplicidade(self, email: str, cpf: str):

        if self._repo.buscar_por_email(email):
            raise UsuarioJaExiste("email")

        if self._repo.buscar_por_cpf(cpf):
            raise UsuarioJaExiste("CPF")       