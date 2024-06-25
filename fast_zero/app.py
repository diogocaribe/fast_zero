"""Api para estudo"""

from http import HTTPStatus

from fastapi import FastAPI, HTTPException

from fast_zero.schemas import Message, UserDb, UserList, UserPublic, UserSchema

app = FastAPI()

database = []


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Olá mundo'}


@app.post('/user/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema):  # Schema pydantic do user e validação
    user_with_id = UserDb(
        id=len(database) + 1,  # Criando o id com o len não podendo ser 0
        **user.model_dump(),  # Construindo o dict a partir do
    )

    database.append(user_with_id)

    return user_with_id


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
