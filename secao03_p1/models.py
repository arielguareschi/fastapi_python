from typing import Optional

from pydantic import BaseModel, validator


class Curso(BaseModel):
    id: Optional[int] = None
    titulo: str
    aulas: int #mais de 12
    horas: int #mais de 10

    @validator('titulo')
    def validar_titulo(cls, value: str):
        palavras = value.split(' ')
        if len(palavras) < 3:
            raise ValueError('pelo menos 3 palavras')
        
        if value.islower():
            raise ValueError('nao so minusculo')

        return value
            
    @validator('aulas')
    def validar_aulas(cls, value: int):
        if (value < 12):
            raise ValueError('mais que 12')
        
        return value
    
    @validator('horas')
    def validar_horas(cls, value: int):
        if (value < 10):
            raise ValueError('mais que 10')
        
        return value


cursos = [Curso(id=1, titulo="Progra 1 a", aulas=43, horas=333),
          Curso(id=2, titulo="Progra 2 a", aulas=43, horas=333),
          Curso(id=3, titulo="Progra 3 a", aulas=43, horas=333),
          Curso(id=4, titulo="Progra 4 a", aulas=43, horas=333),
          Curso(id=5, titulo="Progra 5 a", aulas=43, horas=333)]
