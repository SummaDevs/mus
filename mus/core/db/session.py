from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from mus.api.config.config import api_config

SQLALCHEMY_DATABASE_URI = "postgresql+asyncpg://{0}:{1}@{2}:{3}/{4}".format(
    api_config["DB"]["DB_USER"],
    api_config["DB"]["DB_PASS"],
    api_config["DB"]["DB_HOST"],
    api_config["DB"]["DB_PORT"],
    api_config["DB"]["DB_NAME"],
)

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URI,
    pool_pre_ping=True,
    pool_size=int(api_config["DB"]["DB_POOL_SIZE"]),
    max_overflow=int(api_config["DB"]["DB_MAX_OVERFLOW"]),
    future=True,
    echo=True if api_config["LOGGER"]["LOGGING_LEVEL"] == "DEBUG" else False,
)

async_session = sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,
    future=True,
    autoflush=False,
)
