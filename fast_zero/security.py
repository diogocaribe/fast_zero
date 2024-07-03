from pwdlib import PasswordHash

pwd_context = PasswordHash.recommended()


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
