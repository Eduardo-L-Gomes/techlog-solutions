from fastapi import APIRouter, Form, Depends, HTTPException, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from typing import Annotated
from dotenv import load_dotenv
import os

from app.models.cliente import Cliente, ClienteCriarAtualizar
from app.db_local.cliente_repositorio import ClientRepository
from app.db_local.usuario_repositorio import UserRepository
from app.dependencies import obter_cliente_repositorio, obter_usuario_repositorio

load_dotenv()

router = APIRouter(
    prefix="/login"
)

templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
async def pagina_login(request:Request):
    return templates.TemplateResponse(request=request, name="login.html", context={"request": request})

@router.post("/")
async def login(usuario_repositorio: Annotated[UserRepository, Depends(obter_usuario_repositorio)],
                request: Request, 
                email = Form(...), 
                senha = Form(...)):

    usuario = await usuario_repositorio.buscar_usuario_por_email_senha(email, senha)
    if usuario:
        response = RedirectResponse(url="/", status_code=303)
        response.set_cookie(key="session_token", value="token-senha", httponly=True)

        return response

    return templates.TemplateResponse(request=request, name="login.html", context={
        "request": request,
        "email": email,
        "senha": senha,
        "error": "Credenciais invalidas"
    })

@router.post("/logout")
async def logout(request: Request):
    pass