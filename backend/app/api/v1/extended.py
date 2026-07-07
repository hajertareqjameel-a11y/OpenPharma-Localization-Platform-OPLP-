from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.repositories.extended_repo import list_active_ingredients, list_factories, list_imports
from app.schemas.extended import ActiveIngredientRead, FactoryRead, ImportRead

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get('/active-ingredients', response_model=list[ActiveIngredientRead])
def active_ingredients(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return list_active_ingredients(db, skip=skip, limit=limit)

@router.get('/factories', response_model=list[FactoryRead])
def factories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return list_factories(db, skip=skip, limit=limit)

@router.get('/imports', response_model=list[ImportRead])
def imports(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return list_imports(db, skip=skip, limit=limit)
