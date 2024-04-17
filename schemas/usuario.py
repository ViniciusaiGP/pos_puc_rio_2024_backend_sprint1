from typing import List
from pydantic import BaseModel


class LoginSchema(BaseModel):
    """ Define como é a conexão de exemplo de usuário.
    """
    login: str = "teste"
    senha: str = "1234"

class LoginRepSchema(BaseModel):
    """ Define como é a conexão de exemplo de usuário.
    """
    access_token: str 
    login: str
    

class RegisterSchema(BaseModel):
    """ Define como um novo usuário será criado.
    """
    login: str = "teste"
    senha: str = "1234"
    email: str =  "teste@teste.com"
    

class ListagemUsuariosSchema(BaseModel):
    """ Define como uma listagem de usuários será retornada.
    """
    Users:List[LoginRepSchema]

class LogoutSchema(BaseModel):
    """ Retorno do logout do usuário.
    """
    message: str 
    