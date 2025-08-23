import os
import argparse
from data_loader import load_financial_data
from financial_calculator import calculate_financial_metrics
from report_generator import generate_report

def main():
    """
    Orquesta el proceso completo del agente de análisis financiero.
    """
    # 1. Configurar el parser de argumentos para la línea de comandos
    parser = argparse.ArgumentParser(
        description="Agente de IA para Análisis Financiero de Pymes."
    )
    parser.add_argument(
        "filepath",
        type=str,
        help="La ruta al archivo CSV con los datos financieros.",
    )
    args = parser.parse_args()

    # 2. Obtener la clave de API desde las variables de entorno
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("Error: La variable de entorno 'GOOGLE_API_KEY' no está configurada.")
        print("Por favor, establece tu clave de API de Google para continuar.")
        return

    print(f"Iniciando análisis para el archivo: {args.filepath}...")

    try:
        # 3. Cargar y validar los datos
        print("Paso 1: Cargando y validando datos...")
        financial_df = load_financial_data(args.filepath)
        print("Datos cargados exitosamente.")

        # 4. Calcular las métricas financieras
        print("Paso 2: Calculando métricas financieras...")
        metrics = calculate_financial_metrics(financial_df)
        print("Métricas calculadas exitosamente.")

        # 5. Generar el informe narrativo
        print("Paso 3: Generando informe con IA (esto puede tardar un momento)...")
        report = generate_report(metrics, api_key)
        print("Informe generado exitosamente.")

        # 6. Presentar el informe final
        print("\n" + "="*80)
        print(" " * 25 + "INFORME DE ANÁLISIS FINANCIERO")
        print("="*80 + "\n")
        print(report)
        print("\n" + "="*80)
        print(" " * 30 + "FIN DEL INFORME")
        print("="*80 + "\n")

    except (FileNotFoundError, ValueError) as e:
        # Capturar errores de carga de datos o de la API y mostrarlos de forma amigable
        print(f"\nError en el procesamiento: {e}")
    except Exception as e:
        print(f"\nOcurrió un error inesperado: {e}")

if __name__ == "__main__":
    main()
