from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from model.produto import ProdutoModel


class ProdutoSchema(BaseModel):
    """ Define como um novo produto a ser inserido deve ser representado
    """
    produto: str 
    qtde: Optional[int] 
    un: str 
    vl_unit: float 
    vl_total: float 

class ListagemProdutosSchema(BaseModel):
    """ Define como uma listagem de produtos será retornada.
    """
    produtos:List[ProdutoSchema]


def apresenta_produtos(produtos: List[ProdutoModel], token: str) -> Dict[str, Any]:
    """ Retorna uma representação do produto seguindo o schema definido em
        ProdutoViewSchema, além de exigir um token de autenticação.
    """
    result = []
    for produto in produtos:
        result.append({
            "produto": produto.produto,
            "qtde": produto.qtde,
            "un": produto.un,
            "vl_unit": produto.vl_unit,
            "vl_total": produto.vl_total,
        })

    return {"produtos": result, "token": token}

def apresenta_produto(produto: ProdutoModel):
    """ Retorna uma representação do produto seguindo o schema definido em
        ProdutoViewSchema.
    """
    return {
       "produto": produto.produto,
        "qtde": produto.qtde,
        "un": produto.un,
        "vl_unit": produto.vl_unit,
        "vl_total": produto.vl_total,
    }
    
class ProdutoViewSchema(BaseModel):
    """ Define como um produto será retornado: produto 
    """
    produto_id: int = 99999
    produto: str = "Macarrão"
    qtde: Optional[int] = 1
    un: str = "UN"
    vl_unit: float = 7.50
    vl_total: float = 7.50
    
    
    




