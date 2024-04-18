# Implementação QRCode

Este projeto é uma implementação inicial de um sistema de gerenciamento de estoque com leitura de QRCode gerada pelas compras de mercado. Ele fornece uma API RESTful construída com Flask, Flask-RESTful e Flask-JWT-Extended.

## Descrição

Este sistema foi desenvolvido para ajudar pessoas a gerenciar seu estoque de forma eficiente, permitindo a criação de produtos, a listagem de usuários, a autenticação de usuários e a leitura de notas fiscais eletrônicas a partir de uma URL.


## Requisitos

Primeiro vamos criar um ambiente virtual para fazer a instalação das bibliotecas.

Windows:
`python -m venv venv`
No macOS e Linux:
`python3 -m venv venv`

Após executar o comando, uma nova pasta com o nome do ambiente virtual será criada no diretório atual.
Ative o ambiente virtual. Isso é feito executando um script específico dependendo do seu sistema operacional.

Windows:
`venv\Scripts\activate`
No macOS e Linux:
`source venv/bin/activate`

Ao fazer isso, você notará que o prompt do terminal será prefixado com o nome do seu ambiente virtual, indicando que está ativo.

Certifique-se de ter o Python instalado em sua máquina. Você pode instalar as dependências do projeto executando:

`pip install -r requirements.txt`

## Configuração

O projeto utiliza um banco de dados SQLite, então não há necessidade de configurações adicionais. Porém, para uso em produção, recomenda-se alterar para um banco de dados mais robusto, como PostgreSQL ou MySQL.

## Funcionalidades

 - Primeiramente execute o `POST /registrar` para criar o usuario de conexão modelo.
 - Adicione o `TOKEN` no Authorize, ao fazer isso vc tem acesso a todas as funcionalidades.

### Produtos

- `GET /produtos`: Retorna uma lista de todos os produtos cadastrados.
- `POST /produto`: Cria um novo produto.

### Usuários

- `POST /registrar`: Cria um novo usuário.
- `POST /login`: Realiza a autenticação do usuário e fornece um token de acesso.
- `POST /logout`: Desconecta o usuário e adiciona o token à lista negra.

### Nota Fiscal

- `POST /nota_url`: Realiza a leitura de uma nota fiscal eletrônica a partir de uma URL.

## Documentação

A documentação da API pode ser encontrada em `/openapi/swagger`, onde você pode explorar todas as rotas disponíveis.

## Executando o projeto

Para iniciar o servidor de desenvolvimento, execute:

`python app.py`

O servidor será iniciado em `http://localhost:5000`.
