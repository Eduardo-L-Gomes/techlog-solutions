from app.db_local.local import DBLocal
from app.models.cliente import Cliente, ClienteCriarAtualizar

class ClientRepository:
    def __init__(self, banco_de_dados: DBLocal):
        self.bd = banco_de_dados

    async def listar_clientes(self) -> list[Cliente]:
        with self.bd.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, nome, email, telefone FROM clientes")
            linhas = cursor.fetchall()
            clientes = [
                Cliente(id_=linha[0], nome=linha[1], email=linha[2], telefone=linha[3])
                for linha in linhas
            ]
            return clientes

    async def obter_cliente(self, cliente_id: int) -> Cliente | None:
        with self.bd.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, nome, email, telefone FROM clientes WHERE id = ?", (cliente_id,)
            )
            linha = cursor.fetchone()
            if linha:
                return Cliente(id_=linha[0], nome=linha[1], email=linha[2], telefone=linha[3])
            return None

    async def criar_cliente(self, cliente: ClienteCriarAtualizar) -> Cliente:
        with self.bd.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO clientes (nome, email, telefone) VALUES (?,?,?)", 
                (cliente.nome, cliente.email, cliente.telefone,)
            )
            client_id = cursor.lastrowid
            return Cliente(id_=client_id, nome=cliente.nome, email=cliente.email, telefone=cliente.telefone)

    async def atualizar_cliente(self, cliente_id:int, cliente: ClienteCriarAtualizar) -> Cliente | None:
        with self.bd.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE clientes SET nome = ?, email = ?, telefone = ? WHERE id = ?",
                (cliente.nome, cliente.email, cliente.telefone, cliente_id,)
            )
            if cursor.rowcount == 0:
                return None
            return Cliente(id_=cliente_id, nome=cliente.nome, email=cliente.email, telefone=cliente.telefone)

    async def deletar_cliente(self, cliente_id: int) -> bool | None:
        with self.bd.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM clientes WHERE id = ?",
                (cliente_id,)
            )
            if cursor.rowcount < 0:
                return None
            return cursor.rowcount > 0