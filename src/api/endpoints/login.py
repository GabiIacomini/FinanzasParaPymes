from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.session import get_db
from src.core.security import create_access_token, verify_password, get_user
from src.schemas.token import Token
from src.core.config import ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter()

@router.post("/token", response_model=Token, summary="Obtener un token de acceso")
async def login_for_access_token(
    db: AsyncSession = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
):
    """
    Endpoint para que un usuario inicie sesión con su nombre de usuario y contraseña.

    Si las credenciales son correctas, devuelve un token de acceso JWT.
    """
    user = await get_user(db, username=form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Nombre de usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        # El "subject" del token será el nombre de usuario.
        # También incluimos el user_id para un acceso más fácil.
        data={"sub": user.username, "id": str(user.id)},
        expires_delta=access_token_expires,
    )

    return {"access_token": access_token, "token_type": "bearer"}
