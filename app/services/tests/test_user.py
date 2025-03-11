import unittest

from app.conftest import engine, TestingSessionLocal
from app.factory.address import AddressFactory  # Assuming you have AddressFactory
from app.factory.user import UserFactory
from app.schemas.user import UserCreate
from app.services.user import UserService


class TestServices(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures."""
        connection = engine.connect()
        self.db = TestingSessionLocal(bind=connection)
        self.user = UserFactory()  # Generates a random user
        self.address = AddressFactory(user=self.user)
        self.service = UserService(self.db)
        self.user.addresses = [self.address]  # Assign the generated address to the user

    def tearDown(self):
        """Tear down test fixtures."""
        self.db.close()
        self.db.rollback()

    def test_create_user(self):
        """Test creating a user."""

        user_create = UserCreate(
            email="newuser@example.com", password="newpassword123", username="New User"
        )
        self.user = self.service.create(user_create)
        self.assertIsNotNone(self.user)
