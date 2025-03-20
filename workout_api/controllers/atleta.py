from datetime import datetime
from uuid import uuid4
from typing import Optional  # Import necessário para parâmetros opcionais

from fastapi import APIRouter, Body, HTTPException, status
from pydantic import UUID4

from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError  # Import necessário para capturar a exceção

from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy_future import paginate as sqlalchemy_paginate

from workout_api.dependencies import DataBaseDependency
from workout_api.models.atleta import Atleta as AtletaModel
from workout_api.schemas.atleta import Atleta as AtletaIn
from workout_api.schemas.atleta import AtletaOut, AtletaOutBasic
from workout_api.schemas.atleta import AtletaUpdate
from workout_api.models.categoria import Categoria as CategoriaModel
from workout_api.models.centro_treinamento import CentroTreinamento as CentroTreinamentoModel

router = APIRouter(prefix="/atletas", tags=["Atletas"])


# @router.get(
# "/",
# summary="Consultar todas as Categorias",
# status_code=status.HTTP_200_OK,
# response_model=list[AtletaOut],
# )
# async def list_atletas(db_session: DataBaseDependency) -> list[AtletaOut]:
# atletas: list[AtletaOut] = (
# (await db_session.execute(select(AtletaModel))).scalars().all()
# )
# return atletas
######### ********************************


@router.post(
    "/",
    summary="Criar novo atleta",
    status_code=status.HTTP_201_CREATED,
    response_model=AtletaOut,
)
async def create_atleta(
    db_session: DataBaseDependency, atleta_in: AtletaIn = Body(...)
) -> AtletaOut:

    categoria_nome = atleta_in.categoria.nome
    centro_treinamento_nome = atleta_in.centro_treinamento.nome

    categoria = (
        (
            await db_session.execute(
                select(CategoriaModel).filter_by(nome=categoria_nome)
            )
        )
        .scalars()
        .first()
    )

    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"A categoria {categoria_nome} não foi encontrada.",
        )

    centro_treinamento = (
        (
            await db_session.execute(
                select(CentroTreinamentoModel).filter_by(nome=centro_treinamento_nome)
            )
        )
        .scalars()
        .first()
    )

    if not centro_treinamento:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"O centro de treinamento {centro_treinamento_nome} não foi encontrado.",
        )
    if not centro_treinamento:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"O centro de treinamento {centro_treinamento_nome} não foi encontrado.",
        )
    try:
        atleta_out = AtletaOut(
            id=uuid4(), created_at=datetime.utcnow(), **atleta_in.model_dump()
        )
        atleta_model = AtletaModel(
            **atleta_out.model_dump(exclude={"categoria", "centro_treinamento"})
        )

        atleta_model.categoria_id = categoria.pk_id
        atleta_model.centro_treinamento_id = centro_treinamento.pk_id

        db_session.add(atleta_model)
        await db_session.commit()

        return atleta_out
    except IntegrityError as exc:
        # Captura a exceção de integridade e verifica se é relacionada ao CPF
        await db_session.rollback()  # Reverte a transação em caso de erro
        if "cpf".strip().upper() in str(exc.orig).strip().upper():  # Verifica se o erro está relacionado ao CPF
            raise HTTPException(
                status_code=status.HTTP_303_SEE_OTHER,
                detail=f"Já existe um atleta cadastrado com o CPF: {atleta_in.cpf}",
            ) from exc
        # Relevanta a exceção se não for relacionada ao CPF
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocorreu um erro ao inserir os dados no banco referente a integridade",
        ) from exc
    except Exception as exc:
        await db_session.rollback()  # Reverte a transação em caso de erro
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocorreu um erro ao inserir os dados no banco",
        ) from exc


# @router.get(
#     "/",
#     summary="Consultar todas as Atletas",
#     status_code=status.HTTP_200_OK,
#     response_model=list[AtletaOut],
# )
# async def list_atletas(db_session: DataBaseDependency) -> list[AtletaOut]:
#     atletas = (await db_session.execute(select(AtletaModel))).scalars().all()
#     return [AtletaOut.model_validate(atleta, from_attributes=True) for atleta in atletas]
######### ********************************
## @router.get(
##     "/",
##     summary="Consultar todas as Atletas com filtros opcionais",
##     status_code=status.HTTP_200_OK,
##     response_model=list[AtletaOutBasic],
## )
## async def list_atletas(
##     db_session: DataBaseDependency,
##     nome: Optional[str] = None,
##     cpf: Optional[str] = None,
## ) -> list[AtletaOutBasic]:
##     query = select(AtletaModel)
##     # Adiciona filtros à query se os parâmetros forem fornecidos
##     if nome:
##         query = query.filter(AtletaModel.nome.ilike(f"%{nome}%"))
##     if cpf:
##         query = query.filter(AtletaModel.cpf == cpf)
##     atletas = (await db_session.execute(query)).scalars().all()
##     # return [AtletaOut.model_validate(atleta, from_attributes=True) for atleta in atletas]
##     # Customiza a resposta para incluir apenas os campos desejados
##     return [AtletaOutBasic.model_validate(atleta, from_attributes=True) for atleta in atletas]
## ######### ********************************


@router.get(
    "/",
    summary="Consultar todas as Atletas com filtros opcionais",
    status_code=status.HTTP_200_OK,
    response_model=Page[AtletaOutBasic],
)
async def list_atletas(
    db_session: DataBaseDependency,
    nome: Optional[str] = None,
    cpf: Optional[str] = None,
) -> list[AtletaOutBasic]:
    query = select(AtletaModel)
    # Adiciona filtros à query se os parâmetros forem fornecidos
    if nome:
        query = query.filter(AtletaModel.nome.ilike(f"%{nome}%"))
    if cpf:
        query = query.filter(AtletaModel.cpf == cpf)
    # atletas = (await db_session.execute(query)).scalars().all()
    # return [AtletaOutBasic.model_validate(atleta, from_attributes=True) for atleta in atletas]
    # Usa a função de paginação da biblioteca
    return await sqlalchemy_paginate(db_session, query)


@router.get(
    "/{id}",
    summary="Consulta uma Atleta pelo id",
    status_code=status.HTTP_200_OK,
    response_model=AtletaOut,
)
async def list_atleta_por_id(id: UUID4, db_session: DataBaseDependency) -> AtletaOut:
    atleta: AtletaOut = (
        (await db_session.execute(select(AtletaModel).filter_by(id=id)))
        .scalars()
        .first()
    )
    if not atleta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Atleta não encontrada no id: {id}",
        )
    return atleta


@router.patch(
    "/{id}",
    summary="Editar um Atleta pelo id",
    status_code=status.HTTP_200_OK,
    response_model=AtletaOut,
)
async def atualizar_atleta(
    id: UUID4, db_session: DataBaseDependency, atleta_up: AtletaUpdate = Body(...)
) -> AtletaOut:
    atleta: AtletaOut = (
        (await db_session.execute(select(AtletaModel).filter_by(id=id)))
        .scalars()
        .first()
    )
    if not atleta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Atleta não encontrado no id: {id}",
        )
    atleta_update = atleta_up.model_dump(exclude_unset=True)
    for key, value in atleta_update.items():
        setattr(atleta, key, value)
    await db_session.commit()
    await db_session.refresh(atleta)
    return atleta


@router.delete(
    "/{id}", summary="Deletar um Atleta pelo id", status_code=status.HTTP_204_NO_CONTENT
)
async def delete_atleta(id: UUID4, db_session: DataBaseDependency) -> None:
    atleta: AtletaOut = (
        (await db_session.execute(select(AtletaModel).filter_by(id=id)))
        .scalars()
        .first()
    )
    if not atleta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Atleta não encontrado no id: {id}",
        )
    await db_session.delete(atleta)
    await db_session.commit()
