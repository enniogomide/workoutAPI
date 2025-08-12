from typing import Annotated

from pydantic import UUID4, Field

from contrib.schemas import BaseSchema


class CentroTreinamentoIn(BaseSchema):
    nome: Annotated[
        str,
        Field(
            description='Nome centro treinamento',
            example='São Paulo',
            max_length=20,
        ),
    ]
    endereco: Annotated[
        str,
        Field(
            description='Endereço centro treinamento',
            example='Rua São João, 120',
            max_length=60,
        ),
    ]
    proprietario: Annotated[
        str,
        Field(
            description='Proprietário do centro treinamento',
            example='Jose Silva',
            max_length=30,
        ),
    ]


class CentroTreinamentoAtleta(BaseSchema):
    nome: Annotated[
        str,
        Field(
            description='Nome centro treinamento',
            example='São Paulo',
            max_length=20,
        ),
    ]


class CentroTreinamentoOut(CentroTreinamentoIn):
    id: Annotated[
        UUID4, Field(description='Identficador do centro de treinamento')
    ]
