# Agente de Análisis Financiero para Pymes API

Este proyecto provee una API REST para acceder a un agente de IA capaz de realizar análisis financieros detallados para pequeñas y medianas empresas (pymes). La API ahora cuenta con un sistema de autenticación de usuarios y persistencia de datos en una base de datos PostgreSQL.

## Descripción

La API permite a los desarrolladores integrar capacidades de análisis financiero en sus propias aplicaciones. Los usuarios pueden registrarse, gestionar sus transacciones (ingresos, egresos, etc.) y recibir informes completos con indicadores clave, interpretaciones y recomendaciones accionables, diseñados para ser comprensibles por personas sin formación financiera avanzada.

### Arquitectura de la API REST

La API está diseñada siguiendo los principios de REST, utilizando JSON para el intercambio de datos y códigos de estado HTTP estándar. Utiliza una base de datos PostgreSQL para almacenar todos los datos y Alembic para gestionar las migraciones del esquema.

### Prerrequisitos

*   Python 3.10 o superior.
*   Una clave de API de Google para el modelo Gemini (puedes obtenerla en [Google AI Studio](https://aistudio.google.com/)).
*   Una base de datos PostgreSQL en funcionamiento. Puedes usar un servicio en la nube como [Supabase](https://supabase.com/) o [Neon](https://neon.tech/) que ofrecen capas gratuitas.

### Instalación

1.  **Clona el repositorio.**

2.  **Crea un entorno virtual (recomendado):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # En Windows: venv\Scripts\activate
    ```

3.  **Instala las dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

### Configuración de Variables de Entorno

Crea un archivo `.env` en la raíz del proyecto o configura las variables directamente en tu entorno de despliegue.

*   `DATABASE_URL`: La URL de conexión a tu base de datos PostgreSQL. Debe incluir el driver `asyncpg`.
    *   *Ejemplo*: `postgresql+asyncpg://user:password@host:port/dbname`
*   `GOOGLE_API_KEY`: Tu clave de API para la IA de Google (Gemini).
*   `API_SECRET_KEY`: Una clave secreta larga y aleatoria que defines para la firma de tokens JWT.
*   `ACCESS_TOKEN_EXPIRE_MINUTES`: (Opcional) El tiempo de vida de los tokens de acceso en minutos. Por defecto es `30`.

### Base de Datos y Migraciones

El proyecto utiliza **SQLAlchemy** como ORM y **Alembic** para gestionar las migraciones de la base de datos.

Una vez que hayas configurado tu `DATABASE_URL`, debes aplicar las migraciones para crear todas las tablas necesarias en tu base de datos. Ejecuta el siguiente comando desde la raíz del proyecto:

```bash
alembic upgrade head
```

Este comando aplicará todos los scripts de migración pendientes que se encuentran en el directorio `alembic/versions`.

### Ejecución y Despliegue

Para iniciar el servidor de la API, ejecuta el siguiente comando desde la raíz del proyecto:

```bash
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```
*   `uvicorn`: Es el servidor ASGI que ejecuta la aplicación.
*   `src.main:app`: Le dice a Uvicorn que encuentre el objeto `app` dentro del archivo `src/main.py`.

## Uso de la API

La API ahora utiliza autenticación por token (OAuth2/JWT). Para acceder a los endpoints protegidos, primero debes registrar un usuario y luego obtener un token de acceso.

### Autenticación

1.  **Registrar un nuevo usuario:** `POST /api/v1/users/`
2.  **Obtener un token:** `POST /api/v1/login/token`
    -   Envía tu `username` y `password` en un formulario (`x-www-form-urlencoded`).
    -   La respuesta contendrá un `access_token`.
3.  **Usar el token:** Incluye el token en el encabezado de autorización de tus solicitudes a endpoints protegidos.
    -   **Ejemplo de encabezado:** `Authorization: Bearer <tu_access_token>`

### Endpoints Principales

La URL base para todos los endpoints es `https://<tu-dominio>/api/v1`.

*   `/login`: Endpoints para la autenticación y obtención de tokens.
*   `/users`: Para crear y gestionar usuarios.
*   `/transactions`: Para crear, leer, actualizar y eliminar las transacciones financieras del usuario autenticado.
*   `/transaction-categories`: Para gestionar las categorías de las transacciones.
*   `/analysis`: Para solicitar análisis financieros basados en las transacciones del usuario.

Puedes explorar todos los endpoints y sus detalles interactuando con la documentación de Swagger UI que se genera automáticamente en la ruta `/docs` de tu API (ej. `http://127.0.0.1:8000/docs`).

## Términos Legales y de Cumplimiento (Argentina)

(Las secciones legales y de cumplimiento se mantienen sin cambios)

### Aclaración sobre el Alcance del Análisis (Normativa CNV)
...

### Política de Uso y Protección de Datos Personales (Ley 25.326)
...
