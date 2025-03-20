from datetime import datetime, timedelta

import jwt

from workout_api.config import settings


# Função para criar um token JWT
def create_access_token(data: dict) -> str:
    """
    Gera um token JWT com os dados fornecidos.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


# Função para verificar e decodificar um token JWT
def verify_access_token(token: str) -> dict:
    """
    Verifica e decodifica um token JWT.
    """
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise ValueError("Token expirado")
    except jwt.InvalidTokenError:
        raise ValueError("Token inválido")
