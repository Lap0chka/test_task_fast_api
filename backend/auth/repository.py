from auth.models import UserModel, RefreshTokenModel
from base.repository import SQLAlchemyRepository


class UserRepository(SQLAlchemyRepository):
    model = UserModel


class AuthRepository(SQLAlchemyRepository):
    model = RefreshTokenModel

