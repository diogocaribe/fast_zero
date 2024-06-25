"""Api para estudo"""

from http import HTTPStatus

from fastapi import FastAPI

from fast_zero.schemas import Message, UserDb, UserPublic, UserSchema

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
