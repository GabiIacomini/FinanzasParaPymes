import os
import json
import google.generativeai as genai
from typing import Dict, Any

def generate_report(metrics: Dict[str, Any], api_key: str) -> str:
    """
    Genera un informe financiero narrativo utilizando la API de Gemini.

    Args:
        metrics: Un diccionario con las métricas financieras calculadas.
        api_key: La clave de API para Google Gemini.

    Returns:
        Una cadena de texto con el informe generado.
    """
    if not api_key:
        raise ValueError("La clave de API de Google no fue proporcionada.")

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')

    # Formatear las métricas para que sean fáciles de leer en el prompt
    formatted_metrics = json.dumps(metrics, indent=2, ensure_ascii=False)

    prompt = f"""
    **Misión:** Eres "FinanzasClaras", un asesor financiero experto en pymes de Argentina. Tu objetivo es analizar un conjunto de métricas financieras y generar un informe claro, accionable y pedagógico para un empresario que no tiene conocimientos financieros avanzados. Tu tono debe ser profesional pero cercano, alentador y siempre enfocado en dar los próximos pasos.

    **Contexto:** Has recibido las siguientes métricas financieras para una pyme. Los valores monetarios están en Pesos Argentinos (ARS).

    **Métricas a Analizar:**
    ```json
    {formatted_metrics}
    ```

    **Estructura Obligatoria del Informe:**
    Basándote *únicamente* en los datos proporcionados, genera un informe con el siguiente formato exacto en Markdown:

    ---

    ### Análisis Financiero para tu Pyme
    **Período Analizado:** {metrics.get("periodo_analizado", "N/A")}

    **1. Resumen Ejecutivo (El Vistazo Rápido)**
    *   Escribe 2 o 3 viñetas concisas con los hallazgos más importantes. Empieza con lo bueno y luego lo que hay que mejorar. Sé directo y claro.

    **2. Salud Financiera General**
    *   Proporciona una calificación cualitativa (ej: "Sólida", "Mejorable", "En Riesgo") y justifica brevemente por qué, basándote en el balance entre ingresos, egresos y rentabilidad.

    **3. Análisis Detallado por Área**
    *   **Rentabilidad:** Analiza el Margen de Beneficio Neto. Explica en términos sencillos qué significa el resultado de `{metrics.get('margen_beneficio_neto', 0):.2f}%`. Compara los ingresos totales con los egresos totales.
    *   **Gestión de Gastos:** Analiza el desglose de egresos. Menciona las 2 o 3 categorías de gastos más importantes y su peso relativo. Explica qué significa esto para la estructura de costos del negocio.

    **4. Recomendaciones y Planes de Acción**
    *   Basado en el análisis, proporciona 2 recomendaciones claras y accionables.
    *   Para cada recomendación, detalla 2 o 3 pasos prácticos que el empresario puede tomar. Por ejemplo, si el beneficio es bajo, recomienda "Revisar la estrategia de precios" o "Auditar los costos de los proveedores principales". Si los gastos fijos son muy altos, sugiere formas de optimizarlos.

    ---
    """

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error al generar el informe con la API de Gemini: {e}"

if __name__ == '__main__':
    print("Ejecutando pruebas para report_generator.py...")

    # Para esta prueba, se requiere una clave de API de Google.
    # El usuario debe establecer la variable de entorno GOOGLE_API_KEY.
    api_key_from_env = os.getenv("GOOGLE_API_KEY")

    if not api_key_from_env:
        print("\nADVERTENCIA: La variable de entorno GOOGLE_API_KEY no está configurada.")
        print("La prueba de integración con la API de Gemini será omitida.")
    else:
        print("\nClave de API encontrada. Procediendo con la prueba de integración...")
        # Usar un conjunto de métricas de ejemplo
        sample_metrics = {
            "total_ingresos": 305000.0,
            "total_egresos": 440000.0,
            "beneficio_neto": -135000.0,
            "margen_beneficio_neto": -44.26,
            "desglose_egresos": {
                "Salarios": 270000.0,
                "Gastos Fijos": 150000.0,
                "Marketing": 22000.0,
                "Servicios Profesionales": 25000.0,
                "Gastos de Software": 15000.0,
                "Gastos Administrativos": 8000.0
            },
            "periodo_analizado": "2024-01-05 al 2024-03-29"
        }

        reporte_generado = generate_report(sample_metrics, api_key_from_env)

        print("\n--- INICIO DEL REPORTE GENERADO ---")
        print(reporte_generado)
        print("--- FIN DEL REPORTE GENERADO ---\n")

        if "Error" not in reporte_generado and "Salud Financiera" in reporte_generado:
            print("Prueba de generación de informe parece exitosa.")
        else:
            print("La prueba de generación de informe pudo haber fallado.")
