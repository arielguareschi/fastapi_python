from pydantic import BaseSettings, AnyHttpUrl
from sqlalchemy.ext.declarative import declarative_base


class Settings(BaseSettings):
    '''
    Configuracoes gerais
    '''
    API_V1_STR: str = '/api/v1'
    DB_URL: str = 'postgresql+asyncpg://postgres:masterkey@localhost:5432/faculdade'
    #DB_URL: str = 'firebird+fdb://SYSDBA:masterkey@10.11.12.247:3050/aero32db/siga/aerosml.gdb'
    DBBaseModel = declarative_base()

    class Config:
        case_sensitive = True


settings = Settings()
