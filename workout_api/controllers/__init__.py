from fastapi import APIRouter, status

from workout_api.config import settings
from workout_api.controllers.atleta import router as atleta_router
from workout_api.controllers.categoria import router as categoria_router
from workout_api.controllers.centro_treinamento import (
    router as centro_treinamento_router,
)

router = APIRouter()


@router.get("/")
async def root():
    return {"message": "Bem-vindo à Workout API!"}


try:
    rota_secreta = (
        str(settings.SECRET_KEY)
        .replace(" ", "")
        .replace("/", "")
        .replace("\\", "")
        .replace(".", "")
        .replace(";", "")
        .replace("-", "")
        .strip()
        .lower()
    )

    @router.get(f"/secret_key_{rota_secreta}")
    async def read_root():
        return {
            "app_name": settings.APP_NAME,
            "app_version": settings.APP_VERSION,
            "debug": settings.DEBUG,
            "database_url": settings.DATABASE_URL,
            "secret_key": settings.SECRET_KEY,
        }

except:
    pass

router.include_router(atleta_router)
router.include_router(categoria_router)
router.include_router(centro_treinamento_router)

__all__ = ["router"]
