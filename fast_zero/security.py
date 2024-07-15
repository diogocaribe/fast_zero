from datetime import datetime, timedelta
from http import HTTPStatus
from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import decode, encode
from jwt.exceptions import DecodeError, ExpiredSignatureError
from pwdlib import PasswordHash
from sqlalchemy import select
from zoneinfo import ZoneInfo

from fast_zero.database import Session, get_session
from fast_zero.models import User
from fast_zero.schemas import TokenData
from fast_zero.settings import Settings

pwd_context = PasswordHash.recommended()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/token')
T_Session = Annotated[Session, Depends(get_session)]

settings = Settings()


def get_password_hash(password: str) -> str:
    """Função que criptografa a senha ('hash')

    Args:
        password (str): Senha declarada pelo usuário

    Returns:
        string: Hash gerado pelo pwdlib
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hash_password: str) -> bool:
    """Função para descriptografar a senha suja.

    Args:
        plain_password (str): Senha declarada pelo usuário (limpa)
        hash_password (str) : Senha criptografada (suja) gravada no banco

    Returns:
        bool: Se plain_password e hash_password são iguais.
    """
    return pwd_context.verify(plain_password, hash_password)


def create_access_token(data: dict) -> None:
    """Função para criar o token (jwt)

    Args:
        data (dict): Dados que serão fornecidos para o paylod do jwt
    """
    to_encode = data.copy()

    expire = datetime.now(tz=ZoneInfo('UTC')) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({'exp': expire})
    encoded_jwt = encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    return encoded_jwt


def get_current_user(
    session: T_Session,
    # Isso funciona para exigir que o usuário esteja logado para realizar
    #  alguma operação
    token: str = Depends(oauth2_scheme),
):
    credentials_exception = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )

    try:
        payload = decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get('sub')
        if not username:
            raise credentials_exception
        token_data = TokenData(username=username)
    except ExpiredSignatureError:
        raise credentials_exception
    except DecodeError:
        raise credentials_exception

    user = session.scalar(select(User).where(User.email == token_data.username))

    if not user:
        raise credentials_exception

    return user
