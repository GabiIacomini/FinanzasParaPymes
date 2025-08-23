import uvicorn
import os

def start():
    """
    Punto de entrada para iniciar el servidor de la API en producción.
    Utiliza Uvicorn para correr la aplicación FastAPI definida en `src/api.py`.
    """
    # Obtener el puerto desde las variables de entorno, con un valor por defecto.
    # Replit, por ejemplo, establece la variable PORT automáticamente.
    port = int(os.getenv("PORT", 8000))

    uvicorn.run(
        "src.api:app",
        host="0.0.0.0",
        port=port,
        reload=True  # 'reload=True' es útil para desarrollo, se puede quitar en producción.
    )

if __name__ == "__main__":
    # Verificar que las variables de entorno necesarias estén configuradas antes de iniciar.
    required_vars = ["GOOGLE_API_KEY", "API_SECRET_KEY"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]

    if missing_vars:
        print("Error: Faltan las siguientes variables de entorno requeridas:")
        for var in missing_vars:
            print(f"- {var}")
        print("\nPor favor, configura estas variables (en Replit, usa la pestaña 'Secrets') y vuelve a intentarlo.")
    else:
        print("Iniciando el servidor de la API...")
        start()
