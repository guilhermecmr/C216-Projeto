# EnqueteHub

## Descrição do Projeto

O EnqueteHub é uma aplicação web desenvolvida como projeto da disciplina C216, com foco no gerenciamento de enquetes e votação. A ideia é permitir que usuários cadastrem-se no sistema, façam login, criem enquetes com múltiplas opções de respostas e acompanhem os resultados em tempo real por meio de uma API REST.

A aplicação foi construída com uma arquitetura separando responsabilidade entre backend, banco de dados, testes e frontend. O backend expõe rotas para criação, consulta, atualização e remoção de usuários, enquetes e opções, além do registro de votos e da consulta dos resultados de cada enquete. O projeto também utiliza Docker e Docker Compose para execução em ambiente containerizado.

## Tecnologias Utilizadas

### Backend
- Python 3.12
- FastAPI
- asyncpg
- Uvicorn

### Banco de Dados
- PostgreSQL

### Testes
- Pytest
- FastAPI TestClient

### Infraestrutura
- Docker

### Frontend
- Em desenvolvimento

## Execução

> Depois

## Estrutura

```text
C216-PROJETO/
├── backend/
│   ├── app/
│   │   ├── db/
│   │   │   ├── connection.py
│   │   │   ├── init.sql
│   │   │   └── seed.sql
│   │   ├── routes/
│   │   │   ├── auth.py
│   │   │   ├── options.py
│   │   │   ├── polls.py
│   │   │   ├── users.py
│   │   │   └── votes.py
│   │   ├── schemas/
│   │   │   ├── auth.py
│   │   │   ├── option.py
│   │   │   ├── poll.py
│   │   │   ├── user.py
│   │   │   └── vote.py
│   │   ├── services/
│   │   │   ├── auth_service.py
│   │   │   ├── option_service.py
│   │   │   ├── poll_service.py
│   │   │   ├── user_service.py
│   │   │   └── vote_service.py
│   │   └── main.py
│   ├── tests/
│   │   ├── auxiliares.py
│   │   ├── test_options.py
│   │   ├── test_polls.py
│   │   ├── test_users.py
│   │   └── test_votes.py
│   ├── Dockerfile
│   ├── pytest.ini
│   └── requirements.txt
├── frontend/
├── docker-compose.yml
└── README.md
```

## Testes e Execução dos Testes

> Depois

## Banco de Dados
<details>
No projeto, foi utilizado o banco de dados PostgreSQL. A modelagem foi criada para sustentar o fluxo principal do sistema de votação.

A estrutura foi separada em quatro tabelas principais: `usuarios`, `enquetes`, `opcoes` e `votos`. Essa divisão permite representar corretamente os atores do sistema, as enquetes criadas por eles, as alternativas disponíveis para cada enquete e os votos registrados em cada opção. O banco também utiliza chaves estrangeiras e restrições de unicidade para garantir consistência dos dados e evitar situações inválidas, como um voto duplicado do mesmo usuário na mesma enquete.

### Tabela `usuarios`

Armazena os usuários cadastrados no sistema.

Campos principais:
- `id`: identificador único do usuário.
- `nome`: nome do usuário.
- `email`: endereço de e-mail, com restrição de unicidade.
- `senha`: senha cadastrada.
- `created_at`: data e hora de criação do registro.

### Tabela `enquetes`

Armazena as enquetes criadas no sistema.

Campos principais:
- `id`: identificador único da enquete.
- `titulo`: título da enquete.
- `descricao`: descrição opcional da enquete.
- `usuario_id`: referência ao usuário que criou a enquete.
- `created_at`: data e hora de criação do registro.

### Tabela `opcoes`

Armazena as alternativas disponíveis em cada enquete.

Campos principais:
- `id`: identificador único da opção.
- `texto`: conteúdo textual da opção.
- `enquete_id`: referência à enquete à qual a opção pertence.

### Tabela `votos`

Armazena os votos registrados pelos usuários.

Campos principais:
- `id`: identificador único do voto.
- `usuario_id`: referência ao usuário que votou.
- `enquete_id`: referência à enquete votada.
- `opcao_id`: referência à opção escolhida.
- `created_at`: data e hora do voto.

### Relacionamentos do Banco

- `usuarios` 1:N `enquetes`
  - Um usuário pode criar várias enquetes.
  - Cada enquete pertence a um único usuário.

- `enquetes` 1:N `opcoes`
  - Uma enquete pode possuir várias opções.
  - Cada opção pertence a uma única enquete.

- `usuarios` N:N `enquetes` por meio de `votos`
  - Um usuário pode votar em várias enquetes.
  - Uma enquete pode receber votos de vários usuários.
  - A tabela `votos` registra essa interação e também guarda a opção escolhida.

- `opcoes` 1:N `votos`
  - Uma opção pode receber vários votos.
  - Cada voto referencia exatamente uma opção.

### Regras de Integridade

- Não é permitido criar enquete associada a usuário inexistente.
- Não é permitido criar opção associada a enquete inexistente.
- Não é permitido votar em opção que não pertença à enquete informada.
- Não é permitido votar mais de uma vez na mesma enquete com o mesmo usuário.
- O resultado da enquete é calculado a partir da contagem dos votos armazenados.
</details>

## Endpoints do Backend
<details>
A API do backend está organizada em quatro grupos principais: usuários, enquetes, opções e votos. A seguir estão os endpoints atualmente implementados.

### Autenticação

#### `POST /auth/login`

Realiza a autenticação de um usuário já cadastrado.

Entrada esperada:
- `email`
- `senha`

Resposta:
- `id`
- `nome`
- `email`

Uso:
- Permite que o frontend valide as credenciais do usuário e mantenha sua sessão ativa durante o uso da aplicação.

Erros possíveis:
- `401` se o e-mail ou a senha estiverem incorretos.

### Usuários

#### `POST /users`
Cria um novo usuário no sistema.

Entrada esperada:
- `nome`
- `email`
- `senha`

Resposta:
- Dados do usuário criado, incluindo `id`, `nome` e `email`.

Uso:
- Cadastro inicial de usuários no sistema.

#### `GET /users`
Lista todos os usuários cadastrados.

Resposta:
- Lista com os registros de usuários disponíveis.

Uso:
- Consulta geral de usuários.

#### `GET /users/{user_id}`
Busca um usuário específico pelo identificador.

Parâmetro:
- `user_id`: identificador do usuário.

Resposta:
- Dados do usuário encontrado.

Erros possíveis:
- `404` se o usuário não existir.

#### `PUT /users/{user_id}`
Atualiza completamente os dados de um usuário existente.

Parâmetro:
- `user_id`: identificador do usuário.

Entrada esperada:
- `nome`
- `email`
- `senha`

Resposta:
- Dados atualizados do usuário.

Erros possíveis:
- `404` se o usuário não existir.

#### `DELETE /users/{user_id}`
Remove um usuário do sistema.

Parâmetro:
- `user_id`: identificador do usuário.

Resposta:
- Mensagem confirmando a remoção.

Erros possíveis:
- `404` se o usuário não existir.

### Enquetes

#### `POST /polls`
Cria uma nova enquete.

Entrada esperada:
- `titulo`
- `descricao`
- `usuario_id`

Resposta:
- Dados completos da enquete criada.

Uso:
- Cadastro de uma nova enquete vinculada a um usuário.

#### `GET /polls`
Lista todas as enquetes cadastradas.

Resposta:
- Lista de enquetes.

Uso:
- Tela de consulta geral das enquetes.

#### `GET /polls/{poll_id}`
Busca uma enquete específica pelo identificador.

Parâmetro:
- `poll_id`: identificador da enquete.

Resposta:
- Dados completos da enquete.

Erros possíveis:
- `404` se a enquete não existir.

#### `PUT /polls/{poll_id}`
Atualiza completamente os dados de uma enquete.

Parâmetro:
- `poll_id`: identificador da enquete.

Entrada esperada:
- `titulo`
- `descricao`

Resposta:
- Dados atualizados da enquete.

Erros possíveis:
- `404` se a enquete não existir.

#### `DELETE /polls/{poll_id}`
Remove uma enquete do sistema.

Parâmetro:
- `poll_id`: identificador da enquete.

Resposta:
- Mensagem confirmando a remoção.

Erros possíveis:
- `404` se a enquete não existir.

#### `GET /polls/results/{poll_id}`
Retorna o resultado consolidado de uma enquete.

Parâmetro:
- `poll_id`: identificador da enquete.

Resposta:
- Identificador da enquete.
- Título.
- Total de votos.
- Lista de opções com contagem de votos e percentual.

Uso:
- Exibição dos resultados da votação.

Erros possíveis:
- `404` se a enquete não existir.

### Opções

#### `POST /options`
Cria uma nova opção para uma enquete.

Entrada esperada:
- `texto`
- `enquete_id`

Resposta:
- Dados completos da opção criada.

Uso:
- Cadastro das alternativas disponíveis em uma enquete.

#### `GET /options`
Lista todas as opções cadastradas.

Resposta:
- Lista de opções disponíveis.

Uso:
- Consulta geral das alternativas do sistema.

#### `GET /options/poll/{poll_id}`
Lista todas as opções pertencentes a uma enquete específica.

Parâmetro:
- `poll_id`: identificador da enquete.

Resposta:
- Lista das opções vinculadas à enquete informada.

Uso:
- Tela de votação e consulta das opções de uma enquete.

#### `GET /options/{option_id}`
Busca uma opção específica pelo identificador.

Parâmetro:
- `option_id`: identificador da opção.

Resposta:
- Dados completos da opção.

Erros possíveis:
- `404` se a opção não existir.

#### `PUT /options/{option_id}`
Atualiza o texto de uma opção existente.

Parâmetro:
- `option_id`: identificador da opção.

Entrada esperada:
- `texto`

Resposta:
- Dados atualizados da opção.

Erros possíveis:
- `404` se a opção não existir.

#### `DELETE /options/{option_id}`
Remove uma opção do sistema.

Parâmetro:
- `option_id`: identificador da opção.

Resposta:
- Mensagem confirmando a remoção.

Erros possíveis:
- `404` se a opção não existir.

### Votos

#### `POST /votes`
Registra o voto de um usuário em uma enquete.

Entrada esperada:
- `usuario_id`
- `enquete_id`
- `opcao_id`

Validações realizadas:
- O usuário deve existir.
- A enquete deve existir.
- A opção deve existir.
- A opção deve pertencer à enquete informada.
- O usuário não pode votar mais de uma vez na mesma enquete.

Resposta:
- Dados do voto registrado.

Erros possíveis:
- `404` se usuário, enquete ou opção não existirem.
- `400` se a opção não pertencer à enquete.
- `400` se o usuário já tiver votado naquela enquete.
</details>

## Endpoints do Frontend

> Depois
