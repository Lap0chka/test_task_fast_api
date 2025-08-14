from base.repository import SQLAlchemyRepository

from auth.models import RefreshTokenModel, UserModel


class UserRepository(SQLAlchemyRepository):
    model = UserModel


class AuthRepository(SQLAlchemyRepository):
    model = RefreshTokenModel
