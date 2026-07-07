from fastapi import FastAPI
from app.core.config import settings
from app.api.v1.medicines import router as medicines_router
from app.db.session import engine

# import models to ensure they are registered with SQLAlchemy metadata
from app import models

app = FastAPI(title="OpenPharma Localization Platform - API")

app.include_router(medicines_router, prefix="/api/v1", tags=["medicines"])


@app.on_event("startup")
def on_startup():
    # create tables in dev when using a simple migration-free workflow
    from app.models.base import Base
    Base.metadata.create_all(bind=engine)


@app.get("/health")
def health():
    return {"status": "ok"}
