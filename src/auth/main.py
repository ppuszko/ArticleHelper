from fastapi_users.authentication import CookieTransport, JWTStrategy, AuthenticationBackend, BearerTransport
from fastapi_users import BaseUserManager, UUIDIDMixin, FastAPIUsers
from fastapi import Request, Depends

from typing import AsyncIterator
from uuid import UUID

from ..db.models import User
from ..db.main import get_user_db
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

class UserManager(UUIDIDMixin, BaseUserManager[User, UUID]):
    reset_password_token_secret = AuthConfig.RESET_PASSWORD_TOKEN_SECRET
    verification_token_secret = AuthConfig.VERIFICATION_TOKEN_SECRET

    async def on_after_register(self, user: User, request: Request | None = None):
        print(f"User {user.id} has registered.")

    async def on_after_forgot_password(
        self, user: User, token: str, request: Request | None = None
    ):
        print(f"User {user.id} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(
        self, user: User, token: str, request: Request | None = None
    ):
        print(f"Verification requested for user {user.id}. Verification token: {token}")

async def get_user_manager(user_db = Depends(get_user_db)) -> AsyncIterator[UserManager]:
    yield UserManager(user_db)

fastapi_users = FastAPIUsers[User, UUID](
    get_user_manager,
    [auth_backend]
)