# Workout API

Este projeto é uma API desenvolvida com **FastAPI** e **Docker** como parte do curso "Desenvolvendo Sua Primeira API com FastAPI, Python e Docker".

## Estrutura de Diretórios

```
workout_api/
├── main.py                # Ponto de entrada da aplicação
├── config.py              # Configurações da aplicação
├── database.py            # Configuração do banco de dados
├── security.py            # Funcionalidades de segurança
├── controllers/           # Rotas (controllers)
│   ├── __init__.py        # Importação centralizada dos controllers
│   ├── atleta.py          # Rotas para Atleta
│   ├── categoria.py       # Rotas para Categoria
│   ├── centro_treinamento.py  # Rotas para Centro de Treinamento
├── models/                # Modelos SQLAlchemy
│   ├── __init__.py        # Importação centralizada dos modelos
│   ├── atleta.py          # Modelo para Atleta
│   ├── categoria.py       # Modelo para Categoria
│   ├── centro_treinamento.py  # Modelo para Centro de Treinamento
├── schemas/               # Esquemas Pydantic
│   ├── __init__.py        # Importação centralizada dos esquemas
│   ├── atleta.py          # Esquema para Atleta
│   ├── categoria.py       # Esquema para Categoria
│   ├── centro_treinamento.py  # Esquema para Centro de Treinamento
├── alembic/               # Diretório do Alembic para migrações
├── requirements.txt       # Dependências do projeto
└── Makefile               # Automação de tarefas
└── README.md           # Documentação do projeto
```

## Como Executar

### Pré-requisitos

- Python 3.9 ou superior
- Docker e Docker Compose (opcional, mas recomendado)

### Passos

1. Clone o repositório:

   ```bash
   git clone <URL_DO_REPOSITORIO>
   cd workout_api
   ```
2. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```
3. Execute a aplicação:

   ```bash
   uvicorn app.main:app --reload
   ```
4. Acesse a API no navegador:

   ```
   http://127.0.0.1:8000
   ```

### Usando Docker

1. Construa a imagem Docker:

   ```bash
   docker build -t workout_api .
   ```
2. Execute o container:

   ```bash
   docker run -p 8000:8000 workout_api
   ```

## Testes

Para rodar os testes automatizados, use:

```bash
pytest
```

## Complementos

- **Documentação Automática**: Acesse `/docs` para visualizar a documentação gerada automaticamente pelo Swagger.
- **Requisitos Adicionais**: Certifique-se de que o arquivo `requirements.txt` contém todas as dependências necessárias.
- **Links Úteis**:
  - [FastAPI Documentation](https://fastapi.tiangolo.com/)
  - [Docker Documentation](https://docs.docker.com/)
