from pydantic import BaseModel
from typing import List


class NotaSchema(BaseModel):
    """ Exemplo de nota url
    """
    nota_url: str = "http://www.fazenda.pr.gov.br/nfce/qrcode?p=41240411517841002211650050003017141734260606|2|1|2|6E4A8B1F83EAE8EEC741FF1A8AEBB913FD6D9688" 
    
class Item(BaseModel):
    """ Item de montagem para a lista.
    """
    Produto: str
    Qtde: int
    UN: str
    Vl_Total: float
    Vl_Unit: float

class InformacoesPagamento(BaseModel):
    """ Montagem do modo de pagamento.
    """
    Forma_de_pagamento: str
    Valor_total_pago: float 

class Empresa(BaseModel):
    """ Montagem da informação de compra da empresa.
    """
    CNPJ: str
    Endereco: str
    Nome_da_Empresa: str

class ListagemNotaSchema(BaseModel):
    """ Define como uma listagem de usuários será retornada.
    """
    Empresa: Empresa
    Informacoes_de_Pagamento: InformacoesPagamento
    Itens: List[Item]
