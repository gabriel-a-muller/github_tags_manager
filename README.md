# GITHUB Tag Manager

GITHUB Tag Manager é um projeto pessoal com o objetivo de adicionar TAGS aos repositórios com estrela do usuário.
O objetivo (além do aprendizado) é tornar possível pesquisar repositórios favoritados de acordo com as tags que o usuário desejar.

## Installation

Crie um venv para o projeto

```
path/to/project/python virtualenv venv
```

Instale as dependencias
Use o [pip](https://pip.pypa.io/en/stable/) para instala-las.

```bash
pip install -r requirements.txt
```

Não esqueça de rodar as migrações para o banco de dados!

Atualmente o arquivo de configuração do Django settings.py está no versionamento do projeto no GIT.

Isso em uma perspectiva de deploy e segurança, não é desejável.

Mas como estamos lidando com um projeto pessoal, de teste e avaliação, não representa risco.

### Dito isto, IMPORTANTE:

No settings, existe as informações necessárias para login no banco de dados utilizado em dev.

Caso queira utilizar um banco de dados para rodar a aplicação, crie um local com o nome tags_manager. (E altere informações de login)

Também está presente a chave da aplicação do GITHUB. 

## Usage

Ao rodar a aplicação e logar com sua conta do GitHub* a aplicação irá alimentar a tela com seus repositórios favoritos. Basta adicionar tags, pesquisar, clicar nas tags, interaja!

*(não se preocupe com seus dados, esta aplicação trabalha apenas com read-only)

## Contributing
Atualmente o projeto se encontra **SEM TESTES!** (Whops!)

É um passo fundamental para qualquer contribuição séria ou desenvolvimento saudável e escalável.

Existe a possibilidade do autor voltar e realizar esses testes =].

Qualquer dica, sugestão ou dúvida, fique livre para entrar em contato.

