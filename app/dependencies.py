from fastapi import Depends
from typing import Annotated

from app.db_local.local import DBLocal
from app.db_local.cliente_repositorio import ClientRepository
from app.db_local.usuario_repositorio import UserRepository

db = DBLocal()

def obter_banco_de_dados() -> DBLocal:
    return db

def obter_cliente_repositorio(
        db_local: Annotated[DBLocal, 
                            Depends(obter_banco_de_dados)]
    ) -> ClientRepository:
    return ClientRepository(db_local)

def obter_usuario_repositorio(
        db_local: Annotated[DBLocal,
                            Depends(obter_banco_de_dados)]
    ) -> UserRepository:
    return UserRepository(db_local)