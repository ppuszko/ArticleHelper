import logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from langchain_google_genai import ChatGoogleGenerativeAI
import os

from src.exceptions.exceptions import AppException
from src.db.main import init_engine, init_sessionmaker
from src.auth.main import fastapi_users, auth_backend
from src.auth.schemas import UserCreate, UserRead
from src.api.doc.routes import doc_router
from src.config.ai import AIConfig

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler()]
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    os.environ["GOOGLE_API_KEY"] = AIConfig.GOOGLE_API_KEY

    engine = init_engine()
    app.state.engine = engine
    app.state.sessionmaker = init_sessionmaker(engine)

    app.state.img_proc_model = ChatGoogleGenerativeAI(model=AIConfig.IMG_PROC_MODEL)
    app.state.text_proc_model = ChatGoogleGenerativeAI(model=AIConfig.TEXT_PROC_MODEL)

    yield

    await engine.dispose()

app = FastAPI(title="TeXelp", lifespan=lifespan)

@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

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

app.include_router(doc_router, prefix="/doc", tags=["doc"])

