from pydantic import BaseModel
from typing import Optional
import uuid

# --- Esquemas de Token para Autenticación ---

# Esquema para la respuesta del endpoint de login.
# Esto es lo que se devuelve al cliente.
class Token(BaseModel):
    access_token: str
    token_type: str


# Esquema para los datos contenidos dentro del token JWT.
# Esto es lo que se extrae del token para identificar al usuario en las solicitudes protegidas.
class TokenData(BaseModel):
    username: Optional[str] = None
    user_id: Optional[str] = None # Se guarda como string en el token
