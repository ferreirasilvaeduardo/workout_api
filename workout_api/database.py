from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from workout_api.config import settings

# Criar o engine assíncrono e # Criar a fábrica de sessões

engine = create_async_engine(settings.DATABASE_URL, echo=settings.DEBUG)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


# Dependência para obter a sessão do banco de dados
async def get_session() -> AsyncGenerator:
    async with async_session() as session:
        yield session
