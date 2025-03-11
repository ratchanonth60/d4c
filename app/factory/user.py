import factory
from factory.alchemy import SQLAlchemyModelFactory

from app.core.security import (
    get_password_hash,
)
from app.models.user import User, UserRole


class UserFactory(SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session_persistence = "commit"  # Ensures objects are committed

    id = factory.Sequence(lambda n: n + 1)
    username = factory.Faker("user_name")
    email = factory.Faker("email")
    hashed_password = factory.LazyAttribute(
        lambda _: get_password_hash("password123")
    )  # Hash default password
    role = factory.Iterator([UserRole.USER, UserRole.ADMIN])  # Randomly assign roles
    is_active = True
    is_verified = factory.Faker("boolean")
