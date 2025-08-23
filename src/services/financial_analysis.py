from typing import List, Dict, Any
from decimal import Decimal
from collections import defaultdict
from src.db.models import Transaction

def calculate_financial_metrics(transactions: List[Transaction]) -> Dict[str, Any]:
    """
    Calcula un conjunto de métricas financieras clave a partir de una lista de objetos
    de transacción de SQLAlchemy.

    Args:
        transactions: Una lista de objetos `Transaction` de la base de datos.
                      Se espera que la relación `category` haya sido cargada (eager loaded).

    Returns:
        Un diccionario con las métricas calculadas.
    """
    if not transactions:
        return {
            "total_ingresos": 0,
            "total_egresos": 0,
            "beneficio_neto": 0,
            "margen_beneficio_neto": 0,
            "desglose_egresos": {},
            "periodo_analizado": "N/A"
        }

    total_ingresos = Decimal(0)
    total_egresos = Decimal(0)
    desglose_egresos = defaultdict(Decimal)

    # Determinar el período de análisis
    fechas = [t.date for t in transactions]
    fecha_inicio = min(fechas).strftime('%Y-%m-%d')
    fecha_fin = max(fechas).strftime('%Y-%m-%d')

    for t in transactions:
        if t.type == 'income':
            total_ingresos += t.amount
        elif t.type == 'expense':
            total_egresos += t.amount
            # Asegurarse de que la categoría no sea None
            if t.category:
                desglose_egresos[t.category.name] += t.amount

    # Calcular beneficio y margen
    beneficio_neto = total_ingresos - total_egresos
    margen_beneficio_neto = (beneficio_neto / total_ingresos) * 100 if total_ingresos > 0 else Decimal(0)

    # Ordenar desglose de egresos por monto, de mayor a menor
    desglose_egresos_ordenado = dict(sorted(desglose_egresos.items(), key=lambda item: item[1], reverse=True))

    # Formatear el diccionario final, convirtiendo Decimal a float para serialización JSON
    metrics = {
        "total_ingresos": float(total_ingresos),
        "total_egresos": float(total_egresos),
        "beneficio_neto": float(beneficio_neto),
        "margen_beneficio_neto": float(round(margen_beneficio_neto, 2)),
        "desglose_egresos": {k: float(v) for k, v in desglose_egresos_ordenado.items()},
        "periodo_analizado": f"{fecha_inicio} al {fecha_fin}",
    }

    return metrics
