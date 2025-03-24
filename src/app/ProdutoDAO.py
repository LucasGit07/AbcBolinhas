import db
from infra.orm.ProdutoModel import ProdutoDB
from fastapi import APIRouter
from domain.entities.Produto import Produto
from typing import Annotated
from fastapi import Depends
from security import get_current_active_user, User

router = APIRouter(dependencies=[Depends(get_current_active_user)])
#Mateus Zancheta Falcão

# Criar as rotas/endpoints: GET, POST, PUT, DELETE

@router.get("/produto/", tags=["Produto"], dependencies=[Depends(get_current_active_user)], )
async def get_produto( current_user:Annotated[User, Depends(get_current_active_user)], ):
    try:
        session = db.Session()

        dados = session.query(ProdutoDB).all()

        print(current_user)
        
        return dados, 200
    
    except Exception as e:
        return {"erro": str(e)}, 400
    finally:
        session.close()

@router.get("/produto/{id}", tags=["Produto"])
async def get_produto(id: int):
    try:
        session = db.Session()

        dados = session.query(ProdutoDB).filter(ProdutoDB.id_produto == id).all()
        return dados, 200
    
    except Exception as e:
        return {"erro": str(e)}, 400
    finally:
        session.close()

@router.post("/produto/", tags=["Produto"])
async def post_produto(corpo: Produto):
    try:
        session = db.Session()

        dados = ProdutoDB(None, corpo.nome, corpo.descricao,
                              corpo.foto, corpo.valor_unitario)

        session.add(dados)
        # session.flush()
        session.commit()

        return {"id": dados.id_produto}, 200

    except Exception as e:
        session.rollback()
        return {"erro": str(e)}, 400
    finally:
        session.close()

@router.put("/produto/{id}", tags=["Produto"])
async def put_produto(id: int, corpo: Produto):
    try:
        session = db.Session()

        dados = session.query(ProdutoDB).filter(ProdutoDB.id_produto == id).one()
        
        dados.nome = corpo.nome
        dados.descricao = corpo.descricao
        dados.foto = corpo.foto
        dados.valor_unitario = corpo.valor_unitario

        session.add(dados)
        session.commit()

        return {"id": dados.id_produto}, 200
    
    except Exception as e:
        session.rollback()
        return {"erro": str(e)}, 400
    finally:
        session.close()

@router.delete("/produto/{id}", tags=["Produto"])
async def delete_produto(id: int):
    try:
        session = db.Session()
        
        dados = session.query(ProdutoDB).filter(ProdutoDB.id_produto == id).one()
        
        session.delete(dados)
        session.commit()
        
        return {"id": dados.id_produto}, 200
    
    except Exception as e:
        session.rollback()
        return {"erro": str(e)}, 400
    finally:
        session.close()