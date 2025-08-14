from auth.models import RefreshTokenModel, UserModel
from base.repository import SQLAlchemyRepository


class UserRepository(SQLAlchemyRepository):
    model = UserModel


class AuthRepository(SQLAlchemyRepository):
    model = RefreshTokenModel
