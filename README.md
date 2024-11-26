
# Microblog

## Descrição

O **Microblog** é uma aplicação web desenvolvida com **Django** e **Django REST Framework**, oferecendo funcionalidades como criação de postagens, comentários, curtidas e gerenciamento de seguidores. A aplicação é projetada para facilitar a interação entre usuários em uma rede social simplificada.
Para acessar a documencao rode no terminal a aplicacao e acesse
http://127.0.0.1:8000/redoc/#tag/api/operation/api_schema_retrieve

## Tecnologias Utilizadas

Este projeto foi desenvolvido utilizando as seguintes tecnologias:

-   **Python 3.x**
-   **Django 5.1.3**
-   **Django REST Framework 3.15.2**
-   **PostgreSQL** (via `psycopg2`)
-   **DRF-Yasg** e **Spectacular** para documentação de APIs
-   **JWT (SimpleJWT)** para autenticação de usuários

## Requisitos para Configuração

Para configurar o ambiente e rodar o projeto, você precisará de:

-   **Python 3.8 ou superior**
-   Banco de dados **PostgreSQL** configurado
-   Ferramentas: `pip` e `virtualenv`

## Configuração e Execução

### 1. Clone o Repositório

Primeiro, clone o repositório para sua máquina local e navegue até o diretório do projeto. Execute os seguintes comandos no terminal:

1.  Clone o repositório com o comando `git clone https://seu-repositorio-url.git`.
2.  Navegue até a pasta do projeto com `cd microblog`.

### 2. Crie e Ative um Ambiente Virtual

É recomendado criar um ambiente virtual para isolar as dependências do projeto. Para criar o ambiente virtual, execute o comando `python -m venv venv`.

Em seguida, ative o ambiente virtual:

-   Se você estiver usando **Linux** ou **macOS**, execute `source venv/bin/activate`.
-   Se você estiver no **Windows**, execute `venv\Scripts\activate`.

### 3. Instale as Dependências

Com o ambiente virtual ativado, instale as dependências necessárias para rodar o projeto utilizando o comando `pip install -r requirements.txt`.


### 4. Configure o Banco de Dados

Acesse o arquivo `settings.py` localizado na pasta principal do seu projeto Django e configure o banco de dados de acordo com as suas necessidades. O Django utiliza, por padrão, o SQLite, mas para este projeto, recomenda-se o uso do PostgreSQL.

No arquivo `settings.py`, localize a variável `DATABASES`. Substitua a configuração padrão pelo seguinte modelo, ajustando os valores para corresponder às credenciais do seu banco de dados PostgreSQL:

### 5. Faça as Migrações do Banco de Dados

Antes de rodar o servidor, você precisa criar as migrações para os modelos que você definiu e, em seguida, aplicar essas migrações ao banco de dados.

1.  Para gerar as migrações, execute o comando `python manage.py makemigrations`.
2.  Após isso, aplique as migrações para criar as tabelas no banco de dados com o comando `python manage.py migrate`.

### 6. Rode o Servidor de Desenvolvimento

Após configurar tudo, inicie o servidor de desenvolvimento com o comando `python manage.py runserver`.

### Documentação da API

A API do projeto **microblog** possui documentação gerada automaticamente com o **Redoc**. Para acessá-la, basta abrir seu navegador e ir até:

`http://127.0.0.1:8000/redoc`

A documentação será sempre atualizada automaticamente com base nas definições dos endpoints da API.