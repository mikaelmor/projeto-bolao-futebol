from flask import current_app
import random


def registrar_eventos(socketio):

    @socketio.on("admin:iniciar_jogo")
    def iniciar_jogo(data):
        jogo_id = data.get("jogo_id")
        service = current_app.config["SIMULACAO_SERVICE"]
        try:
            jogo = service.iniciar(jogo_id)
            socketio.emit("jogo:atualizado", {"jogo": jogo})
        except Exception as exc:
            socketio.emit("admin:erro", {"erro": str(exc)})

    @socketio.on("admin:finalizar_jogo")
    def finalizar_jogo(data):
        jogo_id = data.get("jogo_id")
        resultado = data.get("resultado")
        try:
            jogo = _definir_resultado_planejado(jogo_id, resultado)
            socketio.emit("jogo:atualizado", {"jogo": jogo})
        except Exception as exc:
            socketio.emit("admin:erro", {"erro": str(exc)})

    @socketio.on("admin:randomizar_resultado")
    def randomizar_resultado(data):
        jogo_id = data.get("jogo_id")
        resultado = random.choice(("time_a", "empate", "time_b"))
        try:
            jogo = _definir_resultado_planejado(jogo_id, resultado)
            socketio.emit("jogo:atualizado", {"jogo": jogo})
        except Exception as exc:
            socketio.emit("admin:erro", {"erro": str(exc)})
           
    @socketio.on("admin:reiniciar_jogo")
    def reiniciar_jogo(data):
        jogo_id = data.get("jogo_id")
        jogo_service = current_app.config["JOGO_SERVICE"]
        sim_service = current_app.config["SIMULACAO_SERVICE"]

        sim_service._simulacoes.pop(jogo_id, None)
        sim_service._placares_finalizados.pop(jogo_id, None)

        jogo = jogo_service._repo.buscar_por_id(jogo_id)
        jogo.status = __import__('models.jogo', fromlist=['StatusJogo']).StatusJogo.DISPONIVEL
        jogo.resultado_final = None
        jogo_service._repo.atualizar(jogo)

        socketio.emit("jogo:atualizado", {"jogo": sim_service._com_simulacao(jogo.to_dict())})


def _definir_resultado_planejado(jogo_id, resultado):
    sim_service = current_app.config["SIMULACAO_SERVICE"]
    return sim_service.definir_resultado_planejado(jogo_id, resultado)
