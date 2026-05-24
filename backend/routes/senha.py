import hashlib
import os
import secrets
import string

MINIMO_CARACTERES = 5
SIMBOLOS = "!@#$%&*"


def gerar_senha_temporaria(tamanho: int = 10) -> str:
    if tamanho < MINIMO_CARACTERES:
        raise ValueError(f"Tamanho minimo da senha e {MINIMO_CARACTERES} caracteres.")

    alfabeto = string.ascii_letters + string.digits + SIMBOLOS

    while True:
        senha = "".join(secrets.choice(alfabeto) for _ in range(tamanho))
        if (
            any(c.isupper() for c in senha)
            and any(c.islower() for c in senha)
            and any(c.isdigit() for c in senha)
            and any(c in SIMBOLOS for c in senha)
        ):
            return senha


def validar_forca_senha(senha: str) -> tuple[bool, str]:
    if len(senha) < MINIMO_CARACTERES:
        return False, f"A senha deve ter no minimo {MINIMO_CARACTERES} caracteres"
    if not any(c.isalnum() for c in senha):
        return False, "A senha deve ter pelo menos uma letra ou numero"
    if not any(c in SIMBOLOS for c in senha):
        return False, "A senha deve ter pelo menos um caractere especial"
    return True, "Senha valida"


def hash_senha(senha: str) -> str:
    salt = os.urandom(16).hex()
    senha_hash = hashlib.sha256(f"{salt}{senha}".encode()).hexdigest()
    return f"{salt}:{senha_hash}"


def verificar_senha(senha: str, senha_hash: str) -> bool:
    try:
        salt, hash_esperado = senha_hash.split(":", 1)
        hash_calculado = hashlib.sha256(f"{salt}{senha}".encode()).hexdigest()
        return secrets.compare_digest(hash_calculado, hash_esperado)
    except ValueError:
        return False
