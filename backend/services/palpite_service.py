#services/palpite_service.py
from datetime import datetime
from models.jogo import StatusJogo
from models.palpite import(
    EscolhaPalpite,
    EscolhaInvalida,
    Palpite,
    PalpiteBloqueado,
    PalpiteDuplicado,
    PalpiteNaoEncontrado,
)
from models.repositorio_jogo import RepositorioJogo
from models.repositorio_palpite import RepositorioPalpite

ESCOLHAS_VALIDAS = {e.value for e in EscolhaPalpite}

class PalpiteService:
    def __init__(
        self,
        repositorio_palpite: RepositorioPalpite,
        repositorio_jogo: RepositorioJogo,
    ):
        self._repo = repositorio_palpite
        self._repo_jogo = repositorio_jogo

#criar palpite
    def criar_palpite(self, id_usuario: int, id_jogo: int, escolha: str) -> dict:
        #registra o palpite de um usuario pra uma partida

        escolha = escolha.strip().lower()
        if escolha not in ESCOLHAS_VALIDAS:
            raise EscolhaInvalida()
        
        jogo = self._repo_jogo.buscar_por_id(id_jogo)
        if not jogo:
            from models.jogo import JogoNaoEncontrado
            raise JogoNaoEncontrado()
        
        if not jogo.aberto_para_palpites:
            raise PalpiteBloqueado()
        
        if self._repo.buscar_por_usuario_e_jogo(id_usuario, id_jogo):
            raise PalpiteDuplicado()
        
        palpite = Palpite(
            id_usuario=id_usuario,
            id_jogo=id_jogo,
            escolha=EscolhaPalpite(escolha),
        )
        palpite = self._repo.salvar(palpite)
        return self._enriquecer(palpite, jogo)

    def salvar_palpite(self, id_usuario: int, id_jogo: int, escolha: str) -> dict:
        escolha = escolha.strip().lower()
        if escolha not in ESCOLHAS_VALIDAS:
            raise EscolhaInvalida()

        jogo = self._repo_jogo.buscar_por_id(id_jogo)
        if not jogo:
            from models.jogo import JogoNaoEncontrado
            raise JogoNaoEncontrado()

        if not jogo.aberto_para_palpites:
            raise PalpiteBloqueado()

        palpite = self._repo.buscar_por_usuario_e_jogo(id_usuario, id_jogo)
        if palpite:
            palpite.escolha = EscolhaPalpite(escolha)
            palpite.acertou = None
            palpite.pontos_ganhos = 0
            palpite = self._repo.atualizar(palpite)
            return self._enriquecer(palpite, jogo)

        return self.criar_palpite(id_usuario, id_jogo, escolha)

    def remover_palpite_do_jogo(self, id_usuario: int, id_jogo: int) -> dict:
        jogo = self._repo_jogo.buscar_por_id(id_jogo)
        if not jogo:
            from models.jogo import JogoNaoEncontrado
            raise JogoNaoEncontrado()

        if not jogo.aberto_para_palpites:
            raise PalpiteBloqueado()

        palpite = self._repo.excluir_por_usuario_e_jogo(id_usuario, id_jogo)
        if not palpite:
            raise PalpiteNaoEncontrado()

        return self._enriquecer(palpite, jogo)
    
    def editar_palpite(self, id_palpite: int, id_usuario: int, nova_escolha: str) -> dict:
        nova_escolha = nova_escolha.strip().lower()
        if nova_escolha not in ESCOLHAS_VALIDAS:
            raise EscolhaInvalida()
        
        palpite = self._repo.buscar_por_id(id_palpite)
        if not palpite or palpite.id_usuario != id_usuario:
            raise PalpiteNaoEncontrado()

        jogo = self._repo_jogo.buscar_por_id(palpite.id_jogo)
        if not jogo.aberto_para_palpites:
            raise PalpiteBloqueado()

        palpite.escolha = EscolhaPalpite(nova_escolha)
        palpite = self._repo.atualizar(palpite)
        return self._enriquecer(palpite, jogo)
    
    def palpites_do_usuario(self, id_usuario: int) -> list[dict]:
        palpites = self._repo.listar_por_usuario(id_usuario)
        resultado = []
        for p in palpites:
            jogo = self._repo_jogo.buscar_por_id(p.id_jogo)
            resultado.append(self._enriquecer(p, jogo))
        return resultado

    def buscar_palpite(self, id_palpite: int, id_usuario: int) -> dict:
        palpite = self._repo.buscar_por_id(id_palpite)
        if not palpite or palpite.id_usuario != id_usuario:
            raise PalpiteNaoEncontrado()
        jogo = self._repo_jogo.buscar_por_id(palpite.id_jogo)
        return self._enriquecer(palpite, jogo)

    def pontuacao_total(self, id_usuario: int) -> dict:
        #soma de pontos do usuario
        palpites = self._repo.listar_por_usuario(id_usuario)
        total = sum(p.pontos_ganhos for p in palpites)
        acertos = sum(1 for p in palpites if p.acertou)
        return {
            "id_usuario": id_usuario,
            "pontuacao_total": total,
            "total_palpites": len(palpites),
            "acertos": acertos,
        }


    def avaliar_palpites_do_jogo(self, id_jogo: int) -> list[dict]:
    
        #Avalia todos os palpites de uma partida finalizada e atribui pontos
        jogo = self._repo_jogo.buscar_por_id(id_jogo)
        if not jogo or jogo.resultado_final is None:
            return []

        palpites = self._repo.listar_por_jogo(id_jogo)
        avaliados = []
        for p in palpites:
            p.avaliar(jogo)
            self._repo.atualizar(p)
            avaliados.append(self._enriquecer(p, jogo))
        return avaliados

    @staticmethod
    def _enriquecer(palpite: Palpite, jogo) -> dict:
        dados = palpite.to_dict()
        dados["partida"] = {
            "time_a": jogo.time_a,
            "time_b": jogo.time_b,
            "data_jogo": jogo.data_jogo.isoformat(),
            "horario": jogo.horario.strftime("%H:%M"),
            "status": jogo.status.value,
            "resultado_final": jogo.resultado_final.value if jogo.resultado_final else None,
            "aberto_para_palpites": jogo.aberto_para_palpites,
        }
        # Mostra pontos possíveis enquanto pendente
        if palpite.acertou is None:
            dados["pontos_possiveis"] = jogo.pontos_para(palpite.escolha.value)
        return dados
