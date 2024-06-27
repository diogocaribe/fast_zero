from sqlalchemy import select

from fast_zero.models import User


def test_model_table_user():
    user = User(
        username='usernametest',
        email='emailtest@email.com',
        password='123',
    )
    assert user == User(
        username='usernametest', email='emailtest@email.com', password='123'
    )


def test_create_user(session):
    new_user = User(username='alice', email='alice@email.com', password='123')

    session.add(new_user)
    session.commit()
    user = session.scalar(select(User).where(User.username == 'alice'))
    assert user.username == 'alice'


def test_update_user(session):
    new_user = User(username='alice', email='alice@email.com', password='123')

    session.add(new_user)
    session.commit()

    session.query(User).filter(User.id == 1).update({'username': 'alice sousa'})
    user = session.scalar(select(User).where(User.id == 1))
    assert user.username == 'alice sousa'
