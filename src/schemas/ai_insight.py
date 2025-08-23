import uuid
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime

# --- Esquemas de AI Insight ---

class AiInsightBase(BaseModel):
    type: str = Field(..., description="Tipo de insight: 'pattern', 'opportunity', 'recommendation', 'alert'.")
    title: str = Field(..., description="Título conciso del insight.")
    description: str = Field(..., description="Descripción detallada y accionable del insight.")
    priority: Optional[str] = Field("medium", description="Prioridad del insight: 'low', 'medium', 'high'.")
    json_metadata: Optional[Dict[str, Any]] = Field(None, alias="metadata", description="Datos adicionales en formato JSON.")

    class Config:
        allow_population_by_field_name = True


class AiInsightCreate(AiInsightBase):
    # El user_id es necesario al momento de crear el insight en la base de datos.
    user_id: uuid.UUID


class AiInsight(AiInsightBase):
    id: uuid.UUID
    user_id: uuid.UUID = Field(..., description="ID del usuario asociado a este insight.")
    is_read: bool = Field(..., description="Indica si el usuario ha leído el insight.")
    created_at: datetime = Field(..., description="Fecha y hora de generación del insight.")

    class Config:
        orm_mode = True
