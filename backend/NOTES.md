# Notes and decisions made during Stage 1 scaffolding

- Minimal FastAPI scaffold added under backend/app. This is intentionally small but functional: it includes a medicines router and a PLI compute endpoint.
- Database layer uses SQLAlchemy and reads DATABASE_URL from .env via pydantic settings. Alembic is listed in requirements but migration scripts are not yet added in this commit.
- Seed script programmatically creates 30 medicines marked with data_confidence="seed" — these are synthetic placeholder records for frontend development.
- PLI implementation is deterministic and driven by backend/pli_weights_v1.json; factors are normalized with simple heuristics. This will be extended in later commits.
- No secrets committed. .env.example present.

If you want, next I'll:
- Add Alembic environment and an initial migration file.
- Expand the API with auth stubs and additional entity endpoints (active-ingredients, factories, imports).
- Add GitHub Actions CI workflow for running pytest on PRs.

