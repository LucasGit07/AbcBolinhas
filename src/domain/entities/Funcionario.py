from pydantic import BaseModel
#Mateus Zancheta Falcão

class Funcionario(BaseModel):
    id_funcionario: int = None
    nome: str
    matricula: str
    cpf: str
    telefone: str = None
    grupo: int
    senha: str = None
    
class LoginFuncionario(BaseModel):
    cpf: str
    senha: str
