# Agente de Análisis Financiero para Pymes API

Este proyecto provee una API REST para acceder a un agente de IA capaz de realizar análisis financieros detallados para pequeñas y medianas empresas (pymes).

## Descripción

La API permite a los desarrolladores integrar capacidades de análisis financiero en sus propias aplicaciones. Los usuarios pueden enviar datos transaccionales (ingresos, egresos, etc.) y recibir un informe completo con indicadores clave, interpretaciones y recomendaciones accionables, diseñado para ser comprensible por personas sin formación financiera avanzada.

## Arquitectura de la API REST

La API está diseñada siguiendo los principios de REST, utilizando JSON para el intercambio de datos y códigos de estado HTTP estándar para indicar el resultado de las operaciones.

### Prerrequisitos

Para desplegar y ejecutar este proyecto, necesitarás:

*   Python 3.10 o superior.
*   Una cuenta de [Replit](https://replit.com/) (recomendado para un despliegue sencillo) o un entorno Python local.
*   Una clave de API de Google para el modelo Gemini (puedes obtenerla en [Google AI Studio](https://aistudio.google.com/)).

### Instalación

1.  **Clona el repositorio (si aplica) o carga los archivos en tu entorno.**

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

Para proteger tus claves secretas, debes configurarlas como variables de entorno. Si usas Replit, utiliza la pestaña "Secrets".

*   `GOOGLE_API_KEY`: Tu clave de API para la IA de Google (Gemini).
*   `API_SECRET_KEY`: Una clave secreta que tú defines para proteger el acceso a tu API. Debe ser una cadena de texto larga y aleatoria. Los clientes que consuman la API deberán usar esta clave.

### Ejecución y Despliegue

Para iniciar el servidor de la API, ejecuta el siguiente comando desde la raíz del proyecto:

```bash
uvicorn src.api:app --host 0.0.0.0 --port 8000
```

*   `uvicorn`: Es el servidor ASGI que ejecuta la aplicación.
*   `src.api:app`: Le dice a Uvicorn que encuentre el objeto `app` dentro del archivo `src/api.py`.
*   `--host 0.0.0.0`: Hace que el servidor sea accesible desde fuera del contenedor/máquina.
*   `--port 8000`: Expone la API en el puerto 8000.

En Replit, el servidor se iniciará automáticamente al presionar el botón "Run", siempre que el `main.py` esté configurado para lanzar Uvicorn.

## Uso de la API (Documentación para Desarrolladores)

### URL Base

La URL base para todos los endpoints de la API es:

```
https://<tu-dominio-de-replit-o-servidor>/api/v1
```

### Autenticación

La API utiliza un esquema de autenticación por clave de API. Todas las solicitudes deben incluir un encabezado `X-API-Key` con tu `API_SECRET_KEY` secreta.

**Ejemplo de encabezado:**
`X-API-Key: tu_clave_secreta_muy_larga_y_segura`

Si la clave es incorrecta o no se proporciona, la API devolverá un error `401 Unauthorized`.

### Endpoints

#### 1. Solicitar un nuevo análisis

Inicia un nuevo proceso de análisis financiero. Dado que el análisis puede tardar varios segundos, la API funciona de forma asíncrona. Se envía la tarea y se recibe un ID para consultar el resultado más tarde.

*   **Endpoint:** `POST /analysis`
*   **Descripción:** Envía una lista de transacciones financieras para ser analizadas.
*   **Cuerpo de la Solicitud (Request Body):**

    ```json
    {
      "transactions": [
        {
          "Fecha": "2024-01-05",
          "Descripción": "Venta de servicio de consultoría",
          "Categoría": "Ventas",
          "Ingreso": 50000,
          "Egreso": 0
        },
        {
          "Fecha": "2024-01-15",
          "Descripción": "Pago de alquiler de oficina",
          "Categoría": "Gasto Fijo",
          "Ingreso": 0,
          "Egreso": 25000
        },
        {
          "Fecha": "2024-01-25",
          "Descripción": "Salarios del personal",
          "Categoría": "Gasto Fijo",
          "Ingreso": 0,
          "Egreso": 40000
        }
      ]
    }
    ```

*   **Respuesta Exitosa (202 Accepted):**

    ```json
    {
      "message": "Análisis iniciado. Consulta el estado en unos momentos.",
      "analysis_id": "a1b2c3d4-e5f6-7890-1234-567890abcdef"
    }
    ```

*   **Respuestas de Error:**
    *   `400 Bad Request`: Si el cuerpo de la solicitud es inválido (ej. JSON mal formado, campos faltantes).
    *   `401 Unauthorized`: Si la `X-API-Key` es inválida o no se proporciona.

#### 2. Consultar el estado y resultado de un análisis

Recupera el estado o el informe final de un análisis previamente solicitado.

*   **Endpoint:** `GET /analysis/{analysis_id}`
*   **Descripción:** Consulta el resultado usando el ID devuelto por la solicitud POST.
*   **Parámetros de URL:**
    *   `analysis_id` (string, requerida): El identificador único del análisis.

*   **Respuesta (Análisis en Proceso - 200 OK):**

    ```json
    {
      "analysis_id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
      "status": "procesando",
      "result": null
    }
    ```

*   **Respuesta (Análisis Completado - 200 OK):**

    ```json
    {
      "analysis_id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
      "status": "completado",
      "result": {
        "metrics": {
            "total_ingresos": 50000.0,
            "total_egresos": 65000.0,
            "beneficio_neto": -15000.0,
            "margen_beneficio_neto": -30.0,
            "desglose_egresos": {
                "Gasto Fijo": 65000.0
            },
            "periodo_analizado": "2024-01-05 al 2024-01-25"
        },
        "report": "--- \n\n### Análisis Financiero para tu Pyme...\n\n (El informe completo en Markdown generado por la IA) \n\n---"
      }
    }
    ```

*   **Respuestas de Error:**
    *   `401 Unauthorized`: Si la `X-API-Key` es inválida.
    *   `404 Not Found`: Si el `analysis_id` no existe.
    *   `500 Internal Server Error`: Si ocurrió un error inesperado durante el análisis.

### Ejemplos de Uso

#### Con `curl`

1.  **Solicitar el análisis:**
    ```bash
    curl -X POST "https://<tu-dominio-de-replit>/api/v1/analysis" \
    -H "Content-Type: application/json" \
    -H "X-API-Key: tu_clave_secreta_muy_larga_y_segura" \
    -d '{
      "transactions": [
        {"Fecha": "2024-01-05", "Descripción": "Venta", "Categoría": "Ventas", "Ingreso": 50000, "Egreso": 0},
        {"Fecha": "2024-01-15", "Descripción": "Alquiler", "Categoría": "Gasto Fijo", "Ingreso": 0, "Egreso": 25000}
      ]
    }'
    ```

2.  **Consultar el resultado (usando el `analysis_id` recibido):**
    ```bash
    curl -X GET "https://<tu-dominio-de-replit>/api/v1/analysis/a1b2c3d4-e5f6-7890-1234-567890abcdef" \
    -H "X-API-Key: tu_clave_secreta_muy_larga_y_segura"
    ```

#### Con Python (`requests`)

```python
import requests
import time
import os

# --- Configuración ---
BASE_URL = "https://<tu-dominio-de-replit>/api/v1"  # Reemplaza con tu URL
API_KEY = os.getenv("API_SECRET_KEY") # Es una buena práctica usar variables de entorno

if not API_KEY:
    raise ValueError("La variable de entorno API_SECRET_KEY no está configurada.")

headers = {
    "Content-Type": "application/json",
    "X-API-Key": API_KEY,
}

payload = {
    "transactions": [
        {"Fecha": "2024-01-05", "Descripción": "Venta", "Categoría": "Ventas", "Ingreso": 80000, "Egreso": 0},
        {"Fecha": "2024-01-15", "Descripción": "Alquiler", "Categoría": "Gasto Fijo", "Ingreso": 0, "Egreso": 30000},
        {"Fecha": "2024-01-25", "Descripción": "Salarios", "Categoría": "Gasto Fijo", "Ingreso": 0, "Egreso": 45000}
    ]
}

# 1. Iniciar el análisis
try:
    response = requests.post(f"{BASE_URL}/analysis", json=payload, headers=headers)
    response.raise_for_status()  # Lanza una excepción para códigos de error HTTP

    data = response.json()
    analysis_id = data["analysis_id"]
    print(f"Análisis iniciado con éxito. ID: {analysis_id}")

    # 2. Consultar el resultado en un bucle
    while True:
        print("Consultando estado del análisis...")
        result_response = requests.get(f"{BASE_URL}/analysis/{analysis_id}", headers=headers)
        result_response.raise_for_status()

        result_data = result_response.json()

        if result_data["status"] == "completado":
            print("\n--- ¡Análisis Completado! ---")
            print(result_data["result"]["report"])
            break
        elif result_data["status"] == "fallido":
            print("\nEl análisis ha fallado.")
            print(result_data.get("result"))
            break

        print("El análisis aún está en proceso. Esperando 10 segundos...")
        time.sleep(10)

except requests.exceptions.HTTPError as http_err:
    print(f"Error HTTP: {http_err}")
    print(f"Cuerpo de la respuesta: {http_err.response.text}")
except Exception as err:
    print(f"Ocurrió otro error: {err}")

```

## Términos Legales y de Cumplimiento (Argentina)

El uso de esta API está sujeto a los siguientes términos, diseñados para cumplir con el marco regulatorio argentino.

### Aclaración sobre el Alcance del Análisis (Normativa CNV)

El servicio de análisis financiero proporcionado a través de esta API tiene como único propósito el de ser una **herramienta informativa y de apoyo a la gestión interna** de la empresa. Los informes, métricas y recomendaciones generados por el agente de IA **no constituyen, bajo ninguna circunstancia, una recomendación de inversión, asesoramiento financiero, ni una oferta pública o privada de valores** según lo definido por la Ley N° 26.831 del Mercado de Capitales y las normativas de la Comisión Nacional de Valores (CNV) de Argentina. La interpretación y el uso de la información proporcionada son responsabilidad exclusiva del usuario final.

### Política de Uso y Protección de Datos Personales (Ley 25.326)

Al utilizar esta API, usted y su aplicación aceptan las siguientes condiciones en cumplimiento de la Ley de Protección de Datos Personales N° 25.326:

*   **Consentimiento del Titular:** La aplicación o sistema que consume esta API **es la única responsable de obtener el consentimiento previo, expreso e informado** del titular de los datos (el usuario final o la empresa) para la recolección y tratamiento de su información financiera con el fin de realizar el análisis.
*   **Finalidad y Confidencialidad:** Los datos enviados a través de la API serán utilizados exclusivamente para la finalidad de generar el análisis financiero solicitado. Nos comprometemos a tratar dicha información como **estrictamente confidencial** y a no compartirla con terceros no autorizados, salvo obligación legal.
*   **Medidas de Seguridad:** Se implementan medidas de seguridad técnicas y organizativas para proteger la información. Todos los datos en tránsito están **cifrados mediante el protocolo HTTPS**. Las claves de API y otros secretos se gestionan de forma segura.
*   **Principio de Calidad y Anonimización:** Se recomienda encarecidamente que, siempre que sea posible, los datos enviados a la API sean **previamente anonimizados o seudonimizados**. Evite enviar información personal identificable (como nombres de clientes, CUITs personales, etc.) en campos como "Descripción". La responsabilidad de garantizar la calidad y minimización de los datos recae en la aplicación cliente.
*   **Derechos del Titular:** La aplicación cliente debe garantizar un canal para que el titular de los datos pueda ejercer sus derechos de acceso, rectificación y supresión.
