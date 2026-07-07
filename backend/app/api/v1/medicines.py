from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.repositories.medicine_repo import list_medicines, get_medicine
from app.services.pli import compute_pli
from app.schemas.medicine import MedicineRead

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/medicines", response_model=list[MedicineRead])
def medicines(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    meds = list_medicines(db, skip=skip, limit=limit)
    return meds


@router.get("/medicines/{medicine_id}/pli")
def medicine_pli(medicine_id: str, db: Session = Depends(get_db)):
    med = get_medicine(db, medicine_id)
    if not med:
        raise HTTPException(status_code=404, detail="Medicine not found")
    # Build a lightweight dict for compute_pli
    med_dict = {
        "who_essential": med.who_essential,
        "annual_import_estimate_usd": float(med.annual_import_estimate_usd) if med.annual_import_estimate_usd else 0,
        # placeholder fields for demonstration
        "manufacturing_complexity": "medium",
        "patent_status": "unknown",
    }
    result = compute_pli(med_dict, context={})
    return result
