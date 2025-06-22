import db
from infra.orm.FuncionarioModel import FuncionarioDB
from fastapi import APIRouter, Depends, HTTPException
from domain.entities.Funcionario import Funcionario, LoginFuncionario
from typing import Annotated
from fastapi.responses import JSONResponse
from security import get_current_active_user, User
from sqlalchemy.orm import Session
import bcrypt

router = APIRouter()  # Sem dependência global aqui

# --- Rotas CRUD Funcionário ---

@router.get("/funcionario/", tags=["Funcionário"], dependencies=[Depends(get_current_active_user)])
async def get_funcionarios(current_user: Annotated[User, Depends(get_current_active_user)]):
    try:
        session = db.Session()
        dados = session.query(FuncionarioDB).all()
        return dados, 200
    except Exception as e:
        return {"erro": str(e)}, 400
    finally:
        session.close()

@router.get("/funcionario/{id}", tags=["Funcionário"])
async def get_funcionario(id: int):
    try:
        session = db.Session()
        dados = session.query(FuncionarioDB).filter(FuncionarioDB.id_funcionario == id).first()

        if not dados:
            raise HTTPException(status_code=404, detail="Funcionário não encontrado")

        return dados  # FastAPI vai serializar o SQLAlchemy model automaticamente (se estiver correto)

    except HTTPException as e:
        raise e
    except Exception as e:
        return JSONResponse(status_code=500, content={"erro": str(e)})
    finally:
        session.close()

@router.post("/funcionario/", tags=["Funcionário"], dependencies=[Depends(get_current_active_user)])
async def post_funcionario(corpo: Funcionario):
    try:
        session = db.Session()
        # Hash da senha antes de salvar
        hashed_senha = bcrypt.hashpw(corpo.senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        dados = FuncionarioDB(
            None, corpo.nome, corpo.matricula,
            corpo.cpf, corpo.telefone or "", corpo.grupo, hashed_senha
        )
        session.add(dados)
        session.commit()
        return {"id": dados.id_funcionario}, 200
    except Exception as e:
        session.rollback()
        return {"erro": str(e)}, 400
    finally:
        session.close()

@router.put("/funcionario/{id}", tags=["Funcionário"], dependencies=[Depends(get_current_active_user)])
async def put_funcionario(id: int, corpo: Funcionario):
    try:
        session = db.Session()
        dados = session.query(FuncionarioDB).filter(FuncionarioDB.id_funcionario == id).first()
        if not dados:
            raise HTTPException(status_code=404, detail="Funcionário não encontrado")

        dados.nome = corpo.nome
        dados.matricula = corpo.matricula
        dados.cpf = corpo.cpf
        dados.telefone = corpo.telefone or ""
        dados.grupo = corpo.grupo

        # Se senha foi enviada, atualiza com hash, senão mantém a atual
        if corpo.senha:
            dados.senha = bcrypt.hashpw(corpo.senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        session.add(dados)
        session.commit()
        return {"id": dados.id_funcionario}, 200
    except HTTPException as e:
        raise e
    except Exception as e:
        session.rollback()
        return {"erro": str(e)}, 400
    finally:
        session.close()

@router.delete("/funcionario/{id}", tags=["Funcionário"], dependencies=[Depends(get_current_active_user)])
async def delete_funcionario(id: int):
    try:
        session = db.Session()
        dados = session.query(FuncionarioDB).filter(FuncionarioDB.id_funcionario == id).first()
        if not dados:
            raise HTTPException(status_code=404, detail="Funcionário não encontrado")

        session.delete(dados)
        session.commit()
        return {"id": dados.id_funcionario}, 200
    except HTTPException as e:
        raise e
    except Exception as e:
        session.rollback()
        return {"erro": str(e)}, 400
    finally:
        session.close()

# --- Rota de Login (SEM autenticação requerida) ---

@router.post("/funcionario/login/", tags=["Funcionário - Login"])
async def login_funcionario(corpo: LoginFuncionario):
    try:
        session = db.Session()
        dados = session.query(FuncionarioDB).filter(FuncionarioDB.cpf == corpo.cpf).one()

        if not bcrypt.checkpw(corpo.senha.encode('utf-8'), dados.senha.encode('utf-8')):
            return JSONResponse(status_code=401, content={"erro": "Senha incorreta"})

        return JSONResponse(
            status_code=200,
            content={
                "id_funcionario": dados.id_funcionario,
                "nome": dados.nome,
                "cpf": dados.cpf,
                "grupo": dados.grupo
            }
        )
    except Exception as e:
        return JSONResponse(status_code=400, content={"erro": str(e)})
    finally:
        session.close()