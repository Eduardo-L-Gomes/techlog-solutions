from app.db_local.local import DBLocal
from app.models.usuario import Usuario

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