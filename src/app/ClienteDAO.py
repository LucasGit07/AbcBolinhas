import db
from infra.orm.ClienteModel import ClienteDB
from fastapi import APIRouter
from domain.entities.Cliente import Cliente
from typing import Annotated
from fastapi import Depends
from security import get_current_active_user, User

router = APIRouter(dependencies=[Depends(get_current_active_user)])
#Mateus Zancheta Falcão

# Criar as rotas/endpoints: GET, POST, PUT, DELETE

@router.get("/cliente/", tags=["Cliente"], dependencies=[Depends(get_current_active_user)], )
async def get_cliente( current_user:Annotated[User, Depends(get_current_active_user)], ):
    try:
        session = db.Session()
       
        dados = session.query(ClienteDB).all()

        print(current_user)
        
        return dados, 200
    
    except Exception as e:
        return {"erro": str(e)}, 400
    finally:
        session.close()

@router.get("/cliente/{id}", tags=["Cliente"])
async def get_cliente(id: int):
    try:
        session = db.Session()
       
        dados = session.query(ClienteDB).filter(ClienteDB.id_cliente == id).all()
        return dados, 200
    
    except Exception as e:
        return {"erro": str(e)}, 400
    finally:
        session.close()

@router.post("/cliente/", tags=["Cliente"])
async def post_cliente(corpo: Cliente):
    try:
        session = db.Session()

        dados = ClienteDB(None, corpo.nome, corpo.cpf, corpo.telefone)

        session.add(dados)
        # session.flush()
        session.commit()

        return {"id": dados.id_cliente}, 200

    except Exception as e:
        session.rollback()
        return {"erro": str(e)}, 400
    finally:
        session.close()

@router.put("/cliente/{id}", tags=["Cliente"])
async def put_cliente(id: int, corpo: Cliente):
    try:
        session = db.Session()

        dados = session.query(ClienteDB).filter(ClienteDB.id_cliente == id).one()
        
        dados.nome = corpo.nome
        dados.cpf = corpo.cpf
        dados.telefone = corpo.telefone

        session.add(dados)
        session.commit()

        return {"id": dados.id_cliente}, 200
    
    except Exception as e:
        session.rollback()
        return {"erro": str(e)}, 400
    finally:
        session.close()

@router.delete("/cliente/{id}", tags=["Cliente"])
async def delete_cliente(id: int):
    try:
        session = db.Session()
        
        dados = session.query(ClienteDB).filter(ClienteDB.id_cliente == id).one()
        
        session.delete(dados)
        session.commit()
        
        return {"id": dados.id_cliente}, 200
    
    except Exception as e:
        session.rollback()
        return {"erro": str(e)}, 400
    finally:
        session.close()

@router.get("/cliente/cpf/{cpf}", tags=["Cliente - Valida CPF"])
async def cpf_cliente(cpf: str):
    try:
        session = db.Session()
        
        dados = session.query(ClienteDB).filter(ClienteDB.cpf == cpf).all()
        return dados, 200
    
    except Exception as e:
        return {"erro": str(e)}, 400
    finally:
        session.close()