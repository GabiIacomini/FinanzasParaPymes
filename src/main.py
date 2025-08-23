from fastapi import FastAPI
from src.db.session import engine
from src.db.models import Base
# El router principal de la API se importará aquí una vez que se cree.
from src.api.router import api_router

app = FastAPI(
    title="FinTech API - Agente de Análisis Financiero",
    description="API para la aplicación FinTech, proporcionando análisis y gestión financiera para pymes.",
    version="1.0.0",
)

@app.on_event("startup")
async def startup_event():
    """
    Evento que se ejecuta al iniciar la aplicación.
    Crea todas las tablas de la base de datos definidas en los modelos de SQLAlchemy.

    ADVERTENCIA: `create_all` es adecuado para entornos de desarrollo y pruebas.
    Para producción, se debe utilizar un sistema de migración de bases de datos como Alembic
    para gestionar los cambios de esquema de forma segura sin perder datos.
    """
    async with engine.begin() as conn:
        # La siguiente línea borraría todas las tablas al reiniciar. Útil para pruebas.
        # await conn.run_sync(Base.metadata.drop_all)

        # Crea las tablas si no existen.
        await conn.run_sync(Base.metadata.create_all)

# En el siguiente paso, se creará y se incluirá el router principal de la API.
app.include_router(api_router, prefix="/api/v1")

@app.get("/", summary="Health Check", tags=["Status"])
async def root():
    """
    Endpoint principal que se puede usar para verificar que la API está en funcionamiento.
    """
    return {"status": "ok", "message": "Bienvenido a la API de FinTech"}
