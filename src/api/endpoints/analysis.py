from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from typing import List

from src.db.session import get_db
from src.db.models import Transaction as TransactionModel, User as UserModel, AiInsight as AiInsightModel
from src.schemas.ai_insight import AiInsight as AiInsightSchema
from src.core.security import get_current_user
from src.services.financial_analysis import calculate_financial_metrics
from src.services.report_generator import generate_report
from src.core.config import GOOGLE_API_KEY


router = APIRouter()

async def run_analysis_and_save(db: AsyncSession, user: UserModel):
    """
    Función de servicio que se ejecuta en segundo plano para:
    1. Obtener las transacciones del usuario.
    2. Calcular las métricas financieras.
    3. Generar un informe con IA.
    4. Guardar el resultado como un nuevo "insight" en la base de datos.
    """
    # 1. Obtener las transacciones del usuario, cargando las categorías relacionadas
    #    para evitar consultas N+1.
    stmt = (
        select(TransactionModel)
        .where(TransactionModel.user_id == user.id)
        .options(selectinload(TransactionModel.category))
    )
    result = await db.execute(stmt)
    transactions = result.scalars().all()

    if not transactions:
        print(f"No se encontraron transacciones para el usuario {user.id}. No se genera análisis.")
        # En una app real, se podría crear una notificación para el usuario.
        return

    # 2. Calcular métricas
    metrics = calculate_financial_metrics(transactions)

    # 3. Generar informe con IA
    if not GOOGLE_API_KEY or GOOGLE_API_KEY == "TU_CLAVE_DE_API_DE_GOOGLE_AQUI":
        print("ADVERTENCIA: La clave de API de Google no está configurada. No se puede generar el informe de IA.")
        report_text = "El informe de IA no pudo ser generado porque la clave de API de Google no está configurada en el servidor."
    else:
        try:
            report_text = generate_report(metrics, GOOGLE_API_KEY)
        except Exception as e:
            print(f"Error al generar el informe de IA: {e}")
            report_text = f"Ocurrió un error al generar el informe: {e}"

    # 4. Guardar el resultado en la tabla de insights
    insight = AiInsightModel(
        user_id=user.id,
        type="financial_summary",
        title="Resumen Financiero Automático",
        description=report_text,
        priority="medium",
        json_metadata=metrics,
    )
    db.add(insight)
    await db.commit()
    print(f"Análisis financiero completado y guardado para el usuario {user.id}.")


@router.post("/", status_code=status.HTTP_202_ACCEPTED, summary="Solicitar un nuevo análisis financiero")
async def request_financial_analysis(
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    """
    Inicia un análisis financiero para el usuario actual.

    El proceso se ejecuta en segundo plano para no bloquear la respuesta de la API.
    """
    print(f"Iniciando análisis financiero en segundo plano para el usuario {current_user.id}...")
    background_tasks.add_task(run_analysis_and_save, db, current_user)
    return {"message": "El análisis financiero ha sido iniciado. Los resultados estarán disponibles en breve."}


@router.get("/", response_model=List[AiInsightSchema], summary="Obtener los análisis financieros (insights)")
async def get_financial_analyses(
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """
    Obtiene la lista de todos los análisis (insights) generados para el usuario actual.
    """
    result = await db.execute(
        select(AiInsightModel)
        .where(AiInsightModel.user_id == current_user.id)
        .order_by(AiInsightModel.created_at.desc())
    )
    insights = result.scalars().all()
    return insights
