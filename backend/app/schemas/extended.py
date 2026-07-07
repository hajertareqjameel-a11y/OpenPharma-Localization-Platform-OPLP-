from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class ActiveIngredientRead(BaseModel):
    id: UUID
    name: str
    manufacturing_complexity: Optional[str]
    patent_status: Optional[str]

    class Config:
        orm_mode = True

class FactoryRead(BaseModel):
    id: UUID
    name: str
    latitude: Optional[float]
    longitude: Optional[float]
    governorate: Optional[str]
    gmp_status: Optional[str]

    class Config:
        orm_mode = True

class ImportRead(BaseModel):
    id: UUID
    medicine_id: Optional[UUID]
    source_country_code: Optional[str]
    year: Optional[int]
    volume_units: Optional[float]
    cost_usd: Optional[float]

    class Config:
        orm_mode = True
