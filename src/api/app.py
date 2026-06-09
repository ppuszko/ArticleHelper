from fastapi import FastAPI
from contextlib import asynccontextmanager


from src.db.main import init_engine, init_sessionmaker

@asynccontextmanager
async def lifespan(app: FastAPI):
    engine = init_engine()
    app.state.engine = engine
    app.state.sessionmaker = init_sessionmaker(engine)

    yield

    await engine.dispose()