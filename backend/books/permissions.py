from fastapi import HTTPException, status

from base.abstract import AbstractPermissionService


class Is_Authenticated(AbstractPermissionService):
    async def validate_permission(self):
        if not self.user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authenticated"
            )
        if not self.user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Inactive user"
            )
