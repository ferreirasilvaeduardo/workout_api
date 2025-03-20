"""Classes Shemas para validação de dados de centro treinamento."""

from typing import Annotated

from pydantic import Field

from workout_api.schemas.base import Base, OutMixinId


class CentroTreinamento(Base):
    nome: Annotated[str, Field(description='Nome do centro de treinamento', example='CT King', max_length=20)]
    endereco: Annotated[str, Field(description='Endereço do centro de treinamento', example='Rua X, Q02', max_length=60)]
    proprietario: Annotated[str, Field(description='Proprietario do centro de treinamento', example='Marcos', max_length=30)]


class CentroTreinamentoIn(CentroTreinamento):
    pass


class CentroTreinamentoOut(CentroTreinamento, OutMixinId):
    pass
