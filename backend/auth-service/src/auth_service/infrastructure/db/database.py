import asyncio

from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from src.auth_service.config import config

class Database:
    def __init__(
            self,
            url: str,
            echo: bool = False,
            echo_pool: bool = False,
            max_overflow: int = 10,
            pool_size: int = 5,
            pool_timeout: int = 30,
            pool_recycle: int = 3600,
    ):
        self.engine = create_async_engine(
            url=url,
            echo=echo,
            echo_pool=echo_pool,
            max_overflow=max_overflow,
            pool_size=pool_size,
            pool_timeout=pool_timeout,
            pool_recycle=pool_recycle,
        )
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )
        
    async def dispose(self):
        await self.engine.dispose()

    async def get_session(self):
        async with self.session_factory() as session:
            yield session
            
    async def test_connection(self):
        async with self.engine.connect() as conn:
            result = await conn.execute(text("SELECT VERSION()"))
            print("Database version: ", result.all())
            
            
DATABASE_URL = f"postgresql+asyncpg://{config.db.user}:{config.db.password}@{config.db.host}:{config.db.port}/{config.db.database}"
database = Database(
    url=DATABASE_URL,
    echo=config.db.echo,
    echo_pool=config.db.echo_pool,
    max_overflow=config.db.max_overflow,
    pool_size=config.db.pool_size,
    pool_timeout=config.db.pool_timeout,
    pool_recycle=config.db.pool_recycle,
)

# test connection  
asyncio.run(database.test_connection())