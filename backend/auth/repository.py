from auth.models import User
from base.repository import SQLAlchemyRepository


class UserRepository(SQLAlchemyRepository):
    model = User