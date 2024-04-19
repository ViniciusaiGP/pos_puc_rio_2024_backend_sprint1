from datetime import timedelta
import traceback

from flask import jsonify, redirect
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, get_jwt, jwt_required
from flask_openapi3 import OpenAPI, Info, Tag
from flask_restful import Api, reqparse

from blacklist import BLACKLIST
from model.produto import ProdutoModel
from model.usuario import UserModel
from schemas.error import ErrorAuthorizationSchema, ErrorSchema, ServerErrorSchema
from schemas.nota import ListagemNotaSchema, NotaSchema
from schemas.produto import ListagemProdutosSchema, ProdutoViewSchema 
from schemas.usuario import ListagemUsuariosSchema, LoginRepSchema, LoginSchema, LogoutSchema, RegisterSchema
from services.nota_fiscal_eletronica import NotaFiscalExtractor

info = Info(title= "Implementação QRCode", 
            description= '''Essa implementação é a ideia inicial de criar um gererenciamento de stock com Leitura de QRCode gerada pelas comprar de mercado.
                            \n\n\nAo iniciar o projeto efeitue a criação do usuario caso não tenha e se tiver use para gerar sua chave de acesso(*TOKEN*) para poder utilizar a aplicação.''', 
            version="1.0.0")
app = OpenAPI(__name__, info=info)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'grytkRF325Fss'
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=1)

api = Api(app)
jwt = JWTManager(app)
CORS(app) 

@app.before_request
def cria_banco():
    banco.create_all()

@jwt.token_in_blocklist_loader
def verifica_blacklist(self, token):
    return token['jti'] in BLACKLIST

@jwt.revoked_token_loader
def token_de_acesso_invalidado(jwt_header, jwt_payload):
    return jsonify({'mesage': 'Você foi desconectado.'}), 401

home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger")
produto_tag = Tag(name="Produto", description="Rotas para Produtos")
auth_tag = Tag(name="Autentificação", description="Rotas para Autentificação")
usuario_tag = Tag(name="Usuário", description="Rotas para Usuário")
nota_tag = Tag(name="Nota fiscal", description="Rota para trazer a informação da nota fiscal")

security_scheme = {
    "Bearer Token": {
        "type": "http",
        "scheme": "bearer",
        "bearerFormat": "JWT"
    }
}
app.security_schemes = security_scheme

@app.get('/', tags=[home_tag])
def home():
    """ Home da aplicação.

        Redireciona para /openapi/swagger, abrindo a documentação da API.
    """
    return redirect('/openapi/swagger')

@app.get('/produtos', tags=[produto_tag], responses={"200" : ListagemProdutosSchema, "400":ErrorSchema, "401": ErrorAuthorizationSchema, "500":ErrorSchema}, security=[{"Bearer Token": []}])
@jwt_required()
def get_produtos():
    """ Faz a busca por todos os Produto cadastrados.

        Retorna uma lista de listagem de produtos.
    """
    try:
        produtos = ProdutoModel.query.all()
        return {'Produtos': [produto.json() for produto in produtos]}
    except Exception as e:
        traceback.print_exc()
        return {'mesage': 'Ocorreu um erro ao buscar produtos.'}, 500

@app.post('/produto', tags=[produto_tag], responses={"201": ListagemProdutosSchema, "400":ErrorSchema, "401": ErrorAuthorizationSchema, "500":ErrorSchema}, security=[{"Bearer Token": []}])
@jwt_required()
def post_produto(body:ProdutoViewSchema):
    """ Cria um novo produto.

        Cria um novo produto se tiver chave de acesso.
    """
    atributos = reqparse.RequestParser()
    atributos.add_argument('produto', type=str, required=True)
    atributos.add_argument('qtde', type=str, required=True)
    atributos.add_argument('un', type=str, required=True)
    atributos.add_argument('vl_unit', type=str, required=True)
    atributos.add_argument('vl_total', type=str, required=True)
    data = atributos.parse_args()
    
    produto = ProdutoModel(**data)

    try:
        produto.save_produto()
    except:
        traceback.print_exc()
        return {"message": "Um erro ocorreu ao tentar salvar o produto."}, 500

    return produto.json(), 201

@app.get('/usuarios', tags=[usuario_tag], responses={"200": ListagemUsuariosSchema, "400": ErrorSchema, "401": ErrorAuthorizationSchema, "500": ServerErrorSchema}, security=[{"Bearer Token": []}])
@jwt_required()
def get_users():
    """ Lista de usuários.

        Traz todos os usuários se tiver a chave de acesso.
    """
    try:
        users = [users.json() for users in UserModel.query.all()]
        return {'Users': users}, 200
    except:
        return {'error': 'Server error'}, 500

@app.post('/registrar', tags=[usuario_tag])
def post_usuario_novo(body:RegisterSchema):
    """ Cria um novo usuário.

        Cria um usuário caso tenha a chave de acesso.
    """
    atributos = reqparse.RequestParser()
    atributos.add_argument('login', type=str, required=True)
    atributos.add_argument('senha', type=str, required=True)
    atributos.add_argument('email', type=str, required=True)
    atributos.add_argument('ativado', type=bool)
    dados = atributos.parse_args()

    if not dados['email'] or dados['email'] is None:
        return {"mesage": "O campo 'email' precisa estar preenchido."}, 400
    
    if UserModel.find_by_email(dados['email']):
        return {"mesage": "O email '{}' já existe.".format(dados['email'])}, 400

    if UserModel.find_by_login(dados['login']):
        return {"mesage": "O login '{}' já existe.".format(dados['login'])}, 400

    user = UserModel(**dados)
    user.ativado = True 
    try:
        user.save_user()
    except:
        user.delete_user()
        traceback.print_exc()
        return {"mesage": "Um erro aconteceu."}, 500 
    
    token_de_acesso = create_access_token(identity=user.user_id)
    return {
            'mesage': 'Usuário criado com sucesso!',
            'access_token': token_de_acesso,
            'login':dados['login']
            }, 201 # Created

@app.post('/login', tags=[auth_tag], responses={"200": LoginRepSchema, "400": ErrorSchema, "500":ServerErrorSchema})
def post_login(body:LoginSchema):
    """ Autentificação para o usuário.

        Está sendo usado o JWT para a segurança dos endpoints, o retorno será um token e o login.
    """
    atributos = reqparse.RequestParser()
    atributos.add_argument('login', type=str, required=True)
    atributos.add_argument('senha', type=str, required=True)
    dados = atributos.parse_args()

    user = UserModel.find_by_login(dados['login'])
    
    if user and user.senha == dados['senha']:
        if user.ativado:
            token_de_acesso = create_access_token(identity=user.user_id)
            return {
                    'login': dados['login'],
                    'access_token': token_de_acesso
                    }, 200
        return {'mesage' : 'Usuário não confirmado.'}, 400
    return {'message': 'Não existe esse usuário, faça o cadastro.'}, 400 


@app.post('/logout', tags=[auth_tag], responses={"200": LogoutSchema,"500":ServerErrorSchema}, security=[{"Bearer Token": []}])
@jwt_required()
def post_logout():
    """ Desconecta o usuário.

        Adiciona na blacklist o token do usuário conectado e faz com que ele seja impossibilitado de usar novamente.
    """
    try:
        jwt_id = get_jwt()['jti']
        BLACKLIST.add(jwt_id)
        return {'mesage': 'Saiu com sucesso!'}, 200
    except: {'mesage': 'Server error'}, 500

@app.post('/nota_url', tags=[nota_tag], responses={"201": ListagemNotaSchema, "400": ErrorSchema, "401": ErrorAuthorizationSchema, "500":ServerErrorSchema}, security=[{"Bearer Token": []}])
@jwt_required()
def post_nota(body:NotaSchema):
    atributos = reqparse.RequestParser()
    atributos.add_argument('nota_url', type=str, required=True)
    dados = atributos.parse_args()

    if not dados['nota_url'] or dados['nota_url'] is None:
        return {"mesage": "O campo 'nota_url' precisa estar preenchido."}, 400

    try:
        nota_fiscal_extractor = NotaFiscalExtractor(url=dados['nota_url'])
        
        return jsonify(nota_fiscal_extractor.extract()), 200
    except Exception as e:
        return {'mesage': 'Ocorreu um erro na leitura'}, 500

if __name__ == '__main__':
    from sql_alchemy import banco
    banco.init_app(app)
    app.run(debug=True)
