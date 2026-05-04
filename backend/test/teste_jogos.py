"""
tests/test_jogos.py
Testes do módulo de jogos
Execute com pytest tests/test_jogos.py -v
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
from datetime import date, datetime, timedelta

from models.jogo import DadosJogoInvalidos, JogoJaEncerrado, JogoNaoEncontrado, StatusJogo
from models.repositorio_jogo import RepositorioJogoEmMemoria
from services.jogo_service import JogoService

HORARIO_HOJE = datetime.now().replace(hour=20, minute=0, second=0, microsecond=0).isoformat()
HORARIO_AMANHA = (datetime.now() + timedelta(days=1)).replace(hour=16, minute=0, second=0, microsecond=0).isoformat()

JOGO_BASE = {
    "time_casa": "Flamengo",
    "time_visitante": "Vasco",
    "horario": HORARIO_HOJE,
    "campeonato": "Brasileirão Série A",
}

@pytest.fixture
def service():
    return JogoService(RepositorioJogoEmMemoria())


class TestCriarJogo:
    def test_criar_valido(self, service):
        j = service.criar_jogo(**JOGO_BASE)
        assert j["id"] == 1
        assert j["time_casa"] == "Flamengo"
        assert j["status"] == "agendado"
        assert j["placar"] is None

    def test_times_iguais(self, service):
        with pytest.raises(DadosJogoInvalidos) as exc:
            service.criar_jogo(**{**JOGO_BASE, "time_visitante": "Flamengo"})
        assert exc.value.campo == "time_visitante"

    def test_horario_invalido(self, service):
        with pytest.raises(DadosJogoInvalidos) as exc:
            service.criar_jogo(**{**JOGO_BASE, "horario": "nao-e-data"})
        assert exc.value.campo == "horario"

    def test_campo_obrigatorio_vazio(self, service):
        with pytest.raises(DadosJogoInvalidos):
            service.criar_jogo(**{**JOGO_BASE, "campeonato": ""})


class TestConsultarJogos:
    def test_jogos_do_dia(self, service):
        service.criar_jogo(**JOGO_BASE)
        service.criar_jogo(**{**JOGO_BASE, "time_casa": "Botafogo", "horario": HORARIO_AMANHA})
        jogos = service.jogos_do_dia(date.today())
        assert len(jogos) == 1
        assert jogos[0]["time_casa"] == "Flamengo"

    def test_jogo_nao_encontrado(self, service):
        with pytest.raises(JogoNaoEncontrado):
            service.buscar_jogo(999)

    def test_listar_todos(self, service):
        service.criar_jogo(**JOGO_BASE)
        service.criar_jogo(**{**JOGO_BASE, "time_casa": "São Paulo", "horario": HORARIO_AMANHA})
        assert len(service.listar_todos()) == 2


class TestResultado:
    def test_registrar_resultado(self, service):
        j = service.criar_jogo(**JOGO_BASE)
        resultado = service.registrar_resultado(j["id"], placar_casa=2, placar_visitante=1)
        assert resultado["status"] == "encerrado"
        assert resultado["vencedor"] == "Flamengo"
        assert resultado["placar"]["display"] == "Flamengo 2 x 1 Vasco"

    def test_empate(self, service):
        j = service.criar_jogo(**JOGO_BASE)
        resultado = service.registrar_resultado(j["id"], placar_casa=0, placar_visitante=0)
        assert resultado["vencedor"] == "empate"

    def test_nao_pode_alterar_encerrado(self, service):
        j = service.criar_jogo(**JOGO_BASE)
        service.registrar_resultado(j["id"], 1, 0)
        with pytest.raises(JogoJaEncerrado):
            service.registrar_resultado(j["id"], 2, 0)

    def test_placar_negativo(self, service):
        j = service.criar_jogo(**JOGO_BASE)
        with pytest.raises(DadosJogoInvalidos):
            service.registrar_resultado(j["id"], -1, 0)


class TestAtualizar:
    def test_atualizar_campeonato(self, service):
        j = service.criar_jogo(**JOGO_BASE)
        atualizado = service.atualizar_jogo(j["id"], {"campeonato": "Copa do Brasil"})
        assert atualizado["campeonato"] == "Copa do Brasil"

    def test_nao_atualiza_encerrado(self, service):
        j = service.criar_jogo(**JOGO_BASE)
        service.registrar_resultado(j["id"], 1, 0)
        with pytest.raises(JogoJaEncerrado):
            service.atualizar_jogo(j["id"], {"campeonato": "Copa do Brasil"})