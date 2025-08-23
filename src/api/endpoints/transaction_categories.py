from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from src.db.session import get_db
from src.db.models import TransactionCategory as CategoryModel, User as UserModel
from src.schemas.transaction_category import TransactionCategory as CategorySchema, TransactionCategoryCreate
from src.core.security import get_current_user

router = APIRouter()

@router.post(
    "/",
    response_model=CategorySchema,
    status_code=status.HTTP_201_CREATED,
    summary="Crear una nueva categoría de transacción"
)
async def create_transaction_category(
    category_in: TransactionCategoryCreate,
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """
    Crea una nueva categoría de transacción.

    Aunque el esquema actual no asocia las categorías a un usuario específico
    (son globales), se requiere autenticación para crear nuevas categorías.
    Las categorías por defecto (`is_default=True`) solo deberían ser creadas
    mediante scripts de seeding.
    """
    db_category = CategoryModel(**category_in.dict())
    db.add(db_category)
    await db.commit()
    await db.refresh(db_category)
    return db_category

@router.get(
    "/",
    response_model=List[CategorySchema],
    summary="Obtener todas las categorías de transacción"
)
async def read_transaction_categories(
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """
    Devuelve una lista de todas las categorías de transacción disponibles en el sistema.
    """
    result = await db.execute(select(CategoryModel).order_by(CategoryModel.name))
    categories = result.scalars().all()
    return categories
