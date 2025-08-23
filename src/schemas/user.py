import uuid
from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime

# --- Esquemas de Usuario ---

# Atributos compartidos por todos los esquemas de usuario
class UserBase(BaseModel):
    username: str
    email: EmailStr
    company_name: str = Field(..., description="Nombre de la empresa o razón social.")
    tax_id: Optional[str] = Field(None, description="CUIT o CUIL del usuario/empresa.")
    preferred_currency: Optional[str] = Field("ARS", description="Moneda preferida del usuario (ej. ARS, USD).")

    class Config:
        # Permitir que Pydantic mapee automáticamente los nombres de campo
        # de camelCase (en JSON) a snake_case (en Python) y viceversa.
        # En este caso, lo haremos manualmente con alias para mayor claridad.
        allow_population_by_field_name = True


# Esquema para la creación de un nuevo usuario (lo que se espera en el body de un POST)
class UserCreate(UserBase):
    password: str = Field(..., min_length=8, description="Contraseña del usuario.")


# Esquema que representa al usuario tal como se almacena en la base de datos (incluye la contraseña hasheada)
# No se expondrá directamente en la API.
class UserInDB(UserBase):
    id: uuid.UUID
    hashed_password: str

    class Config:
        orm_mode = True


# Esquema para las respuestas de la API (lo que se devuelve en un GET)
# No incluye la contraseña por seguridad.
class User(UserBase):
    id: uuid.UUID
    created_at: datetime = Field(..., description="Fecha y hora de creación del usuario.")

    class Config:
        orm_mode = True
        # Habilita la compatibilidad con modelos de ORM (SQLAlchemy)
        # Permite que Pydantic lea los datos directamente desde los objetos del modelo.
