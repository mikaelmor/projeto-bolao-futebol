import hashlib
import os
import re
import secret
import string
MINIMO_CARACTERES = 6
def gerar_senha_temporaria(tamanho: int = 10)-> str:
    if tamanho <MINIMO_CARACTERES:
        raise ValueError(f"Tamanho minimo da senha é{MINIMO_CARACTERES}  caracteres.")
    
    simbolos = "!@#$%&*"
    alfabeto = string.ascii_letters + strings.digits +simbolos

    while True: 
        senha = "". join(secrets.choice(alfabeto) for _ in range(tamanho))
        if (
            any(c.isupper() for c in senha)
            and any(c.islower() for c in senha)
            and any(c.isdigit() for c in senha)
            and any(c in simbolos for c in senha)
            ):
            return senha
def validar_forca_senha(senha:str)-> tuple[bool, str]:
    if len(senha) <MINIMO_CARACTERES:
        return False, f"A senha deve ter no mínimo {MINIMO_CARACTERES} caracteres"
    return True, "Senha valida"

def hash_senha(senha: str) -> str:
    salt = os.urandom(16).hex()
    hash = hashlib.sha256(f"{salt}{senha}".encode()).hexdigest()
    return f"{salt}{hash}"     

def verificar_senha(senha: str, senha_hash: str) -> bool:
    try:
        salt, hash_esperado = senha_hash.split(":", 1)
        hash_calculado = hashlib.sha256(f"{salt}{senha}".encode()).hexdigest()
        return secrets.compare_digest(hash_calculado, hash_esperado)  
    except ValueError:
        return False