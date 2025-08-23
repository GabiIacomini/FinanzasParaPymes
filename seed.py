import asyncio
import pandas as pd
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from decimal import Decimal

from src.db.session import engine, AsyncSessionLocal
from src.db.models import Base, TransactionCategory, User, Transaction
from src.core.security import get_password_hash

# --- Datos Iniciales ---

# Categorías por defecto que se crearán en el sistema
DEFAULT_CATEGORIES = [
    {"name": "Ventas", "type": "income", "color": "#10B981"},
    {"name": "Servicios Profesionales", "type": "income", "color": "#22C55E"},
    {"name": "Salarios", "type": "expense", "color": "#EF4444"},
    {"name": "Alquiler", "type": "expense", "color": "#EAB308"},
    {"name": "Servicios Públicos", "type": "expense", "color": "#F97316"},
    {"name": "Marketing", "type": "expense", "color": "#8B5CF6"},
    {"name": "Software y Suscripciones", "type": "expense", "color": "#3B82F6"},
    {"name": "Insumos de Oficina", "type": "expense", "color": "#6B7280"},
    {"name": "Impuestos", "type": "expense", "color": "#DC2626"},
    {"name": "Otros Egresos", "type": "expense", "color": "#71717A"},
]

# Mapeo simple para convertir las categorías del CSV a las nuevas categorías por defecto
CSV_CATEGORY_MAP = {
    "Ventas": "Ventas",
    "Compra de licencia de software": "Software y Suscripciones",
    "Gastos de Software": "Software y Suscripciones",
    "Gastos Fijos": "Alquiler",
    "Pago de alquiler de oficina": "Alquiler",
    "Salarios": "Salarios",
    "Pago de salarios": "Salarios",
    "Campaña publicitaria en redes": "Marketing",
    "Marketing": "Marketing",
    "Compra de insumos para oficina": "Insumos de Oficina",
    "Gastos Administrativos": "Insumos de Oficina",
    "Servicios de contador": "Servicios Profesionales",
    "Venta de consultoría inicial": "Servicios Profesionales",
    "Venta de consultoría recurrente": "Servicios Profesionales",
    "Venta de consultoría final": "Servicios Profesionales",
    "Venta de producto A": "Ventas",
    "Venta de producto B": "Ventas",
}


async def seed_database():
    """
    Función principal para poblar la base de datos.
    """
    # Crea todas las tablas. En un entorno de desarrollo, es seguro borrar todo primero.
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    # Usa una única sesión para todas las operaciones de seeding
    async with AsyncSessionLocal() as db:
        # 1. Crear las categorías por defecto
        for cat_data in DEFAULT_CATEGORIES:
            category = TransactionCategory(**cat_data, is_default=True)
            db.add(category)
        await db.commit()
        print(f"✅ {len(DEFAULT_CATEGORIES)} categorías por defecto creadas.")

        # 2. Crear un usuario de prueba
        test_user_email = "test@example.com"
        test_user = User(
            username="testuser",
            email=test_user_email,
            hashed_password=get_password_hash("string"),
            company_name="Pyme Ejemplo S.A.",
            tax_id="30-71234567-8",
        )
        db.add(test_user)
        await db.commit()
        await db.refresh(test_user)
        print(f"✅ Usuario de prueba '{test_user.username}' creado.")

        # 3. Cargar transacciones desde el CSV
        try:
            df = pd.read_csv("datos_ejemplo.csv")

            # Obtener las categorías de la BD para mapear por nombre
            all_categories_q = await db.execute(select(TransactionCategory))
            all_categories = all_categories_q.scalars().all()
            category_map = {c.name: c.id for c in all_categories}

            transactions_to_add = []
            for _, row in df.iterrows():
                ingreso = Decimal(row.get("Ingreso", 0))
                egreso = Decimal(row.get("Egreso", 0))

                amount = ingreso if ingreso > 0 else egreso
                trans_type = "income" if ingreso > 0 else "expense"

                csv_cat_name = row["Categoría"]
                db_cat_name = CSV_CATEGORY_MAP.get(csv_cat_name, "Otros Egresos")
                category_id = category_map.get(db_cat_name)

                if not category_id:
                    print(f"⚠️  Advertencia: No se encontró la categoría '{db_cat_name}' para la transacción '{row['Descripción']}'.")
                    continue

                transactions_to_add.append(
                    Transaction(
                        user_id=test_user.id,
                        category_id=category_id,
                        description=row["Descripción"],
                        amount=amount,
                        type=trans_type,
                        date=pd.to_datetime(row["Fecha"], dayfirst=False)
                    )
                )

            db.add_all(transactions_to_add)
            await db.commit()
            print(f"✅ {len(transactions_to_add)} transacciones del CSV cargadas para el usuario '{test_user.username}'.")

        except FileNotFoundError:
            print("ℹ️  No se encontró el archivo 'datos_ejemplo.csv'. Se omite la carga de transacciones de ejemplo.")
        except Exception as e:
            print(f"❌ Error al cargar las transacciones del CSV: {e}")


if __name__ == "__main__":
    print("--- Iniciando el proceso de seeding de la base de datos ---")
    asyncio.run(seed_database())
    print("--- Proceso de seeding finalizado ---")
