import uuid
from sqlalchemy import (
    create_engine,
    Column,
    String,
    Text,
    TIMESTAMP,
    Numeric,
    Integer,
    Boolean,
    ForeignKey,
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func, text

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(
        UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()")
    )
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)
    company_name = Column("company_name", String, nullable=False)
    tax_id = Column("tax_id", String)
    preferred_currency = Column("preferred_currency", String, server_default="ARS")
    created_at = Column(
        "created_at", TIMESTAMP, server_default=func.now(), nullable=False
    )

    transactions = relationship("Transaction", back_populates="user")
    ai_insights = relationship("AiInsight", back_populates="user")
    cash_flow_projections = relationship("CashFlowProjection", back_populates="user")
    notifications = relationship("Notification", back_populates="user")
    audit_logs = relationship("AuditLog", back_populates="user")


class TransactionCategory(Base):
    __tablename__ = "transaction_categories"

    id = Column(
        UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()")
    )
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)  # 'income' or 'expense'
    is_default = Column("is_default", Boolean, server_default="false", nullable=False)
    color = Column(String, server_default="#6B7280")

    transactions = relationship("Transaction", back_populates="category")


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(
        UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()")
    )
    user_id = Column("user_id", UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    category_id = Column(
        "category_id",
        UUID(as_uuid=True),
        ForeignKey("transaction_categories.id"),
        nullable=False,
    )
    description = Column(String, nullable=False)
    amount = Column(Numeric(15, 2), nullable=False)
    currency = Column(String, nullable=False, server_default="ARS")
    type = Column(String, nullable=False)  # 'income' or 'expense'
    date = Column(TIMESTAMP, nullable=False)
    created_at = Column(
        "created_at", TIMESTAMP, server_default=func.now(), nullable=False
    )

    user = relationship("User", back_populates="transactions")
    category = relationship("TransactionCategory", back_populates="transactions")


class InflationData(Base):
    __tablename__ = "inflation_data"

    id = Column(
        UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()")
    )
    month = Column(Integer, nullable=False)
    year = Column(Integer, nullable=False)
    rate = Column(Numeric(5, 2), nullable=False)
    source = Column(String, server_default="INDEC")
    created_at = Column(
        "created_at", TIMESTAMP, server_default=func.now(), nullable=False
    )


class AiInsight(Base):
    __tablename__ = "ai_insights"

    id = Column(
        UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()")
    )
    user_id = Column("user_id", UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    type = Column(String, nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    priority = Column(String, server_default="medium")
    is_read = Column("is_read", Boolean, server_default="false", nullable=False)
    json_metadata = Column("metadata", JSONB)
    created_at = Column(
        "created_at", TIMESTAMP, server_default=func.now(), nullable=False
    )

    user = relationship("User", back_populates="ai_insights")


class CashFlowProjection(Base):
    __tablename__ = "cash_flow_projections"

    id = Column(
        UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()")
    )
    user_id = Column("user_id", UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    date = Column(TIMESTAMP, nullable=False)
    projected_income = Column("projected_income", Numeric(15, 2), nullable=False)
    projected_expenses = Column("projected_expenses", Numeric(15, 2), nullable=False)
    net_flow = Column("net_flow", Numeric(15, 2), nullable=False)
    created_at = Column(
        "created_at", TIMESTAMP, server_default=func.now(), nullable=False
    )

    user = relationship("User", back_populates="cash_flow_projections")


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(
        UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()")
    )
    user_id = Column("user_id", UUID(as_uuid=True), ForeignKey("users.id"))
    action = Column(String, nullable=False)
    table_name = Column("table_name", String, nullable=False)
    record_id = Column("record_id", String)
    old_values = Column("old_values", JSONB)
    new_values = Column("new_values", JSONB)
    ip_address = Column("ip_address", String)
    user_agent = Column("user_agent", String)
    created_at = Column(
        "created_at", TIMESTAMP, server_default=func.now(), nullable=False
    )

    user = relationship("User", back_populates="audit_logs")


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(
        UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()")
    )
    user_id = Column("user_id", UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    type = Column(String, nullable=False)
    title = Column(String, nullable=False)
    message = Column(Text, nullable=False)
    priority = Column(String, server_default="medium")
    is_read = Column("is_read", Boolean, server_default="false", nullable=False)
    action_url = Column("action_url", String)
    action_text = Column("action_text", String)
    json_metadata = Column("metadata", JSONB)
    expires_at = Column("expires_at", TIMESTAMP)
    created_at = Column(
        "created_at", TIMESTAMP, server_default=func.now(), nullable=False
    )

    user = relationship("User", back_populates="notifications")
