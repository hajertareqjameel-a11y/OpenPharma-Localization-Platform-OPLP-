from sqlalchemy import Column, String, Boolean, Numeric, CHAR, Date, Float, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
import uuid
from app.models.base import Base

class ActiveIngredient(Base):
    __tablename__ = "active_ingredients"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    manufacturing_complexity = Column(String(20), nullable=True)
    patent_status = Column(String(20), nullable=True)
    patent_expiry_date = Column(Date, nullable=True)

class Manufacturer(Base):
    __tablename__ = "manufacturers"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    country_code = Column(CHAR(2), nullable=True)
    is_local = Column(Boolean, nullable=True)
    gmp_certified = Column(Boolean, nullable=True)

class Factory(Base):
    __tablename__ = "factories"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    manufacturer_id = Column(UUID(as_uuid=True), nullable=True)
    name = Column(String(255), nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    governorate = Column(String(100), nullable=True)
    gmp_status = Column(String(50), nullable=True)
    capacity_units_per_year = Column(Numeric, nullable=True)

class ImportRecord(Base):
    __tablename__ = "imports"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    medicine_id = Column(UUID(as_uuid=True), nullable=True)
    source_country_code = Column(CHAR(2), nullable=True)
    year = Column(String(4), nullable=True)
    volume_units = Column(Numeric, nullable=True)
    cost_usd = Column(Numeric, nullable=True)

class PliScore(Base):
    __tablename__ = "pli_scores"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    medicine_id = Column(UUID(as_uuid=True), nullable=False)
    score = Column(Numeric(5,2), nullable=False)
    factor_breakdown = Column(JSONB, nullable=True)
    computed_at = Column(DateTime(timezone=True), server_default=func.now())
    model_version = Column(String(50), nullable=True)

class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), nullable=False, unique=True)
    hashed_password = Column(String(255), nullable=True)
    oauth_provider = Column(String(50), nullable=True)
    role = Column(String(20), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class AuditLog(Base):
    __tablename__ = "audit_logs"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=True)
    action = Column(String(255), nullable=True)
    entity_type = Column(String(100), nullable=True)
    entity_id = Column(UUID(as_uuid=True), nullable=True)
    diff = Column(JSONB, nullable=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
