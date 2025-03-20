from uuid import uuid4

from fastapi import APIRouter, Body, HTTPException, status
from pydantic import UUID4
from sqlalchemy.future import select

from workout_api.dependencies import DataBaseDependency
from workout_api.models.centro_treinamento import (
    CentroTreinamento as CentroTreinamentoModel,
)
from workout_api.schemas.centro_treinamento import (  # Pydantic model
    CentroTreinamentoIn,
    CentroTreinamentoOut,
)

router = APIRouter(prefix="/centrotreinamentos", tags=["CentroTreinamentos"])


@router.post(
    "/",
    summary="Criar novo Centro Treinamento",
    status_code=status.HTTP_201_CREATED,
    response_model=CentroTreinamentoOut,
)
async def create_centrotreinamento(
    db_session: DataBaseDependency,
    centrotreinamento_in: CentroTreinamentoIn = Body(...),
) -> CentroTreinamentoOut:
    centrotreinamento_out = CentroTreinamentoOut(
        id=uuid4(), **centrotreinamento_in.model_dump()
    )
    centrotreinamento_model = CentroTreinamentoModel(
        **centrotreinamento_out.model_dump()
    )
    db_session.add(centrotreinamento_model)
    await db_session.commit()
    return centrotreinamento_out


@router.get(
    "/",
    summary="Consultar todas as Centro Treinamentos",
    status_code=status.HTTP_200_OK,
    response_model=list[CentroTreinamentoOut],
)
async def list_centrotreinamentos(
    db_session: DataBaseDependency,
) -> list[CentroTreinamentoOut]:
    centrotreinamentos: list[CentroTreinamentoOut] = (
        (await db_session.execute(select(CentroTreinamentoModel))).scalars().all()
    )

    return centrotreinamentos


@router.get(
    "/{id}",
    summary="Consulta uma Centro Treinamento pelo id",
    status_code=status.HTTP_200_OK,
    response_model=CentroTreinamentoOut,
)
async def list_centrotreinamento_por_id(
    id: UUID4, db_session: DataBaseDependency
) -> CentroTreinamentoOut:
    centrotreinamento: CentroTreinamentoOut = (
        (await db_session.execute(select(CentroTreinamentoModel).filter_by(id=id)))
        .scalars()
        .first()
    )

    if not centrotreinamento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"CentroTreinamento não encontrada no id: {id}",
        )

    return centrotreinamento
