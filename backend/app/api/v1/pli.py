from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.repositories.medicine_repo import get_medicine
from app.services.pli import compute_pli
from app.models.extended_models import PliScore
from app.models.medicine import Medicine
from app.db.session import SessionLocal
import uuid

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get('/medicines/{medicine_id}/pli')
def get_pli(medicine_id: str, db: Session = Depends(get_db)):
    med = get_medicine(db, medicine_id)
    if not med:
        raise HTTPException(status_code=404, detail='Medicine not found')
    med_dict = {
        'who_essential': med.who_essential,
        'annual_import_estimate_usd': float(med.annual_import_estimate_usd) if med.annual_import_estimate_usd else 0,
        'manufacturing_complexity': 'medium',
        'patent_status': 'unknown',
    }
    result = compute_pli(med_dict, context={})
    return result

@router.post('/medicines/{medicine_id}/pli/recompute')
def recompute_pli(medicine_id: str, db: Session = Depends(get_db)):
    med = get_medicine(db, medicine_id)
    if not med:
        raise HTTPException(status_code=404, detail='Medicine not found')
    med_dict = {
        'who_essential': med.who_essential,
        'annual_import_estimate_usd': float(med.annual_import_estimate_usd) if med.annual_import_estimate_usd else 0,
        'manufacturing_complexity': 'medium',
        'patent_status': 'unknown',
    }
    result = compute_pli(med_dict, context={})
    # persist pli_scores
    pli = PliScore(
        id=uuid.uuid4(),
        medicine_id=med.id,
        score=result['score'],
        factor_breakdown=result['factor_breakdown'],
        model_version=result['model_version']
    )
    db.add(pli)
    db.commit()
    db.refresh(pli)
    return {'status': 'ok', 'pli_id': str(pli.id)}
