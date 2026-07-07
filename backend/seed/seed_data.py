from app.db.session import engine, SessionLocal
from app.models.base import Base
from app.models.medicine import Medicine


def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        existing = db.query(Medicine).count()
        if existing > 0:
            print("Seed: medicines already present, skipping")
            return
        meds = []
        for i in range(1, 31):
            meds.append(Medicine(
                generic_name=f"Medicine {i}",
                brand_name=f"Brand {i}",
                atc_code=f"A{i:03d}",
                dosage_form="tablet",
                strength="100mg",
                who_essential=(i % 3 == 0),
                annual_import_estimate_usd=10000 * i,
                data_confidence="seed"
            ))
        db.add_all(meds)
        db.commit()
        print("Seeded 30 medicines (data_confidence=seed)")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
