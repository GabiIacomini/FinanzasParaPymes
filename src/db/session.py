from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from src.core.config import DATABASE_URL

# Crear el motor asíncrono de SQLAlchemy
# `echo=True` es útil para depuración, ya que muestra las consultas SQL generadas.
# Se puede desactivar en producción para un mejor rendimiento.
engine = create_async_engine(DATABASE_URL, echo=True, future=True)

# Crear una fábrica de sesiones asíncronas (Session factory)
# `expire_on_commit=False` es una configuración común para FastAPI,
# ya que evita que los atributos de los objetos SQLAlchemy expiren después de un commit,
# permitiendo acceder a ellos fuera de la sesión (por ejemplo, al retornar el objeto en la respuesta de la API).
AsyncSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

async def get_db() -> AsyncSession:
    """
    Dependencia de FastAPI para obtener una sesión de base de datos.

    Este generador produce una única sesión de base de datos por solicitud
    y se asegura de que se cierre correctamente una vez que la solicitud haya finalizado.
    """
    async with AsyncSessionLocal() as session:
        yield session
