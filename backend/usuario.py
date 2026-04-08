import re
from dataclasses import dataclass, field
from datetime import datetime

def _validar_cpf(cpf:str) -> bool:
    cpf = re.sub(r"\D", "", cpf)

    if len(cpf) != 11 or cpf == cpf [0] * 11:
        return False
    
    def calcular_digito(cpf_parcial: str, peso_inicial: int) -> int:
        soma = sum(int(d) * p for d, p in zip(cpf_parcial, range(peso_inicial, 1, -1)))
        resto = soma % 11
        return 0 if resto < 2 else 11 - resto
    
    d1 = calcular_digito(cpf[:9], 10)
    d2 = calcular_digito(cpf[:10], 11)

    return cpf[-2:] == f"{d1}{d2}"

@dataclass
class Usuario:
    nome: str
    email: str
    cpf: str
    senha_hash: str
    id: int | None = None
    criado_em: datetime = field(default_factory=datetime.utcnow)
    ativo: bool=True

    def to_dict(self, incluir_senha: bool = False) -> dict:
        dados = {
            "id": self.id, 
            "nome": self.nome,
            "email": self.email,
            "cpf_mascarado": self._mascarar_cpf(),
            "ativo": self.ativo,
            "criado_em": self.criado_em.isoformat()
        }
        if incluir_senha:
            dados["senha_hash"] = self.senha_hash
        return dados
    
    def _mascarar_cpf(self) -> str:
        cpf = re.sub(r"\D", "", self.cpf)
        return f"***.{cpf[3:6]}.{cpf[6.9]}-**"
    

class ErroCadastro(Exception):
    def __init__(self, mensagem: str, campo: str | None = None):
        super(). __init__(mensagem)
        self.mensagem = mensagem
        self.campo = campo

    def to_dict(self) -> dict:
        return {"erro": self.mensagem, "campo": self.campo}
    
class CPFInvalido(ErroCadastro):
    def __init__(self):
        super().__init__("CPF invalido.", campo="cpf")

class EmailInvalido(ErroCadastro):
    def __init__(self):
        super().__init__("Email inválido.", campo="email")

class SenhaFraca(ErroCadastro):
    def __init__(self):
        super().__init__("A senha deve ter pelo menos 6 caracteres", campo="senha")

class UsuarioJaExiste(ErroCadastro):
    def __init__(self, campo:str):
        super().__init__(f"Ja existe um cadastro com este {campo}", campo=campo)