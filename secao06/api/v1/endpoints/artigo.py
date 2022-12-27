from typing import List

from fastapi import APIRouter, status, Depends, HTTPException, Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from secao06.models.artigo_model import ArtigoModel
from schemas.artigo_schema import ArtigoSchema
from core.deps import get_session


router = APIRouter()


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=ArtigoSchema)
async def post_artigo(artigo: ArtigoSchema, db: AsyncSession = Depends(get_session)):
    novo_artigo = ArtigoModel(titulo=artigo.titulo,
                            aulas=artigo.aulas, horas=artigo.horas)
    db.add(novo_artigo)
    await db.commit()

    return novo_artigo


@router.get('/', response_model=List[ArtigoSchema])
async def get_artigos(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(ArtigoModel)
        result = await session.execute(query)
        artigos: List[ArtigoModel] = result.scalars().all()

        return artigos


@router.get('/{artigo_id}', response_model=ArtigoSchema, status_code=status.HTTP_200_OK)
async def get_artigo(artigo_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(ArtigoModel).filter(ArtigoModel.id == artigo_id)
        result = await session.execute(query)
        artigo = result.scalar_one_or_none()
        if artigo:
            return artigo
        else:
            raise HTTPException(detail="Artigo nao encontrado",
                                status_code=status.HTTP_404_NOT_FOUND)


@router.put('/{artigo_id}', response_model=ArtigoSchema, status_code=status.HTTP_202_ACCEPTED)
async def put_artigo(artigo_id: int, artigo: ArtigoSchema, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(ArtigoModel).filter(ArtigoModel.id == artigo_id)
        result = await session.execute(query)
        artigo_up = result.scalar_one_or_none()

        if artigo_up:
            artigo_up.titulo = artigo.titulo
            artigo_up.horas = artigo.horas
            artigo_up.aulas = artigo.aulas
            await session.commit()

            return artigo_up
        else:
            raise HTTPException(detail="Artigo nao encontrado",
                                status_code=status.HTTP_404_NOT_FOUND)

@router.delete('/{artigo_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_artigo(artigo_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(ArtigoModel).filter(ArtigoModel.id == artigo_id)
        result = await session.execute(query)
        artigo_del = result.scalar_one_or_none()

        if artigo_del:
            await session.delete(artigo_del)
            await session.commit()
            return Response(status_code=status.HTTP_204_NO_CONTENT)
            
        else:
            raise HTTPException(detail="Artigo nao encontrado",
                                status_code=status.HTTP_404_NOT_FOUND)