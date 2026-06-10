from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager


from ..db.main import init_engine, init_sessionmaker
from ..auth.main import fastapi_users, auth_backend
from ..auth.schemas import UserCreate, UserRead

@asynccontextmanager
async def lifespan(app: FastAPI):
    engine = init_engine()
    app.state.engine = engine
    app.state.sessionmaker = init_sessionmaker(engine)

    yield

    await engine.dispose()

app = FastAPI(title="TeXelp", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth",
    tags=["auth"]
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"]
)
app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"]
)

