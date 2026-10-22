from fastapi import APIRouter, Form, Depends, HTTPException, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from typing import Annotated
from dotenv import load_dotenv
import os

from app.models.cliente import Cliente, ClienteCriarAtualizar
from app.db_local.cliente_repositorio import ClientRepository
from app.dependencies import obter_cliente_repositorio

load_dotenv()

router = APIRouter(
    prefix="/login"
)

email_login = os.getenv("EMAIL_LOGIN")
senha_login = os.getenv("SENHA_LOGIN")

templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
async def pagina_login(request:Request):
    return templates.TemplateResponse(request=request, name="login.html", context={"request": request})

@router.post("/")
async def login(request: Request, email = Form(...), senha = Form(...)):
    
    if email == email_login and senha == senha_login:
        response = RedirectResponse("/", status_code=303)
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