"""
models/repositorio_mysql.py - implementações MySQL de todos os repositórios do GoalPoint
"""
import os
from datetime import date, datetime, time
import mysql.connector
from mysql.connector.connection import MySQLConnection
from models.jogo import FaseJogo, Jogo, ResultadoFinal, StatusJogo
from models.palpite import EscolhaPalpite, Palpite
from models.repositorio import RepositorioUsuario
from models.repositorio_jogo import RepositorioJogo
from models.repositorio_palpite import RepositorioPalpite
from models.usuario import Usuario

# Conexão 
def criar_conexao() -> MySQLConnection:

    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", 3306)),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "goalpoint"),
        charset="utf8mb4",
        autocommit=False,
    )

#Repositório de Usuários 

class RepositorioUsuarioMySQL(RepositorioUsuario):

    def __init__(self, conn: MySQLConnection):
        self._conn = conn

    def salvar(self, usuario: Usuario) -> Usuario:
        cursor = self._conn.cursor()
        cursor.execute(
            """
            INSERT INTO usuarios (nome, email, senha_hash)
            VALUES (%s, %s, %s)
            """,
            (usuario.nome, usuario.email, usuario.senha_hash),
        )
        self._conn.commit()
        usuario.id = cursor.lastrowid
        return usuario

    def buscar_por_email(self, email: str) -> Usuario | None:
        cursor = self._conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
        row = cursor.fetchone()
        return self._row_para_usuario(row) if row else None

    def buscar_por_cpf(self, cpf: str) -> Usuario | None:
        # CPF ñ está no banco SQL — retorna None 
        return None

    def buscar_por_id(self, id: int) -> Usuario | None:
        cursor = self._conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios WHERE id_usuario = %s", (id,))
        row = cursor.fetchone()
        return self._row_para_usuario(row) if row else None

    @staticmethod
    def _row_para_usuario(row: dict) -> Usuario:
        return Usuario(
            id=row["id_usuario"],
            nome=row["nome"],
            email=row["email"],
            cpf="",                   
            senha_hash=row["senha_hash"],
            criado_em=row.get("data_cadastro", datetime.utcnow()),
        )


# Repositório de Jogos
class RepositorioJogoMySQL(RepositorioJogo):

    def __init__(self, conn: MySQLConnection):
        self._conn = conn

    def salvar(self, jogo: Jogo) -> Jogo:
        cursor = self._conn.cursor()
        cursor.execute(
            """
            INSERT INTO jogos
                (fase, data_jogo, horario, time_a, time_b,
                 status, pontos_time_a, pontos_empate, pontos_time_b)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                jogo.fase.value,
                jogo.data_jogo,
                jogo.horario.strftime("%H:%M:%S"),
                jogo.time_a,
                jogo.time_b,
                jogo.status.value,
                jogo.pontos_time_a,
                jogo.pontos_empate,
                jogo.pontos_time_b,
            ),
        )
        self._conn.commit()
        jogo.id_jogo = cursor.lastrowid
        return jogo

    def atualizar(self, jogo: Jogo) -> Jogo:
        cursor = self._conn.cursor()
        cursor.execute(
            """
            UPDATE jogos
            SET fase = %s, data_jogo = %s, horario = %s,
                time_a = %s, time_b = %s, status = %s,
                resultado_final = %s,
                pontos_time_a = %s, pontos_empate = %s, pontos_time_b = %s
            WHERE id_jogo = %s
            """,
            (
                jogo.fase.value,
                jogo.data_jogo,
                jogo.horario.strftime("%H:%M:%S"),
                jogo.time_a,
                jogo.time_b,
                jogo.status.value,
                jogo.resultado_final.value if jogo.resultado_final else None,
                jogo.pontos_time_a,
                jogo.pontos_empate,
                jogo.pontos_time_b,
                jogo.id_jogo,
            ),
        )
        self._conn.commit()
        return jogo

    def buscar_por_id(self, id_jogo: int) -> Jogo | None:
        cursor = self._conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM jogos WHERE id_jogo = %s", (id_jogo,))
        row = cursor.fetchone()
        return self._row_para_jogo(row) if row else None

    def listar_por_data(self, data: date) -> list[Jogo]:
        cursor = self._conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM jogos WHERE data_jogo = %s ORDER BY horario",
            (data,),
        )
        return [self._row_para_jogo(r) for r in cursor.fetchall()]

    def listar_todos(self) -> list[Jogo]:
        cursor = self._conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM jogos ORDER BY data_jogo, horario")
        return [self._row_para_jogo(r) for r in cursor.fetchall()]

    @staticmethod
    def _row_para_jogo(row: dict) -> Jogo:
        horario = row["horario"]
        # mysql-connector retorna timedelta para TIME
        if hasattr(horario, "seconds"):
            total = int(horario.total_seconds())
            horario = time(total // 3600, (total % 3600) // 60, total % 60)

        return Jogo(
            id_jogo=row["id_jogo"],
            fase=FaseJogo(row["fase"]),
            data_jogo=row["data_jogo"] if isinstance(row["data_jogo"], date) else row["data_jogo"].date(),
            horario=horario,
            time_a=row["time_a"],
            time_b=row["time_b"],
            status=StatusJogo(row["status"]),
            resultado_final=ResultadoFinal(row["resultado_final"]) if row["resultado_final"] else None,
            pontos_time_a=row["pontos_time_a"],
            pontos_empate=row["pontos_empate"],
            pontos_time_b=row["pontos_time_b"],
        )

#Repositório de Palpites
class RepositorioPalpiteMySQL(RepositorioPalpite):

    def __init__(self, conn: MySQLConnection):
        self._conn = conn

    def salvar(self, palpite: Palpite) -> Palpite:
        cursor = self._conn.cursor()
        cursor.execute(
            """
            INSERT INTO palpites (id_usuario, id_jogo, escolha)
            VALUES (%s, %s, %s)
            """,
            (palpite.id_usuario, palpite.id_jogo, palpite.escolha.value),
        )
        self._conn.commit()
        palpite.id_palpite = cursor.lastrowid
        return palpite

    def atualizar(self, palpite: Palpite) -> Palpite:
        cursor = self._conn.cursor()
        cursor.execute(
            """
            UPDATE palpites
            SET escolha = %s, acertou = %s, pontos_ganhos = %s
            WHERE id_palpite = %s
            """,
            (
                palpite.escolha.value,
                palpite.acertou,
                palpite.pontos_ganhos,
                palpite.id_palpite,
            ),
        )
        self._conn.commit()
        return palpite

    def buscar_por_id(self, id_palpite: int) -> Palpite | None:
        cursor = self._conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM palpites WHERE id_palpite = %s", (id_palpite,))
        row = cursor.fetchone()
        return self._row_para_palpite(row) if row else None

    def buscar_por_usuario_e_jogo(self, id_usuario: int, id_jogo: int) -> Palpite | None:
        cursor = self._conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM palpites WHERE id_usuario = %s AND id_jogo = %s",
            (id_usuario, id_jogo),
        )
        row = cursor.fetchone()
        return self._row_para_palpite(row) if row else None

    def listar_por_usuario(self, id_usuario: int) -> list[Palpite]:
        cursor = self._conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM palpites WHERE id_usuario = %s ORDER BY data_palpite DESC",
            (id_usuario,),
        )
        return [self._row_para_palpite(r) for r in cursor.fetchall()]

    def listar_por_jogo(self, id_jogo: int) -> list[Palpite]:
        cursor = self._conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM palpites WHERE id_jogo = %s",
            (id_jogo,),
        )
        return [self._row_para_palpite(r) for r in cursor.fetchall()]

    def listar_todos(self) -> list[Palpite]:
        cursor = self._conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM palpites ORDER BY data_palpite DESC")
        return [self._row_para_palpite(r) for r in cursor.fetchall()]

    @staticmethod
    def _row_para_palpite(row: dict) -> Palpite:
        return Palpite(
            id_palpite=row["id_palpite"],
            id_usuario=row["id_usuario"],
            id_jogo=row["id_jogo"],
            escolha=EscolhaPalpite(row["escolha"]),
            data_palpite=row["data_palpite"] if isinstance(row["data_palpite"], datetime) else datetime.utcnow(),
            acertou=row["acertou"],
            pontos_ganhos=row["pontos_ganhos"] or 0,
        )