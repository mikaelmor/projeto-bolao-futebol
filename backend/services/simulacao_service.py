import random
from datetime import datetime

from models.jogo import ErroJogo
from services.jogo_service import JogoService


PLACARES_POSSIVEIS = [
    (2, 0),
    (3, 2),
    (0, 1),
    (1, 2),
    (2, 2),
    (1, 0),
    (0, 2),
    (2, 1),
    (3, 1),
    (1, 1),
    (0, 3),
]


class SimulacaoService:
    def __init__(self, jogo_service: JogoService):
        self._jogo_service = jogo_service
        self._simulacoes: dict[int, dict] = {}
        self._palpites: dict[int, dict[str, str]] = {}
        self._placares_finalizados: dict[int, tuple[int, int]] = {}

    def listar_jogos(self) -> list[dict]:
        jogos = self._jogo_service.listar_todos()
        return [self._com_simulacao(jogo) for jogo in jogos]

    def finalizar_expirados(self) -> list[dict]:
        finalizados = []
        agora = datetime.utcnow()

        for jogo_id, simulacao in list(self._simulacoes.items()):
            decorrido = max(0, int((agora - simulacao["inicio"]).total_seconds()))
            if decorrido >= simulacao["duracao_segundos"]:
                finalizados.append(self.finalizar(jogo_id))

        return finalizados

    def registrar_palpite(self, jogo_id: int, usuario_id: str, escolha: str) -> dict:
        jogo = self._jogo_service.buscar_jogo(jogo_id)
        if jogo["status"] not in ("agendado", "disponivel"):
            raise ErroJogo("Palpites encerrados para este jogo.", campo="status")

        if escolha not in ("time1", "draw", "time2"):
            raise ErroJogo("Escolha invalida.", campo="escolha")

        usuario_id = (usuario_id or "").strip()
        if not usuario_id:
            raise ErroJogo("Usuario invalido.", campo="usuario_id")

        self._palpites.setdefault(jogo_id, {})[usuario_id] = escolha

        return {
            "jogo_id": jogo_id,
            "usuario_id": usuario_id,
            "escolha": escolha,
        }

    def remover_palpite(self, jogo_id: int, usuario_id: str) -> dict:
        jogo = self._jogo_service.buscar_jogo(jogo_id)
        if jogo["status"] not in ("agendado", "disponivel"):
            raise ErroJogo("Palpites encerrados para este jogo.", campo="status")

        usuario_id = (usuario_id or "").strip()
        if not usuario_id:
            raise ErroJogo("Usuario invalido.", campo="usuario_id")

        self._palpites.get(jogo_id, {}).pop(usuario_id, None)

        return {
            "jogo_id": jogo_id,
            "usuario_id": usuario_id,
            "escolha": None,
        }

    def iniciar(self, jogo_id: int, duracao_segundos: int = 120) -> dict:
        duracao_segundos = self._normalizar_duracao(duracao_segundos)
        placar_final = random.choice(PLACARES_POSSIVEIS)

        self._simulacoes[jogo_id] = {
            "inicio": datetime.utcnow(),
            "duracao_segundos": duracao_segundos,
            "placar_final": placar_final,
            "gols": self._gerar_gols(placar_final, duracao_segundos),
        }

        jogo = self._jogo_service.iniciar_jogo(jogo_id)
        return self._com_simulacao(jogo)

    def finalizar(self, jogo_id: int) -> dict:
        jogo = self._jogo_service.buscar_jogo(jogo_id)
        simulacao = self._simulacoes.get(jogo_id)
        placar_final = simulacao["placar_final"] if simulacao else random.choice(PLACARES_POSSIVEIS)
        resultado = self._resultado_por_placar(placar_final)

        jogo = self._jogo_service.registrar_resultado(
            jogo_id,
            resultado,
        )
        self._simulacoes.pop(jogo_id, None)
        self._placares_finalizados[jogo_id] = placar_final
        return self._com_simulacao(jogo)

    def definir_resultado_planejado(self, jogo_id: int, resultado: str) -> dict:
        if resultado not in ("time_a", "empate", "time_b"):
            raise ErroJogo("Resultado invalido. Use: time_a | empate | time_b", campo="resultado")
        if jogo_id not in self._simulacoes:
            raise ErroJogo("Este jogo nao esta em simulacao.", campo="status")

        simulacao = self._simulacoes[jogo_id]
        decorrido = max(0, int((datetime.utcnow() - simulacao["inicio"]).total_seconds()))
        placar_atual = self._placar_atual(simulacao, decorrido)
        placar_final = self._placar_para_resultado(resultado, placar_atual)

        simulacao["placar_final"] = placar_final
        simulacao["gols"] = self._gerar_gols_restantes(
            simulacao["gols"],
            placar_final,
            placar_atual,
            decorrido,
            simulacao["duracao_segundos"],
        )

        return self._com_simulacao(self._jogo_service.buscar_jogo(jogo_id))

    def atualizar_duracao(self, jogo_id: int, duracao_segundos: int) -> dict:
        if jogo_id not in self._simulacoes:
            raise ErroJogo("Este jogo nao esta em simulacao.", campo="status")

        duracao_segundos = self._normalizar_duracao(duracao_segundos)
        simulacao = self._simulacoes[jogo_id]
        simulacao["duracao_segundos"] = duracao_segundos
        simulacao["gols"] = self._gerar_gols(simulacao["placar_final"], duracao_segundos)

        return self._com_simulacao(self._jogo_service.buscar_jogo(jogo_id))

    def _com_simulacao(self, jogo: dict) -> dict:
        jogo = self._normalizar_jogo(jogo)
        simulacao = self._simulacoes.get(jogo["id"])
        if not simulacao:
            placar_finalizado = self._placares_finalizados.get(jogo["id"])
            if placar_finalizado:
                jogo = {
                    **jogo,
                    "placar": {
                        "selecao_a": placar_finalizado[0],
                        "selecao_b": placar_finalizado[1],
                        "display": f'{jogo["selecao_a"]} {placar_finalizado[0]} x {placar_finalizado[1]} {jogo["selecao_b"]}',
                    },
                    "vencedor": self._vencedor_por_placar(jogo, placar_finalizado),
                }
            return {
                **jogo,
                "simulacao": None,
                "palpites_total": len(self._palpites.get(jogo["id"], {})),
            }

        decorrido = max(0, int((datetime.utcnow() - simulacao["inicio"]).total_seconds()))
        duracao = simulacao["duracao_segundos"]
        segundo_visual = min(decorrido, duracao)
        minuto = min(90, int((segundo_visual / duracao) * 90)) if duracao else 0
        placar_a, placar_b = self._placar_atual(simulacao, segundo_visual)

        return {
            **jogo,
            "status": "em_andamento",
            "placar": {
                "selecao_a": placar_a,
                "selecao_b": placar_b,
                "display": f'{jogo["selecao_a"]} {placar_a} x {placar_b} {jogo["selecao_b"]}',
            },
            "simulacao": {
                "minuto": minuto,
                "duracao_segundos": duracao,
                "segundos_decorridos": segundo_visual,
                "segundos_restantes": max(0, duracao - segundo_visual),
            },
            "palpites_total": len(self._palpites.get(jogo["id"], {})),
        }

    @staticmethod
    def _normalizar_jogo(jogo: dict) -> dict:
        if "id" in jogo and "selecao_a" in jogo:
            return jogo

        status_map = {
            "disponivel": "agendado",
            "em_andamento": "em_andamento",
            "finalizado": "encerrado",
            "cancelado": "cancelado",
        }
        data_jogo = jogo.get("data_jogo", "")
        horario = jogo.get("horario", "")

        return {
            "id": jogo.get("id_jogo"),
            "selecao_a": jogo.get("time_a"),
            "selecao_b": jogo.get("time_b"),
            "horario": f"{data_jogo}T{horario}:00" if data_jogo and horario and len(horario) == 5 else horario,
            "fase": "Copa do Mundo",
            "estadio": "Estadio GoalPoint",
            "grupo": None,
            "status": status_map.get(jogo.get("status"), jogo.get("status")),
            "resultado_final": jogo.get("resultado_final"),
            "placar": None,
            "vencedor": None,
            "criado_em": None,
            "pontuacao": jogo.get("pontuacao"),
        }

    @staticmethod
    def _resultado_por_placar(placar: tuple[int, int]) -> str:
        if placar[0] > placar[1]:
            return "time_a"
        if placar[1] > placar[0]:
            return "time_b"
        return "empate"

    @staticmethod
    def _vencedor_por_placar(jogo: dict, placar: tuple[int, int]) -> str:
        if placar[0] > placar[1]:
            return jogo["selecao_a"]
        if placar[1] > placar[0]:
            return jogo["selecao_b"]
        return "empate"

    @staticmethod
    def _normalizar_duracao(duracao_segundos: int) -> int:
        try:
            duracao = int(duracao_segundos)
        except (TypeError, ValueError):
            duracao = 120
        return max(10, min(duracao, 3600))

    @staticmethod
    def _placar_para_resultado(resultado: str, placar_atual: tuple[int, int]) -> tuple[int, int]:
        gols_a, gols_b = placar_atual

        if resultado == "time_a":
            return max(gols_a, gols_b + 1), gols_b
        if resultado == "time_b":
            return gols_a, max(gols_b, gols_a + 1)

        gols_empate = max(gols_a, gols_b)
        return gols_empate, gols_empate

    @staticmethod
    def _gerar_gols(placar_final: tuple[int, int], duracao_segundos: int) -> list[dict]:
        gols = []
        for lado, total in (("a", placar_final[0]), ("b", placar_final[1])):
            for _ in range(total):
                gols.append({
                    "lado": lado,
                    "segundo": random.randint(5, max(5, duracao_segundos - 3)),
                })
        return sorted(gols, key=lambda gol: gol["segundo"])

    @staticmethod
    def _gerar_gols_restantes(
        gols_atuais: list[dict],
        placar_final: tuple[int, int],
        placar_atual: tuple[int, int],
        segundo_atual: int,
        duracao_segundos: int,
    ) -> list[dict]:
        gols = [gol for gol in gols_atuais if gol["segundo"] <= segundo_atual]
        inicio = min(duracao_segundos, segundo_atual + 1)
        fim = max(inicio, duracao_segundos - 3)

        for lado, final, atual in (
            ("a", placar_final[0], placar_atual[0]),
            ("b", placar_final[1], placar_atual[1]),
        ):
            for _ in range(max(0, final - atual)):
                gols.append({
                    "lado": lado,
                    "segundo": random.randint(inicio, fim),
                })

        return sorted(gols, key=lambda gol: gol["segundo"])

    @staticmethod
    def _placar_atual(simulacao: dict, segundo_visual: int) -> tuple[int, int]:
        placar_a = 0
        placar_b = 0

        for gol in simulacao["gols"]:
            if gol["segundo"] > segundo_visual:
                continue
            if gol["lado"] == "a":
                placar_a += 1
            else:
                placar_b += 1

        return placar_a, placar_b
