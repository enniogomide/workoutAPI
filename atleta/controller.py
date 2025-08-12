from datetime import datetime
from uuid import uuid4

from fastapi import APIRouter, Body, HTTPException, status, Query
from typing import Optional, Annotated
from pydantic import UUID4
from sqlalchemy.future import select

from atleta.models import AtletaModel
from atleta.schemas import AtletaIn, AtletaOut, AtletaUpdate, AtletaAll
from categorias.models import CategoriaModel
from centro_treinamento.models import CentroTreinamentoModel
from contrib.repository.dependencies import DatabaseDependency

router = APIRouter()


@router.post(
    '/',
    summary='Criar um novo atleta',
    status_code=status.HTTP_201_CREATED,
    response_model=AtletaOut,
)
async def post(
    db_session: DatabaseDependency, atleta_in: AtletaIn = Body()
) -> AtletaOut:
    categoria = (
        (
            await db_session.execute(
                select(CategoriaModel).filter_by(nome=atleta_in.categoria.nome)
            )
        )
        .scalars()
        .first()
    )

    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'Categoria não encontrada: {atleta_in.categoria.nome}',
        )

    centro_treinamento = (
        (
            await db_session.execute(
                select(CentroTreinamentoModel).filter_by(
                    nome=atleta_in.centro_treinamento.nome
                )
            )
        )
        .scalars()
        .first()
    )

    if not centro_treinamento:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'Centro de treinamento não encontrado: {atleta_in.centro_treinamento.nome}',
        )

    try:
        atleta_out = AtletaOut(
            id=uuid4(),
            created_at=datetime.utcnow(),
            **atleta_in.model_dump(),
        )
        atleta_model = AtletaModel(
            **atleta_out.model_dump(
                exclude={'categoria', 'centro_treinamento'}
            )
        )
        atleta_model.categoria_id = categoria.pk_id
        atleta_model.centro_treinamento_id = centro_treinamento.pk_id
        db_session.add(atleta_model)
        await db_session.commit()
    except Exception as e:
        await db_session.rollback()
        if 'UNIQUE constraint failed' in e.args[0]:
            raise HTTPException(
                status_code=status.HTTP_303_SEE_OTHER,
                detail=f'Já existe um atleta cadastrado com o cpf: {atleta_in.cpf}',
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f'Erro ao inserir atleta. {e}',
        )
    return atleta_out


@router.get(
    '/',
    summary='Listar Atletas',
    status_code=status.HTTP_200_OK,
    response_model=list[AtletaOut],
)
async def query_all(
    db_session: DatabaseDependency,
    offset: int = 0,
    limit: int = 100,
    nome: Optional[str] = Query(None, Description='Nome do atleta para filtro'),
    cpf: Optional[str] = Query(None, Description='CPF do atleta para filtro'),

) -> list[AtletaOut]:
    atletas: list[AtletaOut] = (
        (await db_session.execute(
            select(AtletaModel).offset(offset).limit(limit)
            )).scalars().all()
    )
    if nome:
        lista_atletas = [atleta for atleta in atletas if nome.lower() in atleta.nome.lower()]
    elif cpf:
        lista_atletas = [atleta for atleta in atletas if cpf == atleta.cpf]
    else:
        lista_atletas = [AtletaOut.model_validate(atleta) for atleta in atletas]

    return lista_atletas


@router.get(
    '/nomes/',
    summary='Listar todos Atletas com nome, categoria e centro de treinamento',
    status_code=status.HTTP_200_OK,
    response_model=list[AtletaAll],
)
async def query_nomes(
    db_session: DatabaseDependency,
    offset: int = 0,
    limit: int = 100,
) -> list[AtletaAll]:
    atletas: list[AtletaAll] = (
        (await db_session.execute(
            select(AtletaModel).offset(offset).limit(limit)
            )).scalars().all()
    )
    lista_atletas = [AtletaAll.model_validate(atleta) for atleta in atletas]
    return lista_atletas


@router.get(
    '/{id}',
    summary='Listar atleta pelo id',
    status_code=status.HTTP_200_OK,
    response_model=AtletaOut,
)
async def query_id(
    id: UUID4,
    db_session: DatabaseDependency,
) -> AtletaOut:
    atleta: AtletaOut = (
        (await db_session.execute(select(AtletaModel).filter_by(id=id)))
        .scalars()
        .first()
    )
    if not atleta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Atleta não encontrada para id: {id}',
        )
    return atleta


@router.patch(
    '/{id}',
    summary='Atualizar campos específicos do atleta',
    status_code=status.HTTP_200_OK,
    response_model=AtletaOut,
)
async def atualiza_parcial(
    id: UUID4, db_session: DatabaseDependency, atleta_up: AtletaUpdate = Body()
) -> AtletaOut:
    atleta: AtletaOut = (
        (await db_session.execute(select(AtletaModel).filter_by(id=id)))
        .scalars()
        .first()
    )
    if not atleta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Atleta não encontrada para id: {id}',
        )
    atleta_data = atleta_up.model_dump(exclude_unset=True)
    for key, value in atleta_data.items():
        setattr(atleta, key, value)
    await db_session.commit()
    await db_session.refresh(atleta)
    return atleta



@router.delete(
    '/{id}',
    summary='Excluir atleta',
    status_code=status.HTTP_204_NO_CONTENT,
)
async def get(id: UUID4, db_session: DatabaseDependency) -> None:
    atleta: AtletaOut = (
        (await db_session.execute(select(AtletaModel).filter_by(id=id)))
        .scalars()
        .first()
    )
    if not atleta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Atleta não encontrada para id: {id}',
        )
    await db_session.delete(atleta)
    await db_session.commit()
