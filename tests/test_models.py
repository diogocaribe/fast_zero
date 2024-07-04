from fast_zero.models import User


def test_user():
    user = User(username='bob', email='bob@email.com', password='123')

    assert user.__repr__() == 'User(username=bob, email=bob@email.com)'
