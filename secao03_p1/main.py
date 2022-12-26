from typing import Dict, List, Optional, Any

from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import status
from fastapi.responses import JSONResponse
from fastapi import Response
from fastapi import Path
from fastapi import Query
from fastapi import Header
from fastapi import Depends

from time import sleep

from models import Curso, cursos

app = FastAPI(
    title="API do api", 
    version='1.0.1',
    description="teste de api"
    )


def fake_db():
    try:
        print("abrindo o banco de dados")
        sleep(1)
    finally:
        print('fechando o banco')
        sleep(1)





@app.get('/cursoss', description="teste de cursos", summary='todos', response_model=List[Curso], response_description="deu certo")
async def get_cursos(db: Any = Depends(fake_db)):
    return cursos


@app.get('/curso/{curso_id}', response_model=List[Curso])
async def get_cursoss(curso_id: int = Path(default=None, title='ID do curso', description='Deve ser entre 1 e 2', gt=0, lt=3), db: Any = Depends(fake_db)):
    try:
        curso = cursos[curso_id]
        return curso
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Curso nao encontrado")


@app.post('/cursoss', status_code=status.HTTP_201_CREATED, response_model=Curso)
async def post_curso(curso: Curso):
    next_id: int = len(cursos) + 1
    curso.id = next_id
    cursos.append(curso)
    return curso
 

@app.put('/cursoss/{curso_id}', status_code=status.HTTP_202_ACCEPTED)
async def put_curso(curso_id: int, curso: Optional[Curso], db: Any = Depends(fake_db)):
    if curso_id in cursos:
        cursos[curso_id] = curso

        return curso
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Curso nao encontrado {curso_id}")


@app.delete('/cursoss/{curso_id}')
async def delete_curso(curso_id: int, db: Any = Depends(fake_db)):
    if curso_id in cursos:
        del cursos[curso_id]
        # return JSONResponse(content={'status': "removido com sucesso"}, status_code=status.HTTP_204_NO_CONTENT)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Curso nao encontrado {curso_id}")


@app.get('/calculadora')
async def calcular(a: int = Query(default=None, gt=5), b: int = Query(default=None), x_geek: str = Header(default=None), c: Optional[int] = None):
    resultado = a + b + c

    print(x_geek)
    return {"resultado": resultado}


if __name__ == '__main__':
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000,
                log_level="info", reload=True)
