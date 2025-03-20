from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from workout_api.models.base import Base


class Atleta(Base):
    __tablename__ = "atleta"

    pk_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nome: Mapped[str] = mapped_column(String(50), nullable=False)
    cpf: Mapped[str] = mapped_column(String(11), unique=True, nullable=False)
    idade: Mapped[int] = mapped_column(Integer, nullable=False)
    peso: Mapped[float] = mapped_column(Float, nullable=False)
    altura: Mapped[float] = mapped_column(Float, nullable=False)
    sexo: Mapped[str] = mapped_column(String(1), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    categoria: Mapped["Categoria"] = relationship(back_populates="atleta", lazy='selectin')  # noqa
    categoria_id: Mapped[int] = mapped_column(ForeignKey("categoria.pk_id"))
    centro_treinamento: Mapped["CentroTreinamento"] = relationship(back_populates="atleta", lazy='selectin')  # noqa
    centro_treinamento_id: Mapped[int] = mapped_column(ForeignKey("centro_treinamento.pk_id"))


    # pk_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    # nome: Mapped[str] = mapped_column(String(50), nullable=False)
    # cpf: Mapped[str] = mapped_column(String(11), nullable=False, unique=True)
    # idade: Mapped[int] = mapped_column(Integer, nullable=False)
    # peso: Mapped[float] = mapped_column(Float, nullable=False)
    # altura: Mapped[float] = mapped_column(Float, nullable=False)
    # sexo: Mapped[str] = mapped_column(String(1), nullable=False)
    # created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    # categoria_id: Mapped[int] = mapped_column(ForeignKey("categoria.pk_id"))
    # centro_treinamento_id: Mapped[int] = mapped_column(
    #     ForeignKey("centro_treinamento.pk_id")
    # )
    # categoria: Mapped["Categoria"] = relationship(back_populates="atleta", lazy='selectin')  # noqa: F821
    # centro_treinamento: Mapped["CentroTreinamento"] = relationship(
    #     back_populates="atleta", lazy='selectin'
    # )  # noqa: F821
    # __table_args__ = (
    #     CheckConstraint(
    #         "cpf ~ '^[0-9]+$'", name="cpf_numeric_check"
    #     ),  # Restrição CHECK
    # )
    # @field_validator("cpf")
    # def validate_cpf(cls, cpf):
    #     if not cpf.isdigit():
    #         raise ValueError("CPF deve conter apenas dígitos.")
    #     return cpf
