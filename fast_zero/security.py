from datetime import datetime, timedelta

from jwt import encode
from pwdlib import PasswordHash
from zoneinfo import ZoneInfo

from fast_zero.settings import Settings

pwd_context = PasswordHash.recommended()

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
        settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({'exp': expire})
    encoded_jwt = encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    return encoded_jwt
