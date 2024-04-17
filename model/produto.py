from sql_alchemy import banco


class ProdutoModel(banco.Model):
    __tablename__ = 'produtos'

    produto_id = banco.Column(banco.Integer, primary_key=True)
    produto = banco.Column(banco.String(40), nullable=False)
    qtde = banco.Column(banco.Float, nullable=False)
    un = banco.Column(banco.String(2), nullable=False)
    vl_unit = banco.Column(banco.Float, nullable=False)
    vl_total = banco.Column(banco.Float, nullable=False)
    
    def __init__(self, produto, qtde, un, vl_unit, vl_total):
        self.produto = produto
        self.qtde = qtde
        self.un = un
        self.vl_unit = vl_unit
        self.vl_total = vl_total
      
    def json(self):
        return {
            'produto_id': self.produto_id,
            'produto': self.produto,
            'qtde': self.qtde,
            'un': self.un,
            'vl_unit': self.vl_unit,
            'vl_total': self.vl_total
            }

    @classmethod
    def find_produto(cls, produto_id):
        produto = cls.query.filter_by(produto_id=produto_id).first()
        if produto:
            return produto
        return None

    @classmethod
    def find_by_produto(cls, produto):
        produto = cls.query.filter_by(produto=produto).first()
        if produto:
            return produto
        return None

    def save_produto(self):
        banco.session.add(self)
        banco.session.commit()

    def delete_produto(self):
        banco.session.delete(self)
        banco.session.commit()
