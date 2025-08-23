import uuid
from pydantic import BaseModel, Field
from datetime import datetime
from decimal import Decimal
from .transaction_category import TransactionCategory

# --- Esquemas de Transacción ---

class TransactionBase(BaseModel):
    description: str = Field(..., description="Descripción de la transacción.")
    amount: Decimal = Field(..., gt=0, description="Monto de la transacción, debe ser positivo.")
    currency: str = Field("ARS", description="Moneda de la transacción (ej. ARS, USD).")
    type: str = Field(..., description="Tipo de transacción: 'income' (ingreso) o 'expense' (egreso).")
    date: datetime = Field(..., description="Fecha y hora en que se realizó la transacción.")
    category_id: uuid.UUID = Field(..., description="ID de la categoría a la que pertenece la transacción.")

    class Config:
        allow_population_by_field_name = True


class TransactionCreate(TransactionBase):
    # El `user_id` se obtendrá del path de la URL, no del body,
    # por lo que no es necesario aquí.
    pass


class Transaction(TransactionBase):
    id: uuid.UUID
    user_id: uuid.UUID = Field(..., description="ID del usuario al que pertenece la transacción.")
    created_at: datetime = Field(..., description="Fecha y hora de registro de la transacción.")

    # Incluir el objeto completo de la categoría en la respuesta
    # para evitar que el cliente tenga que hacer una solicitud adicional.
    category: TransactionCategory

    class Config:
        orm_mode = True
