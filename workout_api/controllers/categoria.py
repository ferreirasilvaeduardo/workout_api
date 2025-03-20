from uuid import uuid4

from fastapi import APIRouter, Body, HTTPException, status
from pydantic import UUID4
from sqlalchemy.future import select

from workout_api.dependencies import DataBaseDependency
from workout_api.models.categoria import Categoria as CategoriaModel
from workout_api.schemas.categoria import CategoriaIn, CategoriaOut  # Pydantic model

router = APIRouter(prefix="/categorias", tags=["Categorias"])


@router.post(
    "/",
    summary="Criar novo categoria",
    status_code=status.HTTP_201_CREATED,
    response_model=CategoriaOut,
)
async def create_categoria(
    db_session: DataBaseDependency, categoria_in: CategoriaIn = Body(...)
) -> CategoriaOut:
    categoria_out = CategoriaOut(id=uuid4(), **categoria_in.model_dump())
    categoria_model = CategoriaModel(**categoria_out.model_dump())
    db_session.add(categoria_model)
    await db_session.commit()
    return categoria_out


@router.get(
    "/",
    summary="Consultar todas as Categorias",
    status_code=status.HTTP_200_OK,
    response_model=list[CategoriaOut],
)
async def list_categorias(db_session: DataBaseDependency) -> list[CategoriaOut]:
    categorias: list[CategoriaOut] = (
        (await db_session.execute(select(CategoriaModel))).scalars().all()
    )

    return categorias


@router.get(
    "/{id}",
    summary="Consulta uma Categoria pelo id",
    status_code=status.HTTP_200_OK,
    response_model=CategoriaOut,
)
async def list_categoria_por_id(
    id: UUID4, db_session: DataBaseDependency
) -> CategoriaOut:
    categoria: CategoriaOut = (
        (await db_session.execute(select(CategoriaModel).filter_by(id=id)))
        .scalars()
        .first()
    )

    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Categoria não encontrada no id: {id}",
        )

    return categoria
