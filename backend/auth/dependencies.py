from typing import Annotated

from auth.models import UserModel
from auth.services import AuthService, UserService
from base.abstract import AbstractPermissionService
from base.dependencies import get_service
from fastapi.params import Depends, Security
from fastapi.security import OAuth2PasswordBearer
from starlette.requests import Request

oauth_scheme: OAuth2PasswordBearer = OAuth2PasswordBearer(
    tokenUrl="/auth/login",
)


async def get_user_from_jwt(
    token: Annotated[str, Security(oauth_scheme)],
    auth_service: Annotated[AuthService, Depends(get_service(AuthService))],
    user_service: Annotated[UserService, Depends(get_service(UserService))],
) -> UserModel:
    """Return FastAPI dependencies for authentication and validation.

    Includes:
    - OAuth2 password bearer scheme for JWT authentication.
    - Dependency to retrieve an AuthService instance.
    - Async dependency to extract a User from a JWT token.
    - Factory for a permission validation dependency
    """
    user_id = await auth_service.validate_token_for_user(token)
    return await user_service.get_user_by_id(user_id)


class PermissionDependency:
    """
    Permission dependency for permission validation to FastAPI routes.
    """

    def __init__(self, permissions: list[type[AbstractPermissionService]]):
        self.permissions = permissions

    async def __call__(
        self,
        request: Request,
        user: Annotated[UserModel, Depends(get_user_from_jwt)],
    ) -> UserModel:
        """Callable used as a FastAPI dependency.

        It receives the request and
        authenticated user, applies all permission classes, and raises
        if any permission fails.
        """
        for permission_cls in self.permissions:
            # Instantiate permission with request and user
            p_class = permission_cls(request=request, user=user)
            #  the actual permission check
            await p_class.validate_permission()

        # If all checks pass, return the user
        return user
