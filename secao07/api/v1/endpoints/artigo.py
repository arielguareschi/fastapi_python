from typing import List

from fastapi import APIRouter, status, Depends, HTTPException, Response

from sqlalchemy.orm import Session
from sqlalchemy.future import select

from models.artigo_model import ArtigoModel
from models.usuario_model import UsuarioModel

from schemas.artigo_schema import ArtigoSchema

from core.deps import get_session, get_current_user

router = APIRouter()


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=ArtigoSchema)
def post_artigo(artigo: ArtigoSchema, usuario_logado=Depends(get_current_user),
                      db: Session = Depends(get_session)):
    novo_artigo = ArtigoModel(titulo=artigo.titulo,
                              descricao=artigo.descricao,
                              url_fonte=artigo.url_fonte,
                              usuario_id=usuario_logado.id)
    db.add(novo_artigo)
    db.commit()

    return novo_artigo


@router.get('/', response_model=List[ArtigoSchema])
def get_artigos(db: Session = Depends(get_session)):
    with db as session:
        query = select(ArtigoModel)
        result = session.execute(query)
        artigos: List[ArtigoModel] = result.scalars().unique().all()

        return artigos


@router.get('/{artigo_id}', response_model=ArtigoSchema, status_code=status.HTTP_200_OK)
def get_artigo(artigo_id: int, db: Session = Depends(get_session)):
    with db as session:
        query = select(ArtigoModel).filter(ArtigoModel.id == artigo_id)
        result = session.execute(query)
        artigo = result.scalars().unique().one_or_none()
        if artigo:
            return artigo
        else:
            raise HTTPException(detail="Artigo nao encontrado",
                                status_code=status.HTTP_404_NOT_FOUND)


@router.put('/{artigo_id}', response_model=ArtigoSchema, status_code=status.HTTP_202_ACCEPTED)
def put_artigo(artigo_id: int, artigo: ArtigoSchema, usuario_logado=Depends(get_current_user), db: Session = Depends(get_session)):
    with db as session:
        query = select(ArtigoModel).filter(ArtigoModel.id == artigo_id)
        result = session.execute(query)
        artigo_up = result.scalars().unique().one_or_none()

        if artigo_up:
            if artigo_up.titulo:
                artigo_up.titulo = artigo.titulo
            if artigo_up.descricao:
                artigo_up.descricao = artigo.descricao
            if artigo_up.url_fonte:
                artigo_up.url_fonte = artigo.url_fonte
            if usuario_logado.id != artigo_up.usuario_id:
                artigo_up.usuario_id = usuario_logado.id
            session.commit()

            return artigo_up
        else:
            raise HTTPException(detail="Artigo nao encontrado",
                                status_code=status.HTTP_404_NOT_FOUND)


@router.delete('/{artigo_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_artigo(artigo_id: int, usuario_logado=Depends(get_current_user), db: Session = Depends(get_session)):
    with db as session:
        query = select(ArtigoModel).filter(ArtigoModel.id == artigo_id).filter(
            ArtigoModel.usuario_id == usuario_logado.id)
        result = session.execute(query)
        artigo_del = result.scalars().unique().one_or_none()

        if artigo_del:
            session.delete(artigo_del)
            session.commit()
            return Response(status_code=status.HTTP_204_NO_CONTENT)

        else:
            raise HTTPException(detail="Artigo nao encontrado",
                                status_code=status.HTTP_404_NOT_FOUND)
