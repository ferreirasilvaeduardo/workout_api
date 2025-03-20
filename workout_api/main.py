import os
import sys

from fastapi import FastAPI
from fastapi_pagination import add_pagination

# Adicione o diretório do projeto ao sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def create_app():

    from workout_api.config import settings

    app = FastAPI(title=settings.APP_NAME, version=settings.APP_VERSION)

    from workout_api.controllers import router as api_router

    # Registrar as rotas
    app.include_router(api_router)
    # Adicionar Paginação Global
    add_pagination(app)
    return app


app = create_app()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="info", reload=True)
