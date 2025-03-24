from pydantic import BaseModel
from datetime import date

class Comanda(BaseModel):
    id_comanda: int = None
    comanda: str
    data_hora: date
    status: int
    cliente_id: int = None
    funcionario_id: int

class ComandaProdutos(BaseModel):
    id_comanda_produto: int = None
    comanda_id: int
    produto_id: int
    funcionario_id: int
    quantidade: int
    valor_unitario: float