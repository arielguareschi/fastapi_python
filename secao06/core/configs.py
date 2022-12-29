from typing import List
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

    JWT_SECRET: str = 'ldUfdO-I2Wi0_MJXF8EPE3LW4yB0a308JoeEpVNRnO8'
    '''
    import secrets 
    
    token: str = secrets.token_urlsafe(32)
    '''
    ALGORITHM: str = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTS: int = 60 * 24 * 7

    class Config:
        case_sensitive = True


settings = Settings()
