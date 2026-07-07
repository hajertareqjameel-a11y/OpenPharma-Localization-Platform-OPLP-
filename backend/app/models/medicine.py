import uuid
from sqlalchemy import Column, String, Boolean, Numeric, Enum, CHAR
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy import DateTime
from app.models.base import Base


class Medicine(Base):
    __tablename__ = "medicines"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    generic_name = Column(String(255), nullable=False, index=True)
    brand_name = Column(String(255), nullable=True)
    atc_code = Column(String(50), nullable=True, index=True)
    dosage_form = Column(String(100), nullable=True)
    strength = Column(String(100), nullable=True)
    who_essential = Column(Boolean, default=False)
    country_code = Column(CHAR(2), default="IQ")
    local_production_status = Column(String(50), default="none")
    annual_import_estimate_usd = Column(Numeric, nullable=True)
    data_confidence = Column(String(50), default="seed")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
