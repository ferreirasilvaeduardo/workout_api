"""Classes Shemas para validação de dados de atletas."""
from datetime import datetime

from typing import Annotated, Optional

from pydantic import Field, PositiveFloat
# from pydantic import BaseModel, UUID4

from workout_api.schemas.base import Base, OutMixin
from workout_api.schemas.categoria import Categoria
from workout_api.schemas.centro_treinamento import CentroTreinamento


class Atleta(Base):
    nome: Annotated[str, Field(description='Nome do atleta', example='Joao', max_length=50)]
    cpf: Annotated[str, Field(description='CPF do atleta', example='12345678900', max_length=11)]
    idade: Annotated[int, Field(description='Idade do atleta', example=25)]
    peso: Annotated[PositiveFloat, Field(description='Peso do atleta', example=75.5)]
    altura: Annotated[PositiveFloat, Field(description='Altura do atleta', example=1.70)]
    sexo: Annotated[str, Field(description='Sexo do atleta', example='M', max_length=1)]
    categoria: Annotated["Categoria", Field(description='Categoria do atleta')] # noqa
    centro_treinamento: Annotated["CentroTreinamento", Field(description='Centro de treinamento do atleta')] # noqa


class AtletaIn(Atleta):
    pass


class AtletaOut(Atleta, OutMixin):
    pass
    # id: Annotated[UUID4, Field(description="Identificador")]
    # created_at: Annotated[datetime, Field(description="Data de criação")]
    # nome: Annotated[str, Field(description='Nome do atleta', example='Joao', max_length=50)]
    # cpf: Annotated[str, Field(description='CPF do atleta', example='12345678900', max_length=11)]
    # idade: Annotated[int, Field(description='Idade do atleta', example=25)]
    # peso: Annotated[PositiveFloat, Field(description='Peso do atleta', example=75.5)]
    # altura: Annotated[PositiveFloat, Field(description='Altura do atleta', example=1.70)]
    # sexo: Annotated[str, Field(description='Sexo do atleta', example='M', max_length=1)]
    # categoria: Annotated["Categoria", Field(description='Categoria do atleta')]
    # centro_treinamento: Annotated["CentroTreinamento", Field(description='Centro de treinamento do atleta')]
    # class Config:
    #     from_attributes = True  # Substituir orm_mode no Pydantic v2


class AtletaUpdate(Base):
    nome: Annotated[Optional[str], Field(None, description='Nome do atleta', example='Joao', max_length=50)]
    idade: Annotated[Optional[int], Field(None, description='Idade do atleta', example=25)]

# Reconstruir o modelo para garantir que está completamente definido
AtletaOut.model_rebuild()
# Reconstruir o modelo para garantir que está completamente definido
AtletaUpdate.model_rebuild()
