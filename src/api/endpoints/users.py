from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from src.db.session import get_db
from src.db.models import User as UserModel
from src.schemas.user import User as UserSchema, UserCreate
from src.core.security import get_password_hash, get_current_user

router = APIRouter()

@router.post("/", response_model=UserSchema, status_code=status.HTTP_201_CREATED, summary="Registrar un nuevo usuario")
async def create_user(
    *,
    db: AsyncSession = Depends(get_db),
    user_in: UserCreate,
):
    """
    Crea un nuevo usuario en el sistema.

    - **username**: Debe ser único.
    - **email**: Debe ser único.
    - **password**: Se almacenará de forma segura.
    """
    hashed_password = get_password_hash(user_in.password)

    # Usamos los nombres de campo del modelo SQLAlchemy (snake_case)
    db_user = UserModel(
        username=user_in.username,
        email=user_in.email,
        hashed_password=hashed_password,
        company_name=user_in.company_name,
        tax_id=user_in.tax_id,
        preferred_currency=user_in.preferred_currency,
    )

    db.add(db_user)
    try:
        await db.commit()
        await db.refresh(db_user)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El nombre de usuario o el email ya existen en el sistema.",
        )

    return db_user

@router.get("/me", response_model=UserSchema, summary="Obtener datos del usuario actual")
async def read_users_me(current_user: UserModel = Depends(get_current_user)):
    """
    Devuelve los datos del usuario que realiza la solicitud (autenticado).
    """
    return current_user
