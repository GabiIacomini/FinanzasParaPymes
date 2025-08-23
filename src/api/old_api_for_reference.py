import os
import uuid
import pandas as pd
from typing import List, Dict, Any, Optional

from fastapi import FastAPI, Depends, HTTPException, status, Header, BackgroundTasks
from pydantic import BaseModel, Field

# Importar la lógica de negocio existente
from .data_loader import load_financial_data
from .financial_calculator import calculate_financial_metrics
from .report_generator import generate_report

# --- Configuración de la Aplicación ---
app = FastAPI(
    title="Agente de Análisis Financiero para Pymes API",
    description="Una API para realizar análisis financieros de pymes usando IA.",
    version="1.0.0",
)

# --- Almacenamiento en Memoria para los Trabajos de Análisis ---
# En una aplicación de producción, esto debería ser reemplazado por una base de datos
# o un sistema de caché persistente como Redis.
analysis_jobs: Dict[str, Dict[str, Any]] = {}

# --- Modelos de Datos (Contratos de la API) ---
class Transaction(BaseModel):
    Fecha: str
    Descripción: str
    Categoría: str
    Ingreso: float
    Egreso: float

class AnalysisRequest(BaseModel):
    transactions: List[Transaction]

class AnalysisStatusResponse(BaseModel):
    analysis_id: str
    status: str
    result: Optional[Dict[str, Any]] = None

class AnalysisSubmissionResponse(BaseModel):
    message: str
    analysis_id: str

# --- Autenticación ---
API_SECRET_KEY = os.getenv("API_SECRET_KEY")
if not API_SECRET_KEY:
    raise RuntimeError("La variable de entorno API_SECRET_KEY no está configurada.")

async def verify_api_key(x_api_key: str = Header(...)):
    """Dependencia para verificar la clave de API en el encabezado."""
    if x_api_key != API_SECRET_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Clave de API inválida o faltante.",
        )

# --- Tarea en Segundo Plano para el Análisis ---
def run_financial_analysis(job_id: str, transactions_data: List[Dict]):
    """
    Función que se ejecuta en segundo plano para no bloquear la API.
    """
    try:
        # 1. Convertir los datos de entrada a un DataFrame de Pandas
        # Esto simula la carga de datos que antes se hacía desde un CSV.
        df = pd.DataFrame(transactions_data)

        # Validaciones y limpieza básicas (adaptado de data_loader)
        df["Fecha"] = pd.to_datetime(df["Fecha"], errors="coerce")
        df["Ingreso"] = pd.to_numeric(df["Ingreso"], errors="coerce").fillna(0)
        df["Egreso"] = pd.to_numeric(df["Egreso"], errors="coerce").fillna(0)
        df.dropna(subset=["Fecha"], inplace=True)

        if df.empty:
            raise ValueError("Los datos de transacciones resultaron vacíos después de la limpieza.")

        # 2. Calcular métricas financieras
        metrics = calculate_financial_metrics(df)

        # 3. Generar el informe con IA
        google_api_key = os.getenv("GOOGLE_API_KEY")
        if not google_api_key:
            raise ValueError("La clave de API de Google (GOOGLE_API_KEY) no está configurada en el servidor.")

        report_text = generate_report(metrics, google_api_key)

        # 4. Actualizar el estado del trabajo con el resultado completo
        analysis_jobs[job_id]["status"] = "completado"
        analysis_jobs[job_id]["result"] = {
            "metrics": metrics,
            "report": report_text,
        }

    except Exception as e:
        # Si algo sale mal, actualizar el estado a "fallido" con el error
        analysis_jobs[job_id]["status"] = "fallido"
        analysis_jobs[job_id]["result"] = {"error": str(e)}


# --- Endpoints de la API ---
@app.post(
    "/api/v1/analysis",
    response_model=AnalysisSubmissionResponse,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Solicitar un nuevo análisis financiero",
    dependencies=[Depends(verify_api_key)],
)
async def request_analysis(
    analysis_request: AnalysisRequest, background_tasks: BackgroundTasks
):
    """
    Inicia un nuevo proceso de análisis financiero.

    - Recibe una lista de transacciones.
    - Valida la clave de API.
    - Inicia el análisis en segundo plano.
    - Devuelve un ID para consultar el resultado posteriormente.
    """
    job_id = str(uuid.uuid4())
    analysis_jobs[job_id] = {"status": "procesando", "result": None}

    # Añadir la tarea de análisis para que se ejecute en segundo plano
    transactions_dict = [t.dict() for t in analysis_request.transactions]
    background_tasks.add_task(run_financial_analysis, job_id, transactions_dict)

    return {
        "message": "Análisis iniciado. Consulta el estado en unos momentos.",
        "analysis_id": job_id,
    }


@app.get(
    "/api/v1/analysis/{analysis_id}",
    response_model=AnalysisStatusResponse,
    status_code=status.HTTP_200_OK,
    summary="Consultar el estado y resultado de un análisis",
    dependencies=[Depends(verify_api_key)],
)
async def get_analysis_status(analysis_id: str):
    """
    Recupera el estado o el resultado de un análisis previamente solicitado.

    - Valida la clave de API.
    - Busca el análisis por su ID.
    - Devuelve el estado actual (`procesando`, `completado`, `fallido`) y el resultado si está disponible.
    """
    job = analysis_jobs.get(analysis_id)
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El ID de análisis no fue encontrado.",
        )

    return {"analysis_id": analysis_id, "status": job["status"], "result": job["result"]}
