from core.configs import settings
from core.database import engine
from sqlalchemy import MetaData


async def create_tables() -> None:
    import models._all_models
    print('Criando as tabelas')

    #settings.DBBaseModel.metadata.drop_all
    
    
    
    with engine.begin() as conn:        
        settings.DBBaseModel.metadata.drop_all
        settings.DBBaseModel.metadata.create_all
        #await conn.run(settings.DBBaseModel.metadata.drop_all)
        #await conn.run(settings.DBBaseModel.metadata.create_all)
    print('criadas tabelas')

if __name__ == '__main__':    
    import asyncio

    asyncio.run(create_tables())
