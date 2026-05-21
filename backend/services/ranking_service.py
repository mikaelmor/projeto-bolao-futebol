#services/ranking_service.py

from models.repositorio_palpite import RepositorioPalpite
from models.repositorio import RepositorioUsuario

class RankingService:
    def __init__(
        self,
        repositorio_palpite: RepositorioPalpite,
        repositorio_usuario: RepositorioUsuario,
    ):
        self._repo_palpite = repositorio_palpite
        self._repo_usuario = repositorio_usuario

    def ranking_geral(self) -> list[dict]:
        #Retorna todos os usuários com palpites, ordenados por pontuação total decrescente. Empates são desempatados pelo número de acertos.
        # Agrega pontos por usuário varrendo os palpites
        agregado: dict[int, dict] = {}
        for palpite in self._repo_palpite.listar_todos():
            uid = palpite.id_usuario
            if uid not in agregado:
                agregado[uid] = {"pontuacao_total": 0, "acertos": 0, "total_palpites": 0}
            agregado[uid]["pontuacao_total"] += palpite.pontos_ganhos
            agregado[uid]["total_palpites"]  += 1
            if palpite.acertou:
                agregado[uid]["acertos"] += 1

        if not agregado:
            return []

        linhas = []
        for uid, stats in agregado.items():
            usuario = self._repo_usuario.buscar_por_id(uid)
            nome = usuario.nome if usuario else f"Usuário {uid}"
            linhas.append({
                "id_usuario":      uid,
                "nome":            nome,
                "pontuacao_total": stats["pontuacao_total"],
                "acertos":         stats["acertos"],
                "total_palpites":  stats["total_palpites"],
            })

        # Ordena: maior pontuação primeiro
        linhas.sort(key=lambda x: (x["pontuacao_total"], x["acertos"]), reverse=True)

        # Atribui posição (dois usuários com mesma pontuação ficam na mesma posição)
        posicao = 1
        for i, linha in enumerate(linhas):
            if i > 0 and linha["pontuacao_total"] < linhas[i - 1]["pontuacao_total"]:
                posicao = i + 1
            linha["posicao"] = posicao

        return linhas