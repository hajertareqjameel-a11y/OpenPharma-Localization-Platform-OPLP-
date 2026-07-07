from sqlalchemy.orm import Session
from app.models.extended_models import ActiveIngredient, Factory, ImportRecord
from app.schemas.extended import ActiveIngredientRead, FactoryRead, ImportRead


def list_active_ingredients(db: Session, skip: int = 0, limit: int = 100):
    return db.query(ActiveIngredient).offset(skip).limit(limit).all()


def list_factories(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Factory).offset(skip).limit(limit).all()


def list_imports(db: Session, skip: int = 0, limit: int = 100):
    return db.query(ImportRecord).offset(skip).limit(limit).all()
