"""Classes Shemas referente a Base"""

from datetime import datetime
from typing import Annotated

from pydantic import UUID4, BaseModel, Field


class Base(BaseModel):
    """Classe base para Shemas SQLAlchemy."""

    class Config:
        extra = "forbid"  # Não permite campos extras
        from_attriubute = True  # Permite a conversão de atributos
        # Substituir orm_mode # orm_mode = True  # Permite a conversão de tipos de dados


class OutMixin(Base):
    id: Annotated[UUID4, Field(description="Identificador")]
    created_at: Annotated[datetime, Field(description="Data de criação")]


class OutMixinId(Base):
    id: Annotated[UUID4, Field(description="Identificador")]
