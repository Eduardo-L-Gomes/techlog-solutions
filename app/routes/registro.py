from fastapi import APIRouter, Form, Depends, HTTPException, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from typing import Annotated
from dotenv import load_dotenv
import os
from app.models.usuario import UsuarioCriarAtualizar

from app.models.cliente import Cliente, ClienteCriarAtualizar
from app.db_local.cliente_repositorio import ClientRepository
from app.db_local.usuario_repositorio import UserRepository
from app.dependencies import obter_cliente_repositorio, obter_usuario_repositorio

load_dotenv()

router = APIRouter(
    prefix="/registro"
)

templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
async def pagina_registro(request: Request):
    return templates.TemplateResponse(request=request, name="registro.html", context={"request": request})

@router.post("/")
async def registrar_usuario(
    usuario_repositorio: Annotated[UserRepository, Depends(obter_usuario_repositorio)],
    request: Request,
    nome = Form(...),
    email = Form(...),
    senha = Form(...),
    confirma_senha = Form(...),
):

    data = {
        "nome": nome,
        "email": email,
        "senha": senha,
        "confirma_senha": confirma_senha,
    }

    if not all([email, senha, nome, confirma_senha]):
        return templates.TemplateResponse(name="registro.html", request=request, context={"error": "Campos obrigatórios faltantes", **data})

    usuario_existente = await usuario_repositorio.buscar_usuario_por_email(email)
    if usuario_existente:
        return templates.TemplateResponse(name="registro.html", request=request, context={"error": "Usuario inválido", **data})
    
    usuario_criar = UsuarioCriarAtualizar(nome=nome, email=email, senha=senha)

    usuario = await usuario_repositorio.criar_usuario(usuario_criar)

    if usuario:
        response = RedirectResponse(url="/login", status_code=303)
        return response

    return templates.TemplateResponse(name="registro.html", request=request, context={"error": "Não foi possível criar o usuário, tente novamente mais tarde.", **data})