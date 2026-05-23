-- ============================================================
--  GoalPoint â€” Banco de Dados
--  Disciplina: Engenharia de Software
--  Gerado para uso com MySQL + Flask (Python)
-- ============================================================

CREATE DATABASE IF NOT EXISTS goalpoint_def
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE goalpoint_def;

-- ============================================================
--  TABELA: usuarios
--  Armazena os dados de cada participante do bolÃ£o.
--  - email Ã© Ãºnico (nÃ£o pode haver dois usuÃ¡rios com o mesmo login)
--  - senha_hash nunca deve guardar a senha em texto puro
-- ============================================================
CREATE TABLE usuarios (
  id_usuario    INT PRIMARY KEY AUTO_INCREMENT,
  nome          VARCHAR(100) NOT NULL,
  email         VARCHAR(150) NOT NULL UNIQUE,
  cpf           CHAR(11) NOT NULL UNIQUE,
  senha_hash    VARCHAR(255) NOT NULL,
  data_cadastro DATETIME DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT chk_usuarios_cpf_formato CHECK (cpf REGEXP '^[0-9]{11}$')
);

-- ============================================================
--  TABELA: jogos
--  Armazena todas as partidas exibidas no sistema.
--  - pontos_time_a / pontos_empate / pontos_time_b definem
--    a pontuaÃ§Ã£o de cada resultado possÃ­vel por jogo
--  - status controla se o usuÃ¡rio ainda pode palpitar
--  - resultado_final Ã© preenchido apÃ³s o jogo encerrar
-- ============================================================
CREATE TABLE jogos (
  id_jogo         INT PRIMARY KEY AUTO_INCREMENT,
  fase            ENUM('grupos','oitavas','quartas','semifinal','terceiro_lugar','final') NOT NULL,
  data_jogo       DATE NOT NULL,
  horario         TIME NOT NULL,
  time_a          VARCHAR(100) NOT NULL,
  time_b          VARCHAR(100) NOT NULL,
  status          ENUM('disponivel','em_andamento','finalizado') DEFAULT 'disponivel',
  resultado_final ENUM('time_a','empate','time_b') NULL,
  pontos_time_a   INT NOT NULL,
  pontos_empate   INT NOT NULL,
  pontos_time_b   INT NOT NULL
);

-- ============================================================
--  TABELA: palpites
--  Registra a aposta de cada usuÃ¡rio em cada jogo.
--  - UNIQUE (id_usuario, id_jogo) impede palpite duplicado
--  - acertou e pontos_ganhos sÃ£o preenchidos apÃ³s o jogo
-- ============================================================
CREATE TABLE palpites (
  id_palpite    INT PRIMARY KEY AUTO_INCREMENT,
  id_usuario    INT NOT NULL,
  id_jogo       INT NOT NULL,
  escolha       ENUM('time_a','empate','time_b') NOT NULL,
  data_palpite  DATETIME DEFAULT CURRENT_TIMESTAMP,
  acertou       BOOLEAN NULL,
  pontos_ganhos INT DEFAULT 0,
  FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario),
  FOREIGN KEY (id_jogo)    REFERENCES jogos(id_jogo),
  UNIQUE (id_usuario, id_jogo)
);

-- ============================================================
--  TABELA: faq
--  Armazena perguntas e respostas da pÃ¡gina de suporte.
--  Opcional â€” pode ser gerenciado direto no front-end
--  se as informaÃ§Ãµes forem fixas.
-- ============================================================
CREATE TABLE faq (
  id_faq   INT PRIMARY KEY AUTO_INCREMENT,
  pergunta TEXT NOT NULL,
  resposta TEXT NOT NULL
);

-- ============================================================
--  DADOS: jogos fictÃ­cios para demonstraÃ§Ã£o
--
--  Regras de pontuaÃ§Ã£o aplicadas:
--  - Jogo equilibrado:  time_a=10, empate=3, time_b=10
--  - Favorito vs AzarÃ£o: favorito=5, empate=3, azarÃ£o=15
-- ============================================================
INSERT INTO jogos (fase, data_jogo, horario, time_a, time_b, status, pontos_time_a, pontos_empate, pontos_time_b) VALUES
('grupos', '2026-06-10', '14:00:00', 'Brasil',  'Argentina', 'disponivel', 10, 3, 10),
('grupos', '2026-06-10', '15:00:00', 'Holanda', 'Portugal',  'disponivel', 10, 3, 10),
('grupos', '2026-06-10', '16:05:00', 'Catar',   'Espanha',   'disponivel', 15, 3,  5),
('grupos', '2026-06-10', '17:00:00', 'IrÃ£',     'EUA',       'disponivel', 10, 3, 10);

-- ============================================================
--  QUERIES ÃšTEIS PARA O BACK-END (Flask)
-- ============================================================

-- [1] Buscar todos os jogos disponÃ­veis para palpite:
-- SELECT * FROM jogos WHERE status = 'disponivel' ORDER BY data_jogo, horario;

-- [2] Registrar um palpite:
-- INSERT INTO palpites (id_usuario, id_jogo, escolha) VALUES (:id_usuario, :id_jogo, :escolha);

-- [3] Finalizar um jogo e registrar resultado:
-- UPDATE jogos SET resultado_final = :resultado, status = 'finalizado' WHERE id_jogo = :id_jogo;

-- [4] Pontuar os palpites apÃ³s finalizar um jogo:
-- UPDATE palpites
-- SET acertou = (escolha = :resultado),
--     pontos_ganhos = CASE
--         WHEN escolha = :resultado AND escolha = 'time_a' THEN (SELECT pontos_time_a FROM jogos WHERE id_jogo = :id_jogo)
--         WHEN escolha = :resultado AND escolha = 'empate'  THEN (SELECT pontos_empate  FROM jogos WHERE id_jogo = :id_jogo)
--         WHEN escolha = :resultado AND escolha = 'time_b' THEN (SELECT pontos_time_b FROM jogos WHERE id_jogo = :id_jogo)
--         ELSE 0
--     END
-- WHERE id_jogo = :id_jogo;

-- [5] Ranking geral:
-- SELECT u.nome, SUM(p.pontos_ganhos) AS total_pontos
-- FROM usuarios u
-- JOIN palpites p ON u.id_usuario = p.id_usuario
-- GROUP BY u.id_usuario
-- ORDER BY total_pontos DESC;