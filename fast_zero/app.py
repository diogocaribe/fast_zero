"""Api para estudo"""

from http import HTTPStatus

from fastapi import FastAPI, HTTPException
from fastapi.params import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_zero.database import get_session
from fast_zero.models import User
from fast_zero.schemas import Message, UserDb, UserList, UserPublic, UserSchema

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

    user_db = User(username=user.username, email=user.email, password=user.password)

    session.add(user_db)
    session.commit()
    session.refresh(user_db)

    return user_db


@app.get('/users/', response_model=UserList)
def read_users():
    return {'users': database}


@app.put('/users/{user_id}', response_model=UserPublic)
def update_user(user_id: int, user: UserSchema):
    if user_id > len(database) or user_id < 1:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='User not found')
    user_with_id = UserDb(id=user_id, **user.model_dump())

    database[user_id - 1] = user_with_id

    return user_with_id


@app.delete('/users/{user_id}', response_model=Message)
def delete_user(user_id: int):
    if user_id > len(database) or user_id < 1:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='User not found')

    del database[user_id - 1]
    return {'message': 'User deleted'}


@app.get('/users/{user_id}', response_model=UserPublic)
def get_user(user_id: int):
    if user_id > len(database) or user_id < 1:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='User not found')

    return database[user_id - 1]
