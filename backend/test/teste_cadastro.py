import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
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

class TestCadastrar:
    def test_cadastro_valido(self, service):
        usuario = service.cadastrar(**DADOS_VALIDOS)
        assert usuario["id"] == 1
        assert usuario["nome"] == "Maria Silva"
        assert "cpf_mascarado" in usuario
        assert "senha_hash" not in usuario  # nunca expor o hash

    def test_email_normalizado(self, service):
        dados = {**DADOS_VALIDOS, "email": "  MARIA@EXAMPLE.COM  "}
        usuario = service.cadastrar(**dados)
        assert usuario["email"] == "maria@example.com"

    def test_cpf_com_formatacao(self, service):
        """CPF com pontos e traço deve ser aceito."""
        usuario = service.cadastrar(**DADOS_VALIDOS)
        assert "***" in usuario["cpf_mascarado"]

    def test_email_invalido(self, service):
        with pytest.raises(EmailInvalido):
            service.cadastrar(**{**DADOS_VALIDOS, "email": "nao-e-email"})

    def test_cpf_invalido(self, service):
        with pytest.raises(CPFInvalido):
            service.cadastrar(**{**DADOS_VALIDOS, "cpf": "111.111.111-11"})

    def test_senha_muito_curta(self, service):
        with pytest.raises(SenhaFraca):
            service.cadastrar(**{**DADOS_VALIDOS, "senha": "abc"})

    def test_senha_minimo_6_caracteres(self, service):
        usuario = service.cadastrar(**{**DADOS_VALIDOS, "senha": "Ab1@xy"})
        assert usuario["id"] is not None

    def test_email_duplicado(self, service):
        service.cadastrar(**DADOS_VALIDOS)
        with pytest.raises(UsuarioJaExiste) as exc:
            service.cadastrar(**{**DADOS_VALIDOS, "cpf": "275.477.738-13"})
        assert exc.value.campo == "e-mail"

    def test_cpf_duplicado(self, service):
        service.cadastrar(**DADOS_VALIDOS)
        with pytest.raises(UsuarioJaExiste) as exc:
            service.cadastrar(**{**DADOS_VALIDOS, "email": "outro@example.com"})
        assert exc.value.campo == "CPF"

    def test_nome_muito_curto(self, service):
        with pytest.raises(ErroCadastro) as exc:
            service.cadastrar(**{**DADOS_VALIDOS, "nome": "A"})
        assert exc.value.campo == "nome"

#Cadastro com senha gerada 
class TestCadastrarComSenhaGerada:
    def test_retorna_senha_temporaria(self, service):
        resultado = service.cadastrar_com_senha_gerada(
            nome=DADOS_VALIDOS["nome"],
            email=DADOS_VALIDOS["email"],
            cpf=DADOS_VALIDOS["cpf"],
        )
        assert "senha_temporaria" in resultado
        assert len(resultado["senha_temporaria"]) >= 6

    def test_senha_gerada_e_valida(self, service):
        from models.repositorio import RepositorioEmMemoria
        repo = RepositorioEmMemoria()
        svc = CadastroService(repo)
        resultado = svc.cadastrar_com_senha_gerada(
            nome=DADOS_VALIDOS["nome"],
            email=DADOS_VALIDOS["email"],
            cpf=DADOS_VALIDOS["cpf"],
        )
        usuario_salvo = repo.buscar_por_email(DADOS_VALIDOS["email"])
        assert verificar_senha(resultado["senha_temporaria"], usuario_salvo.senha_hash)

#Utilitários de senha
class TestSenha:
    def test_hash_e_verificacao(self):
        senha = "MinhaSenh@123"
        h = hash_senha(senha)
        assert verificar_senha(senha, h)
        assert not verificar_senha("senhaErrada", h)

    def test_hashes_diferentes_para_mesma_senha(self):
        senha = "igual@123"
        assert hash_senha(senha) != hash_senha(senha)

    def test_gerar_senha_tamanho_minimo(self):
        senha = gerar_senha_temporaria(6)
        assert len(senha) == 6

    def test_gerar_senha_padrao(self):
        senha = gerar_senha_temporaria()
        assert len(senha) == 10

    def test_gerar_senha_tamanho_invalido(self):
        with pytest.raises(ValueError):
            gerar_senha_temporaria(3)            