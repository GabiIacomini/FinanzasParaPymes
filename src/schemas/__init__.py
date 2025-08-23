# Este archivo convierte al directorio 'schemas' en un paquete de Python.
# Esto nos permite importar los esquemas desde otros módulos de la aplicación
# de forma organizada, por ejemplo:
# from src.schemas.user import User, UserCreate

from .user import User, UserCreate, UserInDB
from .transaction_category import TransactionCategory, TransactionCategoryCreate
from .transaction import Transaction, TransactionCreate
from .ai_insight import AiInsight, AiInsightCreate
from .token import Token, TokenData
