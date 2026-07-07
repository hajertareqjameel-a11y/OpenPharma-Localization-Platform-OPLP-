from app.db.session import engine, SessionLocal
from app.models.base import Base
from app.models.extended_models import ActiveIngredient, Manufacturer, Factory, ImportRecord, PliScore, User, AuditLog


def seed_extended():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        # For now, keep it minimal: if active_ingredients empty, seed a few
        if db.query(ActiveIngredient).count() == 0:
            ai = ActiveIngredient(name="Paracetamol", manufacturing_complexity="low", patent_status="expired")
            db.add(ai)
        db.commit()
    finally:
        db.close()


if __name__ == '__main__':
    seed_extended()
