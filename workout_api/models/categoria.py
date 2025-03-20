from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from workout_api.models.base import Base


class Categoria(Base):
    __tablename__ = "categoria"

    pk_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nome: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    atleta: Mapped["Atleta"] = relationship(back_populates="categoria")  # noqa
