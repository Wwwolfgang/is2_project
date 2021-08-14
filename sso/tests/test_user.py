import pytest
from sso.models import User


@pytest.mark.django_db
class TestUser:

    def test_user_creation(self):
        user = User.objects.create(
            
        )