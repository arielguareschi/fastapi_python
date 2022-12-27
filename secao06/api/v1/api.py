from fastapi import APIRouter

from secao06.api.v1.endpoints import artigo


api_router = APIRouter()
api_router.include_router(artigo.router, prefix='/artigos', tags=['artigos'])


