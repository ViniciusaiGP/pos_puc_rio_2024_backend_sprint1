from pydantic import BaseModel


class ErrorSchema(BaseModel):
    """ Define como um modelo de retorno de mensagem de erro genérica.
    """
    message: str

class ErrorAuthorizationSchema(BaseModel):
    """ Define como sera a mensagem de erro 401.
    """
    msg: str = "Missing Authorization Header"

class ServerErrorSchema(BaseModel):
    """ Define como sera a mensagem de erro 500.
    """
    message: str = "Server error"