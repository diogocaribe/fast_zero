from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_zero.database import get_session
from fast_zero.models import User
from fast_zero.schemas import Message, UserList, UserPublic, UserSchema
from fast_zero.security import (
    get_current_user,
    get_password_hash,
)

router = APIRouter(
    prefix='/users',
    tags=['users'],
)


T_Session = Annotated[Session, Depends(get_session)]
T_CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post('/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema, session: T_Session):
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


@router.get('/', response_model=UserList)
def read_users(
    session: T_Session,
    skip: int = 0,
    limit: int = 10,
):
    database = session.scalars(select(User).offset(skip).limit(limit))
    return {'users': database}


@router.put(
    '/{user_id}',
    response_model=UserPublic,
    status_code=HTTPStatus.CREATED,
)
def update_user(
    user_id: int,
    user: UserSchema,
    session: T_Session,
    current_user: T_CurrentUser,
):
    if current_user.id != user_id:
        raise HTTPException(HTTPStatus.FORBIDDEN, detail='Not enough permission')
    current_user.username = user.username
    current_user.email = user.email
    current_user.password = get_password_hash(user.password)
    session.commit()
    session.refresh(current_user)
    return current_user


@router.delete('/{user_id}', response_model=Message)
def delete_user(
    user_id: int,
    session: T_Session,
    current_user: T_CurrentUser,
):
    if current_user.id != user_id:
        raise HTTPException(HTTPStatus.FORBIDDEN, detail='Not enough permission')
    session.delete(current_user)
    session.commit()

    return {'message': 'User deleted'}


@router.get('/{user_id}', response_model=UserPublic)
def get_user(user_id: int, session: T_Session):
    user_db = session.scalar(select(User).where(User.id == user_id))
    if not user_db:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='User not found')

    return user_db
