import { useEffect, useState } from "react";
import { io } from "socket.io-client";

const socket = io("http://localhost:5000");

const STATUS_LABEL = {
  disponivel: { text: "Agendado", color: "#4ade80" },
  em_andamento: { text: "Ao vivo", color: "#34d399" },
  finalizado: { text: "Finalizado", color: "#6b7280" },
  cancelado: { text: "Cancelado", color: "#f87171" },
};

const styles = {
  root: {
    minHeight: "100vh",
    fontFamily: "'Inter', 'Segoe UI', sans-serif",
    position: "relative",
    overflow: "hidden",
    color: "#f1f5f9",
  },
  bgImage: {
    position: "fixed",
    inset: 0,
    backgroundImage: `url('https://images.unsplash.com/photo-1522778119026-d647f0596c20?w=1600&q=80')`,
    backgroundSize: "cover",
    backgroundPosition: "center center",
    filter: "blur(5px) brightness(0.28) saturate(1.6)",
    transform: "scale(1.05)",
    zIndex: 0,
  },
  bgOverlay: {
    position: "fixed",
    inset: 0,
    background: "linear-gradient(135deg, rgba(5,78,22,0.55) 0%, rgba(10,18,30,0.88) 55%, rgba(161,122,0,0.3) 100%)",
    zIndex: 1,
  },
  content: {
    position: "relative",
    zIndex: 2,
    padding: "40px 32px",
    maxWidth: 900,
    margin: "0 auto",
  },
  header: {
    marginBottom: 36,
    borderBottom: "1px solid rgba(74,222,128,0.15)",
    paddingBottom: 20,
  },
  badge: {
    display: "inline-block",
    background: "rgba(5,78,22,0.45)",
    border: "1px solid rgba(74,222,128,0.35)",
    color: "#86efac",
    fontSize: 11,
    fontWeight: 600,
    letterSpacing: "0.12em",
    textTransform: "uppercase",
    padding: "4px 12px",
    borderRadius: 999,
    marginBottom: 12,
  },
  title: {
    fontSize: 32,
    fontWeight: 700,
    margin: 0,
    background: "linear-gradient(90deg, #fff 0%, #fcd34d 100%)",
    WebkitBackgroundClip: "text",
    WebkitTextFillColor: "transparent",
    letterSpacing: "-0.02em",
  },
  subtitle: {
    color: "rgba(241,245,249,0.5)",
    fontSize: 14,
    marginTop: 6,
    marginBottom: 0,
  },
  card: {
    background: "rgba(15,23,42,0.65)",
    border: "1px solid rgba(74,222,128,0.12)",
    borderRadius: 16,
    padding: "20px 24px",
    marginBottom: 16,
    backdropFilter: "blur(12px)",
    WebkitBackdropFilter: "blur(12px)",
    transition: "border-color 0.2s",
  },
  cardHeader: {
    display: "flex",
    alignItems: "center",
    justifyContent: "space-between",
    marginBottom: 8,
  },
  matchTitle: {
    fontSize: 18,
    fontWeight: 700,
    margin: 0,
    color: "#f8fafc",
    letterSpacing: "-0.01em",
  },
  statusPill: (status) => ({
    fontSize: 11,
    fontWeight: 700,
    letterSpacing: "0.1em",
    textTransform: "uppercase",
    color: STATUS_LABEL[status]?.color || "#94a3b8",
    background: `${STATUS_LABEL[status]?.color || "#94a3b8"}18`,
    border: `1px solid ${STATUS_LABEL[status]?.color || "#94a3b8"}44`,
    padding: "3px 10px",
    borderRadius: 999,
    display: "flex",
    alignItems: "center",
    gap: 5,
  }),
  liveDot: {
    width: 6,
    height: 6,
    borderRadius: "50%",
    background: "#34d399",
    animation: "pulse 1.5s infinite",
  },
  meta: {
    fontSize: 12,
    color: "rgba(241,245,249,0.4)",
    marginBottom: 16,
  },
  resultado: {
    fontSize: 13,
    color: "#fcd34d",
    fontWeight: 600,
    marginBottom: 12,
  },
  btnRow: {
    display: "flex",
    gap: 8,
    flexWrap: "wrap",
  },
  btn: (bg, text = "#fff") => ({
    padding: "8px 16px",
    background: bg,
    color: text,
    border: "none",
    borderRadius: 10,
    cursor: "pointer",
    fontSize: 13,
    fontWeight: 600,
    transition: "opacity 0.15s, transform 0.1s",
    letterSpacing: "0.01em",
  }),
  empty: {
    textAlign: "center",
    color: "rgba(241,245,249,0.3)",
    fontSize: 14,
    marginTop: 60,
  },
  loginWrap: {
    minHeight: "100vh",
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    justifyContent: "center",
    position: "relative",
    fontFamily: "'Inter', 'Segoe UI', sans-serif",
  },
  loginCard: {
    position: "relative",
    zIndex: 2,
    background: "rgba(15,23,42,0.75)",
    border: "1px solid rgba(74,222,128,0.2)",
    borderRadius: 20,
    padding: "40px 36px",
    width: 340,
    backdropFilter: "blur(16px)",
    WebkitBackdropFilter: "blur(16px)",
    textAlign: "center",
  },
  loginTitle: {
    fontSize: 22,
    fontWeight: 700,
    background: "linear-gradient(90deg, #fff 0%, #fcd34d 100%)",
    WebkitBackgroundClip: "text",
    WebkitTextFillColor: "transparent",
    marginBottom: 6,
    marginTop: 0,
  },
  loginSub: {
    color: "rgba(241,245,249,0.4)",
    fontSize: 13,
    marginBottom: 28,
  },
  input: {
    width: "100%",
    padding: "12px 16px",
    background: "rgba(255,255,255,0.06)",
    border: "1px solid rgba(74,222,128,0.2)",
    borderRadius: 10,
    color: "#f1f5f9",
    fontSize: 15,
    outline: "none",
    boxSizing: "border-box",
    marginBottom: 14,
  },
  loginBtn: {
    width: "100%",
    padding: "12px",
    background: "linear-gradient(135deg, #15803d, #16a34a)",
    color: "#fff",
    border: "none",
    borderRadius: 10,
    cursor: "pointer",
    fontSize: 15,
    fontWeight: 700,
    letterSpacing: "0.02em",
    transition: "opacity 0.15s",
  },
};

const globalCss = `
  @keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.3; }
  }
  button:disabled { opacity: 0.35 !important; cursor: not-allowed !important; }
  button:not(:disabled):hover { opacity: 0.82; transform: translateY(-1px); }
  button:not(:disabled):active { transform: scale(0.97); }
`;

export default function Admin() {
  const [jogos, setJogos] = useState([]);
  const [senha, setSenha] = useState("");
  const [autenticado, setAutenticado] = useState(false);

  const SENHA_ADMIN = "goalpoint";

  const normalizarJogo = (jogo) => ({
    ...jogo,
    id_jogo: jogo.id_jogo ?? jogo.id,
    time_a: jogo.time_a ?? jogo.selecao_a,
    time_b: jogo.time_b ?? jogo.selecao_b,
    status:
      jogo.status === "agendado"
        ? "disponivel"
        : jogo.status === "encerrado"
          ? "finalizado"
          : jogo.status,
  });

  useEffect(() => {
    if (!autenticado) return;

    const carregarJogos = () => {
      fetch("http://localhost:5000/api/simulacao/jogos", {
        headers: { "Content-Type": "application/json" },
      })
        .then((r) => r.json())
        .then((data) => {
          setJogos((data.jogos || []).map(normalizarJogo));
        });
    };

    carregarJogos();
    const intervalId = setInterval(carregarJogos, 1000);

    socket.on("jogo:atualizado", (data) => {
      const jogoAtualizado = normalizarJogo(data.jogo);
      setJogos((prev) =>
        prev.map((j) => (j.id_jogo === jogoAtualizado.id_jogo ? jogoAtualizado : j))
      );
    });

    socket.on("admin:erro", (data) => {
      alert(data.erro || "Erro ao controlar jogo.");
    });

    return () => {
      clearInterval(intervalId);
      socket.off("jogo:atualizado");
      socket.off("admin:erro");
    };
  }, [autenticado]);

  const Bg = () => (
    <>
      <style>{globalCss}</style>
      <div style={styles.bgImage} />
      <div style={styles.bgOverlay} />
    </>
  );

  if (!autenticado) {
    return (
      <div style={styles.loginWrap}>
        <Bg />
        <div style={styles.loginCard}>
          <p style={{ ...styles.badge, display: "block", marginBottom: 16 }}>GoalPoint</p>
          <h2 style={styles.loginTitle}>Painel Admin</h2>
          <p style={styles.loginSub}>Acesso restrito</p>
          <input
            type="password"
            placeholder="Senha admin"
            value={senha}
            onChange={(e) => setSenha(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter") {
                if (senha === SENHA_ADMIN) setAutenticado(true);
                else alert("Senha incorreta!");
              }
            }}
            style={styles.input}
          />
          <button
            style={styles.loginBtn}
            onClick={() => {
              if (senha === SENHA_ADMIN) setAutenticado(true);
              else alert("Senha incorreta!");
            }}
          >
            Entrar
          </button>
        </div>
      </div>
    );
  }

  return (
    <div style={styles.root}>
      <Bg />
      <div style={styles.content}>
        <div style={styles.header}>
          <span style={styles.badge}>Admin · GoalPoint</span>
          <h1 style={styles.title}>Controle de Partidas</h1>
          <p style={styles.subtitle}>Gerencie as simulações em tempo real</p>
        </div>

        {jogos.length === 0 && <p style={styles.empty}>Nenhum jogo encontrado.</p>}

        {jogos.map((jogo) => {
          const statusInfo = STATUS_LABEL[jogo.status] || { text: jogo.status, color: "#94a3b8" };
          const emAndamento = jogo.status === "em_andamento";
          const disponivel = jogo.status === "disponivel";

          return (
            <div key={jogo.id_jogo} style={styles.card}>
              <div style={styles.cardHeader}>
                <h3 style={styles.matchTitle}>
                  {jogo.time_a} <span style={{ color: "rgba(241,245,249,0.35)", fontWeight: 400 }}>×</span> {jogo.time_b}
                </h3>
                <span style={styles.statusPill(jogo.status)}>
                  {emAndamento && <span style={styles.liveDot} />}
                  {statusInfo.text}
                </span>
              </div>

              <p style={styles.meta}>
                {jogo.fase} &nbsp;·&nbsp; {jogo.data_jogo} {jogo.horario}
              </p>

              {jogo.resultado_final && (
                <p style={styles.resultado}>Resultado: {jogo.resultado_final}</p>
              )}

              <div style={styles.btnRow}>
                <button
                  onClick={() => socket.emit("admin:iniciar_jogo", { jogo_id: jogo.id_jogo })}
                  disabled={!disponivel}
                  style={styles.btn("#059669")}
                >
                  ▶ Iniciar
                </button>

                <button
                  onClick={() => socket.emit("admin:finalizar_jogo", { jogo_id: jogo.id_jogo, resultado: "time_a" })}
                  disabled={!emAndamento}
                  style={styles.btn("#3b82f6")}
                >
                  🏆 {jogo.time_a}
                </button>

                <button
                  onClick={() => socket.emit("admin:finalizar_jogo", { jogo_id: jogo.id_jogo, resultado: "empate" })}
                  disabled={!emAndamento}
                  style={styles.btn("#d97706", "#fff")}
                >
                  🤝 Empate
                </button>

                <button
                  onClick={() => socket.emit("admin:finalizar_jogo", { jogo_id: jogo.id_jogo, resultado: "time_b" })}
                  disabled={!emAndamento}
                  style={styles.btn("#8b5cf6")}
                >
                  🏆 {jogo.time_b}
                </button>

                <button
                  onClick={() => socket.emit("admin:randomizar_resultado", { jogo_id: jogo.id_jogo })}
                  disabled={!emAndamento}
                  style={styles.btn("#0e7490")}
                >
                  🎲 Randomizar
                </button>

                <button
                  onClick={() => socket.emit("admin:reiniciar_jogo", { jogo_id: jogo.id_jogo })}
                  style={styles.btn("#dc2626")}
                >
                  🔄 Reiniciar
                </button>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
