import uuid
from pydantic import BaseModel, Field
from typing import Optional

# --- Esquemas de Categoría de Transacción ---

class TransactionCategoryBase(BaseModel):
    name: str = Field(..., description="Nombre de la categoría (ej. 'Ventas', 'Alquiler').")
    type: str = Field(..., description="Tipo de categoría: 'income' (ingreso) o 'expense' (egreso).")
    color: Optional[str] = Field("#6B7280", description="Color hexadecimal para la UI.")

    class Config:
        allow_population_by_field_name = True


class TransactionCategoryCreate(TransactionCategoryBase):
    # No se necesitan campos adicionales para la creación,
    # ya que `is_default` es manejado por la lógica de negocio, no por el usuario.
    pass


class TransactionCategory(TransactionCategoryBase):
    id: uuid.UUID
    is_default: bool = Field(..., description="Indica si es una categoría por defecto del sistema.")

    class Config:
        orm_mode = True
