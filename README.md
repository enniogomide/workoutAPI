# 🏋️ WorkoutAPI

**Versão:** 0.1.0  
**Descrição:** A simple RESTful API developed with FastAPI, SQLAlchemy, and Pydantic for managing workout routines.  
**Autor:** [Ennio Gomide](mailto:ennio.gomide@gmail.com)  
**Arquivo de leitura:** README.md

## 📦 Requirements

- **Versão mínima do Python:** >= 3.13
- **Dependências:**
  - `fastapi (>=0.116.1,<0.117.0)`
  - `uvicorn (>=0.35.0,<0.36.0)`
  - `sqlalchemy (>=2.0.42,<3.0.0)`
  - `pydantic (>=2.11.7,<3.0.0)`
  - `alembic (>=1.16.4,<2.0.0)`
  - `aiosqlite (>=0.21.0,<0.22.0)`
  - `pydantic-settings (>=2.10.1,<3.0.0)`
  - `ruff (>=0.12.8,<0.13.0)`
  - `mkdocs (>=1.6.1,<2.0.0)`

## Project Structure

```
project/
│
└──  workoutapi/
    ├── main.py
    ├── routers.py
    ├── atletas/
    │   ├── __init__.py
    │   ├── controller.py
    │   ├── models.py
    │   └── schemas.py
    │
    ├── categorias/
    │   ├── __init__.py
    │   ├── controller.py
    │   ├── models.py
    │   └── schemas.py
    │
    ├── centro_treinamento/
    │   ├── __init__.py
    │   ├── controller.py
    │   ├── models.py
    │   └── schemas.py
    │ 
    ├── configs/
    |   ├── __init__.py
    |   ├── database.py
    |   └── settings.py
    |
    ├── contrib/
    |   ├── __init__.py
    |   └──  repository
    |       ├── __init__.py
    |       ├── models.py
    |       └── schemas.py
    |
    ├── alembic.ini
    ├── .gitignore
    ├── mkdocs.yml
    ├── poetry.lock
    ├── pyproject.toml
    ├── requirements.txt
    ├── treinamento.db
    └── README.md
```

  ## 🔀 API routers

The API is organized into three main groups of routes, each with its respective prefix and tag:

### 🧍 Atletas (`/atletas`)
- `POST /` – CCreate a new athlete
- `GET /` – List all athletes
- `GET /{id}` – Search for athlete by ID
- `PATCH /{id}` – Partially update an athlete
- `DELETE /{id}` – Delete athlete

### 🏷️ Categorias (`/categorias`)
- `POST /` – Create a new category
- `GET /` – List all category
- `GET /{id}` – Search for category by ID

### 🏋️ Centros de Treinamento (`/centros_treinamento`)
- `POST /` – Create a new training center
- `GET /` – List all training centers
- `GET /{id}` – BSearch training center by ID


# 🔍 API Routes Explanation 

## 🧍 Atletas (`/atletas`)

### `POST /atletas`
- **Descrição**: Cria um novo atleta no banco de dados.
- **Entrada**: Objeto `AtletaIn` contendo os dados do atleta.
- **Saída**: Objeto `AtletaOut` com os dados do atleta criado.
- **Status**: `201 Created`

### `GET /atletas`
- **Descrição**: Lista todos os atletas cadastrados.
- **Saída**: Lista de objetos `AtletaOut`.
- **Status**: `200 OK`

### `GET /atletas/{id}`
- **Descrição**: Retorna os dados de um atleta específico pelo seu ID.
- **Parâmetro**: `id` (UUID)
- **Saída**: Objeto `AtletaOut`.
- **Status**: `200 OK`

### `PATCH /atletas/{id}`
- **Descrição**: Atualiza parcialmente os dados de um atleta.
- **Parâmetros**: `id` (UUID), corpo com `AtletaUpdate`
- **Saída**: Objeto `AtletaOut` atualizado.
- **Status**: `200 OK`

### `DELETE /atletas/{id}`
- **Descrição**: Remove um atleta do banco de dados.
- **Parâmetro**: `id` (UUID)
- **Saída**: Nenhuma (status sem corpo).
- **Status**: `204 No Content`

---

## 🏷️ Categorias (`/categorias`)

### `POST /categorias`
- **Descrição**: Cria uma nova categoria de treino.
- **Entrada**: Objeto `CategoriaIn`.
- **Saída**: Objeto `CategoriaOut`.
- **Status**: `201 Created`

### `GET /categorias`
- **Descrição**: Lista todas as categorias disponíveis.
- **Saída**: Lista de objetos `CategoriaOut`.
- **Status**: `200 OK`

### `GET /categorias/{id}`
- **Descrição**: Retorna os dados de uma categoria específica pelo ID.
- **Parâmetro**: `id` (UUID)
- **Saída**: Objeto `CategoriaOut`.
- **Status**: `200 OK`

---

## 🏋️ Centros de Treinamento (`/centros_treinamento`)

### `POST /centros_treinamento`
- **Descrição**: Cria um novo centro de treinamento.
- **Entrada**: Objeto `CentroTreinamentoIn`.
- **Saída**: Objeto `CentroTreinamentoOut`.
- **Status**: `201 Created`

### `GET /centros_treinamento`
- **Descrição**: Lista todos os centros de treinamento cadastrados.
- **Saída**: Lista de objetos `CentroTreinamentoOut`.
- **Status**: `200 OK`

### `GET /centros_treinamento/{id}`
- **Descrição**: Retorna os dados de um centro de treinamento específico pelo ID.
- **Parâmetro**: `id` (UUID)
- **Saída**: Objeto `CentroTreinamentoOut`.
- **Status**: `200 OK`
