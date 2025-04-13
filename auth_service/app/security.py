from datetime import datetime, timedelta, timezone

from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from app.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/auth/token")


SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password) -> bool:
    """Верификация пароля по хешу"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password) -> str:
    """Преобразование пароля в хеш"""
    return pwd_context.hash(password)


def create_access_token(data: dict, expiries_delta: timedelta | None = None):
    """Создание JWT-токена"""
    to_encode = data.copy()
    if expiries_delta:
        expire = datetime.now(timezone.utc) + expiries_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
