from pydantic import BaseModel
#Mateus Zancheta Falcão

class Cliente(BaseModel):
    id_cliente: int = None
    nome: str
    cpf: str
    telefone: str