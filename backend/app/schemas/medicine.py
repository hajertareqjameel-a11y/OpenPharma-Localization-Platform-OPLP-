from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID

class MedicineBase(BaseModel):
    generic_name: str
    brand_name: Optional[str]
    atc_code: Optional[str]
    dosage_form: Optional[str]
    strength: Optional[str]
    who_essential: Optional[bool] = False
    annual_import_estimate_usd: Optional[float]

class MedicineCreate(MedicineBase):
    pass

class MedicineRead(MedicineBase):
    id: UUID
    country_code: Optional[str]
    local_production_status: Optional[str]
    data_confidence: Optional[str]

    class Config:
        orm_mode = True
