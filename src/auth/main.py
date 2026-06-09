from fastapi_users.authentication import CookieTransport, JWTStrategy, AuthenticationBackend, BearerTransport
from fastapi_users import BaseUserManager, UUIDIDMixin, FastAPIUsers
from fastapi import Request, Depends

from typing import AsyncIterator
from uuid import UUID

from ..config.auth import AuthConfig

cookie_transport = CookieTransport()
bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")

def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=AuthConfig.JWT_SECRET, lifetime_seconds=AuthConfig.TOKEN_LIFETIME_SECONDS)

auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy
)

