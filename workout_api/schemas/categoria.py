"""Classes Shemas para validação de dados de categorias."""

from typing import Annotated

from pydantic import Field

from workout_api.schemas.base import Base, OutMixinId


class Categoria(Base):
    nome: Annotated[str, Field(description='Nome da categoria', example='Scale', max_length=10)]


class CategoriaIn(Categoria):
    pass


class CategoriaOut(Categoria, OutMixinId):
    pass
