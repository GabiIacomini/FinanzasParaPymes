import os
from dotenv import load_dotenv

# Carga las variables de entorno desde un archivo .env
# Es útil para el desarrollo local. En producción, las variables
# se suelen inyectar directamente en el entorno.
load_dotenv()

# URL de conexión a la base de datos.
# Se recomienda usar asyncpg como driver para FastAPI.
# Ejemplo: "postgresql+asyncpg://user:password@host:port/db_name"
DATABASE_URL = os.getenv("DATABASE_URL")

# Clave de API para el servicio de IA de Google
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Clave secreta para proteger los endpoints de nuestra propia API
API_SECRET_KEY = os.getenv("API_SECRET_KEY")

# Tiempo de expiración del token de acceso en minutos
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))


# Validar que las variables críticas estén presentes
if not DATABASE_URL:
    raise RuntimeError("La variable de entorno DATABASE_URL no está configurada.")

if not API_SECRET_KEY:
    raise RuntimeError("La variable de entorno API_SECRET_KEY no está configurada.")
