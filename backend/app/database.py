from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from config import settings

connect_args = {}
if settings.database_url.startswith("sqlite"):
    connect_args["check_same_thread"] = False

engine = create_async_engine(url=settings.database_url, connect_args=connect_args)

SessionLocal = async_sessionmaker(
    autoflush=False, expire_on_commit=False, bind=engine, class_=AsyncSession
)


class Base(DeclarativeBase):
    pass


async def get_db():
    async with SessionLocal() as session:
        yield session


async def init_db():
    async with engine.begin() as db:
        await db.run_sync(Base.metadata.create_all)
