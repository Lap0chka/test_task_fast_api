import logging
from abc import ABC, abstractmethod

from auth.models import UserModel
from starlette.requests import Request

logger = logging.getLogger(__name__)


# Abstract base class for all permission services.
# Enforces a contract for permission validation logic.
class AbstractPermissionService(ABC):
    """Abstract base class for implementing permission validation.
    """

    def __init__(
        self,
        user: UserModel,
        request: Request,
    ):
        """Initialize BasePermissionService with user and request.
        """
        # The current authenticated user
        self.user: UserModel = user

        # The current HTTP request
        self.request: Request = request

    @abstractmethod
    async def validate_permission(
        self,
    ) -> None:
        """Abstract method that must be implemented by all permission classes.

        Should raise an exception if the permission check fails.
        """
        raise NotImplementedError
