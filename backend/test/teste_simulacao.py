import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from services.simulacao_service import PLACARES_POSSIVEIS, SimulacaoService


class TestPlacarEmpate:
    def test_empates_possiveis_sao_placares_com_gols(self):
        empates = {placar for placar in PLACARES_POSSIVEIS if placar[0] == placar[1]}

        assert empates == {(1, 1), (2, 2), (3, 3)}

    def test_empate_nunca_planeja_zero_a_zero(self):
        placares = {
            SimulacaoService._placar_para_resultado("empate", (0, 0))
            for _ in range(20)
        }

        assert placares <= {(1, 1), (2, 2), (3, 3)}
        assert (0, 0) not in placares

    def test_empate_respeita_gols_ja_marcados(self):
        placar = SimulacaoService._placar_para_resultado("empate", (2, 1))

        assert placar in {(2, 2), (3, 3)}
