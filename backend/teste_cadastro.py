import sys
import os 
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import pytest
from models.repositorio import RepositorioEmMemoria
from models.usuario import Usuario, CPFInvalido, EmailInvalido, ErroCadastro, SenhaFraca, UsuarioJaExiste
from services.cadastro_service import CadastroService
from utils.senha import hash_senha, gerar_senha_temporaria, verificar_senha
@pytest.fixture
def cadastro_service():
    return CadastroService(RepositorioEmMemoria())

DADOS_VALIDOS = {
    "nome": "Maria Silva",
    "email":"maria.silva@example.com",
    "cpf": "123.456.789-09",
    "senha": "senha@123",
}

class TestCadastroService:
    def teste_cadastro_valido(self, service):
        usuario = service.cadastrar(**DADOS_VALIDOS)
        assert usuario["id"] == 1
        assert usuario["nome"] == "Maria Silva"
        assert "cpf_mascarado" in usuario
        assert "senha_hash" not in usuario

    def teste_email_normalizado(self, service):
        dados = {**DADOS_VALIDOS, "email": "MARIA.SILVA@EXAMPLE.COM"}
        usuario = service.cadastrar(**dados)
        assert usuario["email"] == "maria.silva@example.com"

    def teste_cpf_somente_numeros(self, service):
        usuario = service.cadastrar(**DADOS_VALIDOS)
        assert "***" in usuario["cpf_mascarado"]

    def teste_email_invalido(self, service):
        with pytest.raises(EmailInvalido):
            service.cadastrar(**{**DADOS_VALIDOS, "email": "email_invalido"})

    def teste_cpf_invalido(self, service):
        with pytest.raises(CPFInvalido):
            service.cadastrar(**{**DADOS_VALIDOS, "cpf": "111.111.111-11"})

    def teste_senha_fraca(self, service):
        with pytest.raises(SenhaFraca):
            service.cadastrar(**{**DADOS_VALIDOS, "senha": "123"})

    def teste_senha_minimo_caracteres(self, service):
        usuario = service.cadastrar(**{**DADOS_VALIDOS, "senha": "Abc@123"})
        assert usuario["id"] is not None 

    def teste_email_duplicado(self, service):
        service.cadastrar(**DADOS_VALIDOS)
        with pytest.raises(UsuarioJaExiste) as exc:
            service.cadastrar(**{**DADOS_VALIDOS, "cpf": "123.456.789-00"})
        assert exc.value.campo == "email"

    def teste_cpf_duplicado(self, service):
        service.cadastrar(**DADOS_VALIDOS)
        with pytest.raises(UsuarioJaExiste) as exc:
            service.cadastrar(**{**DADOS_VALIDOS, "email": "outro@example.com"})
        assert exc.value.campo == "cpf"

class TestCadastroComSenhaGerada: 
    def teste_cadastro_com_senha_gerada(self, service):
        resulatdo = service.cadastrar_com_senha_gerada(
            nome=DADOS_VALIDOS["nome"],
            sobrenome=DADOS_VALIDOS["sobrenome"],
            email=DADOS_VALIDOS["email"],
            cpf=DADOS_VALIDOS["cpf"],
        )
        assert "senha_temporaria" in resultado 
        assert len(resultado["senha_temporaria"]) >= 6

    def teste_senha_gerada_valida(self, service):
        from models.repositorio import RepositorioEmMemoria
        repo = RepositorioEmMemoria()
        svc = CadastroService(repo)
        resultado = svc.cadastrar_com_senha_gerada(
            nome=DADOS_VALIDOS["nome"],
            email=DADOS_VALIDOS["email"],
            cpf=DADOS_VALIDOS["cpf"],
        )    
        usuario_salvo = repo.buscar_por_email(DADOS_VALIDOS["email"])
        assert verificar_senha(resultado["sennha_temporaria"], usuario_salvo.senha_hash)

class TesteSenha:
    def teste_hash_e_verificacao(self):
        senha = "MinhaSenha@123"
        senha_hash = hash_senha(senha)
        assert verificar_senha(senha, senha_hash)
        assert not verificar_senha("SenhaErrada", senha_hash)  

    def teste_hashes_diferentes_para_senhas_iguais(self):
        senha = "SenhaUnica@123"
        hash1 = hash_senha(senha)
        hash2 = hash_senha(senha)
        assert hash1 != hash2

    def gerar_senha_temporaria(self):
        senha1 = gerar_senha_temporaria()
        senha2 = gerar_senha_temporaria()
        assert len(senha1) >= 6
        assert len(senha2) >= 6
        assert senha1 != senha2              