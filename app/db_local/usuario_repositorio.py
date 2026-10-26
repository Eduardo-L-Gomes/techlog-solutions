from app.db_local.local import DBLocal
from app.models.usuario import Usuario, UsuarioCriarAtualizar

class UserRepository:
    def __init__(self, banco_de_dados: DBLocal):
        self.bd = banco_de_dados

    async def buscar_usuario_por_email_senha(self, email: str, senha: str) -> Usuario | None:
        with self.bd.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, nome, email, senha FROM clientes WHERE email = ? AND senha = ?", (email, senha,))
            linha = cursor.fetchone()

            if linha:
                return Usuario(id_=linha[0], nome=linha[1], email=linha[2], senha=linha[3])
            
            return None

    async def buscar_usuario_por_email(self, email) -> Usuario | None:
        with self.bd.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, nome, email FROM clientes WHERE email = ?", (email,))
            linha = cursor.fetchone()

            if linha:
                return Usuario(id_=linha[0], nome=linha[1], email=linha[2], senha=linha[3])
            
            return None        

    async def criar_usuario(self, usuario_criar: UsuarioCriarAtualizar) -> Usuario:
        with self.bd.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)", (usuario_criar.nome, usuario_criar.email, usuario_criar.senha))
            id_ = cursor.lastrowid
            return Usuario(id_=id_, nome=usuario_criar.nome, email=usuario_criar.email, senha=usuario_criar.senha)
            