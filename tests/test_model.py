from sqlalchemy import select

from fast_zero.models import User


def test_user():
    user = User(
        username='usernametest',
        email='emailtest@email.com',
        password='123',
    )
    assert user == User(
        username='usernametest', email='emailtest@email.com', password='123'
    )


def test_create_user(session):
    user = User(
        username='alice',
        email='alice@email.com',
        password='123',
    )

    session.add(user)
    session.commit()

    assert user == session.scalar(select(User).where(User.username == 'alice'))
