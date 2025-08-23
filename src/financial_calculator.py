import pandas as pd
from typing import Dict, Any

def calculate_financial_metrics(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Calcula un conjunto de métricas financieras clave a partir de un DataFrame de transacciones.

    Args:
        df: DataFrame validado que contiene las transacciones financieras.
            Debe tener las columnas 'Ingreso' y 'Egreso'.

    Returns:
        Un diccionario con las métricas calculadas.
    """
    if df.empty:
        return {
            "total_ingresos": 0,
            "total_egresos": 0,
            "beneficio_neto": 0,
            "margen_beneficio_neto": 0,
            "desglose_egresos": {},
            "periodo_analizado": "N/A"
        }

    # 1. Calcular totales
    total_ingresos = df["Ingreso"].sum()
    total_egresos = df["Egreso"].sum()

    # 2. Calcular Beneficio Neto (simplificado)
    beneficio_neto = total_ingresos - total_egresos

    # 3. Calcular Margen de Beneficio Neto
    # Evitar división por cero si no hay ingresos
    if total_ingresos > 0:
        margen_beneficio_neto = (beneficio_neto / total_ingresos) * 100
    else:
        margen_beneficio_neto = 0

    # 4. Calcular desglose de egresos por categoría
    desglose_egresos = df[df['Egreso'] > 0].groupby("Categoría")["Egreso"].sum().to_dict()

    # Ordenar el desglose para mostrar las categorías más importantes primero
    desglose_egresos_ordenado = dict(sorted(desglose_egresos.items(), key=lambda item: item[1], reverse=True))

    # Convertir los valores del desglose a float nativo de Python
    desglose_egresos_serializable = {k: float(v) for k, v in desglose_egresos_ordenado.items()}

    # 5. Determinar el período de análisis
    fecha_inicio = df['Fecha'].min().strftime('%Y-%m-%d')
    fecha_fin = df['Fecha'].max().strftime('%Y-%m-%d')
    periodo_analizado = f"{fecha_inicio} al {fecha_fin}"


    metrics = {
        "total_ingresos": float(total_ingresos),
        "total_egresos": float(total_egresos),
        "beneficio_neto": float(beneficio_neto),
        "margen_beneficio_neto": float(margen_beneficio_neto),
        "desglose_egresos": desglose_egresos_serializable,
        "periodo_analizado": periodo_analizado,
    }

    return metrics

if __name__ == '__main__':
    # Bloque de prueba para verificar que las funciones operan correctamente
    print("Ejecutando pruebas para financial_calculator.py...")

    # Crear un DataFrame de prueba
    test_data = {
        "Fecha": pd.to_datetime(["2024-01-05", "2024-01-15", "2024-01-20", "2024-01-25", "2024-01-30"]),
        "Descripción": ["Venta de servicio", "Pago de alquiler", "Venta de producto", "Salarios", "Publicidad"],
        "Categoría": ["Ventas", "Gasto Fijo", "Ventas", "Gasto Fijo", "Gasto Variable"],
        "Ingreso": [50000, 0, 30000, 0, 0],
        "Egreso": [0, 25000, 0, 40000, 5000]
    }
    test_df = pd.DataFrame(test_data)

    # Calcular métricas
    calculated_metrics = calculate_financial_metrics(test_df)

    # Imprimir resultados para verificación
    import json
    print("\nMétricas Calculadas:")
    print(json.dumps(calculated_metrics, indent=2))

    # Verificaciones (assertions)
    assert calculated_metrics["total_ingresos"] == 80000
    assert calculated_metrics["total_egresos"] == 70000
    assert calculated_metrics["beneficio_neto"] == 10000
    assert abs(calculated_metrics["margen_beneficio_neto"] - 12.5) < 0.01
    assert calculated_metrics["desglose_egresos"]["Gasto Fijo"] == 65000

    print("\n¡Todas las pruebas pasaron exitosamente!")
