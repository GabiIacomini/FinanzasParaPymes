import pandas as pd
from typing import List

def load_financial_data(filepath: str) -> pd.DataFrame:
    """
    Carga datos financieros desde un archivo CSV, los valida y los limpia.

    Args:
        filepath: La ruta al archivo CSV.

    Returns:
        Un DataFrame de pandas con los datos financieros limpios.

    Raises:
        FileNotFoundError: Si el archivo no se encuentra en la ruta especificada.
        ValueError: Si al archivo le faltan columnas requeridas.
    """
    required_columns: List[str] = [
        "Fecha",
        "Descripción",
        "Categoría",
        "Ingreso",
        "Egreso",
    ]

    try:
        df = pd.read_csv(filepath)
    except FileNotFoundError:
        raise FileNotFoundError(f"Error: El archivo no fue encontrado en la ruta '{filepath}'")

    # Validar que todas las columnas requeridas existan
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Error: Faltan las siguientes columnas en el archivo: {', '.join(missing_columns)}")

    # --- Limpieza y formateo de datos ---

    # Convertir columnas de moneda a tipo numérico, reemplazando errores con 0
    df["Ingreso"] = pd.to_numeric(df["Ingreso"], errors="coerce").fillna(0)
    df["Egreso"] = pd.to_numeric(df["Egreso"], errors="coerce").fillna(0)

    # Convertir la columna de fecha a tipo datetime
    df["Fecha"] = pd.to_datetime(df["Fecha"], errors="coerce")

    # Eliminar filas donde la fecha no se pudo convertir
    df.dropna(subset=["Fecha"], inplace=True)

    return df

if __name__ == '__main__':
    # Ejemplo de uso y prueba rápida (se ejecutará solo si se corre este archivo directamente)
    try:
        # Para esta prueba, necesitamos un archivo de ejemplo.
        # Lo crearemos en el siguiente paso del plan.
        # Por ahora, este bloque solo sirve como demostración.
        print("Creando un archivo de prueba temporal 'temp_test_data.csv'...")
        test_data = {
            "Fecha": ["2024-01-01", "2024-01-02", "2024-01-03"],
            "Descripción": ["Venta inicial", "Compra de material", "Venta producto B"],
            "Categoría": ["Venta", "Costo", "Venta"],
            "Ingreso": [1000, "texto_invalido", 2000],
            "Egreso": [0, 500, 0]
        }
        test_df = pd.DataFrame(test_data)
        test_df.to_csv("temp_test_data.csv", index=False)

        print("Probando la función load_financial_data...")
        df_cargado = load_financial_data("temp_test_data.csv")
        print("¡El archivo se cargó y validó correctamente!")
        print("Primeras filas del DataFrame cargado:")
        print(df_cargado.head())
        print("\nTipos de datos del DataFrame:")
        print(df_cargado.info())

    except (FileNotFoundError, ValueError) as e:
        print(e)
    finally:
        # Limpiar el archivo temporal
        import os
        if os.path.exists("temp_test_data.csv"):
            os.remove("temp_test_data.csv")
            print("\nArchivo de prueba temporal eliminado.")
