from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
import uuid

from src.db.session import get_db
from src.db.models import Transaction as TransactionModel, User as UserModel
from src.schemas.transaction import Transaction as TransactionSchema, TransactionCreate
from src.core.security import get_current_user

router = APIRouter()

@router.post(
    "/",
    response_model=TransactionSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Crear una nueva transacción"
)
async def create_transaction(
    *,
    db: AsyncSession = Depends(get_db),
    transaction_in: TransactionCreate,
    current_user: UserModel = Depends(get_current_user)
):
    """
    Crea una nueva transacción asociada al usuario autenticado.
    """
    # Creamos el objeto del modelo SQLAlchemy a partir del esquema Pydantic
    db_transaction = TransactionModel(
        **transaction_in.dict(),
        user_id=current_user.id  # Asociamos la transacción al usuario actual
    )
    db.add(db_transaction)
    await db.commit()
    await db.refresh(db_transaction)
    return db_transaction

@router.get(
    "/",
    response_model=List[TransactionSchema],
    summary="Obtener las transacciones del usuario"
)
async def read_transactions(
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
    skip: int = 0,
    limit: int = 100
):
    """
    Devuelve una lista de las transacciones del usuario autenticado.
    Soporta paginación con `skip` y `limit`.
    """
    result = await db.execute(
        select(TransactionModel)
        .where(TransactionModel.user_id == current_user.id)
        .order_by(TransactionModel.date.desc())
        .offset(skip)
        .limit(limit)
    )
    transactions = result.scalars().all()
    return transactions
