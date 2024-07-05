from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_zero.database import get_session
from fast_zero.models import User
from fast_zero.schemas import Token
from fast_zero.security import create_access_token, verify_password

router = APIRouter(prefix='/auth', tags=['auth'])

T_Session = Annotated[Session, Depends(get_session)]
T_OAuthForm = Annotated[OAuth2PasswordRequestForm, Depends()]


# Craindo uma rota da tokerização da aplicação e que será injetada como
# dependência para os metodos que necessitem de autenticação/autorização
# A rota de token deve ser post para enviar dados para o servidor
# É necessário o python-multipart para utilizar o OAuth[...]Form
@router.post('/token', response_model=Token)
def login_for_access_token(
    session: T_Session,
    form_data: T_OAuthForm,
):
    user = session.scalar(select(User).where(User.email == form_data.username))
    if not user:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail='Incorrect email or password'
        )
    # Verificar autorização com senha encriptada
    if not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail='Incorrect email or password'
        )
    # verificar o token
    access_token = create_access_token(data={'sub': user.email})

    return {'access_token': access_token, 'token_type': 'Bearer'}
