"""Api para estudo"""

from http import HTTPStatus

from fastapi import FastAPI, HTTPException
from fastapi.params import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_zero.database import get_session
from fast_zero.models import User
from fast_zero.schemas import Message, UserList, UserPublic, UserSchema
from fast_zero.security import get_password_hash

app = FastAPI()

database = []


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Olá mundo'}


@app.post('/users/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema, session: Session = Depends(get_session)):
    user_db = session.scalar(
        select(User).where(
            (User.username == user.username) | (User.email == user.email)
        )
    )
    if user_db:
        if user_db.username == user.username:
            raise HTTPException(
                HTTPStatus.BAD_REQUEST, detail='Username already exists'
            )
        elif user_db.email == user.email:
            raise HTTPException(HTTPStatus.BAD_REQUEST, detail='Email already exists')

    user_db = User(
        username=user.username,
        email=user.email,
        password=get_password_hash(user.password),
    )

    session.add(user_db)
    session.commit()
    session.refresh(user_db)

    return user_db


@app.get('/users/', response_model=UserList)
def read_users(skip: int = 0, limit: int = 10, session: Session = Depends(get_session)):
    database = session.scalars(select(User).offset(skip).limit(limit))
    return {'users': database}


@app.put('/users/{user_id}', response_model=UserPublic, status_code=HTTPStatus.CREATED)
def update_user(
    user_id: int, user: UserSchema, session: Session = Depends(get_session)
):
    user_db = session.scalar(select(User).where(User.id == user_id))
    if not user_db:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='User not found')

    if user_db:
        if user_db.username == user.username:
            raise HTTPException(
                HTTPStatus.BAD_REQUEST, detail='Username already exists'
            )
        elif user_db.email == user.email:
            raise HTTPException(HTTPStatus.BAD_REQUEST, detail='Email already exists')

    user_db.username = user.username
    user_db.email = user.email
    user_db.password = user.password
    session.commit()
    session.refresh(user_db)
    return user_db


@app.delete('/users/{user_id}', response_model=Message)
def delete_user(user_id: int, session: Session = Depends(get_session)):
    user_db = session.scalar(select(User).where(User.id == user_id))
    if not user_db:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='User not found')
    session.delete(user_db)
    session.commit()

    return {'message': 'User deleted'}


@app.get('/users/{user_id}', response_model=UserPublic)
def get_user(user_id: int, session: Session = Depends(get_session)):
    user_db = session.scalar(select(User).where(User.id == user_id))
    if not user_db:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='User not found')

    return user_db
