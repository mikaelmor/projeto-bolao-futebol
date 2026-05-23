#tests/test_jogos.py
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
from datetime import date
from models.jogo import DadosJogoInvalidos, JogoJaFinalizado, JogoNaoEncontrado, JogoBloqueado
from models.repositorio_jogo import RepositorioJogoEmMemoria
from services.jogo_service import JogoService

JOGO_BASE = {
    "fase":          "grupos",
    "data_jogo":     "2026-06-10",
    "horario":       "14:00",
    "time_a":        "Brasil",
    "time_b":        "Argentina",
    "pontos_time_a": 10,
    "pontos_empate": 3,
    "pontos_time_b": 10,
}

JOGO_AMANHA = {**JOGO_BASE, "data_jogo": "2026-06-11", "time_a": "França", "time_b": "Espanha"}

@pytest.fixture
def service():
    return JogoService(RepositorioJogoEmMemoria())

#Criação de partidas
class TestCriarJogo:
    def test_criar_valido(self, service):
        j = service.criar_jogo(**JOGO_BASE)
        assert j["id_jogo"] == 1
        assert j["time_a"] == "Brasil"
        assert j["time_b"] == "Argentina"
        assert j["status"] == "disponivel"
        assert j["resultado_final"] is None

    def test_pontuacao_salva_corretamente(self, service):
        j = service.criar_jogo(**JOGO_BASE)
        assert j["pontuacao"]["time_a"] == 10
        assert j["pontuacao"]["empate"] == 3
        assert j["pontuacao"]["time_b"] == 10

    def test_pontuacao_favorito_vs_azarao(self, service):
        j = service.criar_jogo(
            fase="grupos", data_jogo="2026-06-10", horario="16:00",
            time_a="Catar", time_b="Espanha",
            pontos_time_a=15, pontos_empate=3, pontos_time_b=5,
        )
        assert j["pontuacao"]["time_a"] == 15
        assert j["pontuacao"]["time_b"] == 5

    def test_selecoes_iguais_rejeitadas(self, service):
        with pytest.raises(DadosJogoInvalidos) as exc:
            service.criar_jogo(**{**JOGO_BASE, "time_b": "Brasil"})
        assert exc.value.campo == "time_b"

    def test_horario_invalido(self, service):
        with pytest.raises(DadosJogoInvalidos) as exc:
            service.criar_jogo(**{**JOGO_BASE, "horario": "nao-e-hora"})
        assert exc.value.campo == "horario"

    def test_data_invalida(self, service):
        with pytest.raises(DadosJogoInvalidos) as exc:
            service.criar_jogo(**{**JOGO_BASE, "data_jogo": "10-06-2026"})
        assert exc.value.campo == "data_jogo"

    def test_fase_invalida(self, service):
        with pytest.raises(DadosJogoInvalidos) as exc:
            service.criar_jogo(**{**JOGO_BASE, "fase": "brasileirao"})
        assert exc.value.campo == "fase"

    def test_pontuacao_negativa_rejeitada(self, service):
        with pytest.raises(DadosJogoInvalidos):
            service.criar_jogo(**{**JOGO_BASE, "pontos_time_a": -1})

    def test_time_vazio_rejeitado(self, service):
        with pytest.raises(DadosJogoInvalidos) as exc:
            service.criar_jogo(**{**JOGO_BASE, "time_a": ""})
        assert exc.value.campo == "time_a"


#Consultas
class TestConsultarJogos:
    def test_jogos_do_dia(self, service):
        service.criar_jogo(**JOGO_BASE)
        service.criar_jogo(**JOGO_AMANHA)
        jogos = service.jogos_do_dia(date(2026, 6, 10))
        assert len(jogos) == 1
        assert jogos[0]["time_a"] == "Brasil"

    def test_jogos_de_outra_data(self, service):
        service.criar_jogo(**JOGO_BASE)
        service.criar_jogo(**JOGO_AMANHA)
        jogos = service.jogos_do_dia(date(2026, 6, 11))
        assert len(jogos) == 1
        assert jogos[0]["time_a"] == "França"

    def test_dia_sem_jogos_retorna_lista_vazia(self, service):
        service.criar_jogo(**JOGO_BASE)
        assert service.jogos_do_dia(date(2026, 6, 20)) == []

    def test_buscar_por_id(self, service):
        j = service.criar_jogo(**JOGO_BASE)
        encontrado = service.buscar_jogo(j["id_jogo"])
        assert encontrado["time_a"] == "Brasil"

    def test_jogo_nao_encontrado(self, service):
        with pytest.raises(JogoNaoEncontrado):
            service.buscar_jogo(999)

    def test_listar_todos(self, service):
        service.criar_jogo(**JOGO_BASE)
        service.criar_jogo(**JOGO_AMANHA)
        assert len(service.listar_todos()) == 2

    def test_listar_ordenado_por_horario(self, service):
        service.criar_jogo(**{**JOGO_BASE, "horario": "18:00"})
        service.criar_jogo(**{**JOGO_BASE, "time_a": "Alemanha", "time_b": "Japão", "horario": "14:00"})
        jogos = service.jogos_do_dia(date(2026, 6, 10))
        assert jogos[0]["time_a"] == "Alemanha"   


class TestStatus:
    def test_iniciar_jogo(self, service):
        j = service.criar_jogo(**JOGO_BASE)
        iniciado = service.iniciar_jogo(j["id_jogo"])
        assert iniciado["status"] == "em_andamento"
        assert iniciado["aberto_para_palpites"] is False

    def test_nao_pode_iniciar_jogo_ja_iniciado(self, service):
        j = service.criar_jogo(**JOGO_BASE)
        service.iniciar_jogo(j["id_jogo"])
        with pytest.raises(DadosJogoInvalidos):
            service.iniciar_jogo(j["id_jogo"])

    def test_cancelar_jogo(self, service):
        j = service.criar_jogo(**JOGO_BASE)
        cancelado = service.cancelar_jogo(j["id_jogo"])
        assert cancelado["status"] == "cancelado"

    def test_nao_pode_cancelar_finalizado(self, service):
        j = service.criar_jogo(**JOGO_BASE)
        service.registrar_resultado(j["id_jogo"], "time_a")
        with pytest.raises(JogoJaFinalizado):
            service.cancelar_jogo(j["id_jogo"])


#Resultado
class TestResultado:
    def test_time_a_vence(self, service):
        j = service.criar_jogo(**JOGO_BASE)
        r = service.registrar_resultado(j["id_jogo"], "time_a")
        assert r["status"] == "finalizado"
        assert r["resultado_final"] == "time_a"

    def test_time_b_vence(self, service):
        j = service.criar_jogo(**JOGO_BASE)
        r = service.registrar_resultado(j["id_jogo"], "time_b")
        assert r["resultado_final"] == "time_b"

    def test_empate(self, service):
        j = service.criar_jogo(**JOGO_BASE)
        r = service.registrar_resultado(j["id_jogo"], "empate")
        assert r["resultado_final"] == "empate"

    def test_resultado_invalido(self, service):
        j = service.criar_jogo(**JOGO_BASE)
        with pytest.raises(DadosJogoInvalidos) as exc:
            service.registrar_resultado(j["id_jogo"], "venceu_nos_pênaltis")
        assert exc.value.campo == "resultado"

    def test_nao_pode_alterar_finalizado(self, service):
        j = service.criar_jogo(**JOGO_BASE)
        service.registrar_resultado(j["id_jogo"], "time_a")
        with pytest.raises(JogoJaFinalizado):
            service.registrar_resultado(j["id_jogo"], "time_b")


class TestAtualizar:
    def test_atualizar_fase(self, service):
        j = service.criar_jogo(**JOGO_BASE)
        atualizado = service.atualizar_jogo(j["id_jogo"], {"fase": "semifinal"})
        assert atualizado["fase"] == "semifinal"

    def test_atualizar_horario(self, service):
        j = service.criar_jogo(**JOGO_BASE)
        atualizado = service.atualizar_jogo(j["id_jogo"], {"horario": "20:00"})
        assert atualizado["horario"] == "20:00"

    def test_atualizar_pontuacao(self, service):
        j = service.criar_jogo(**JOGO_BASE)
        atualizado = service.atualizar_jogo(j["id_jogo"], {"pontos_time_a": 5, "pontos_time_b": 15})
        assert atualizado["pontuacao"]["time_a"] == 5
        assert atualizado["pontuacao"]["time_b"] == 15

    def test_nao_atualiza_em_andamento(self, service):
        j = service.criar_jogo(**JOGO_BASE)
        service.iniciar_jogo(j["id_jogo"])
        with pytest.raises(JogoBloqueado):
            service.atualizar_jogo(j["id_jogo"], {"fase": "final"})

    def test_nao_atualiza_finalizado(self, service):
        j = service.criar_jogo(**JOGO_BASE)
        service.registrar_resultado(j["id_jogo"], "empate")
        with pytest.raises(JogoJaFinalizado):
            service.atualizar_jogo(j["id_jogo"], {"fase": "final"})