from sqlalchemy.orm import Session
from app.models.medicine import Medicine
from app.schemas.medicine import MedicineCreate


def create_medicine(db: Session, m: MedicineCreate) -> Medicine:
    med = Medicine(**m.dict())
    db.add(med)
    db.commit()
    db.refresh(med)
    return med


def get_medicine(db: Session, medicine_id: str) -> Medicine | None:
    return db.query(Medicine).filter(Medicine.id == medicine_id).first()


def list_medicines(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Medicine).offset(skip).limit(limit).all()
