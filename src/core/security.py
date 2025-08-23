from datetime import datetime, timedelta
from typing import Optional, Any
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.core.config import API_SECRET_KEY
from src.db.session import get_db
from src.db.models import User
from src.schemas import TokenData, User as UserSchema

# --- Password Hashing ---
# Usamos bcrypt como el algoritmo de hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# --- OAuth2 Scheme ---
# Esto le dice a FastAPI en qué URL el cliente debe obtener el token.
# Lo usaremos como una dependencia en los endpoints protegidos.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/login/token")

# --- JWT Configuration ---
ALGORITHM = "HS256"
# Tiempo de vida del token de acceso (ej. 30 minutos)
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica una contraseña plana contra su versión hasheada."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Genera el hash de una contraseña."""
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Crea un nuevo token de acceso JWT."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, API_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_user(db: AsyncSession, username: str) -> Optional[User]:
    """Busca un usuario en la base de datos por su nombre de usuario."""
    result = await db.execute(select(User).filter(User.username == username))
    return result.scalars().first()

async def get_current_user(
    db: AsyncSession = Depends(get_db), token: str = Depends(oauth2_scheme)
) -> User:
    """
    Dependencia de FastAPI para obtener el usuario actual a partir de un token JWT.
    Se usa para proteger endpoints.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, API_SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: str = payload.get("id")
        if username is None or user_id is None:
            raise credentials_exception
        token_data = TokenData(username=username, user_id=user_id)
    except JWTError:
        raise credentials_exception

    user = await get_user(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user
