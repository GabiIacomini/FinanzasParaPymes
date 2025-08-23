from fastapi import APIRouter
from src.api.endpoints import (
    users,
    login,
    transaction_categories,
    transactions,
    analysis,
)

api_router = APIRouter()

# Incluir los routers de los diferentes endpoints en el router principal de la API.
# Se les asigna un prefijo y etiquetas para agruparlos en la documentación de OpenAPI.
api_router.include_router(login.router, tags=["Login"], prefix="/login")
api_router.include_router(users.router, tags=["Users"], prefix="/users")
api_router.include_router(
    transaction_categories.router,
    tags=["Transaction Categories"],
    prefix="/transaction-categories",
)
api_router.include_router(
    transactions.router, tags=["Transactions"], prefix="/transactions"
)
api_router.include_router(analysis.router, tags=["Analysis"], prefix="/analysis")
