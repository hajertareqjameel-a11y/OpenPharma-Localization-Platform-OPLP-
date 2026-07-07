import pytest
from app.services.pli import compute_pli


def test_compute_pli_basic():
    med = {
        "who_essential": True,
        "annual_import_estimate_usd": 50000,
        "manufacturing_complexity": "low",
        "patent_status": "expired",
    }
    res = compute_pli(med, context={"manufacturing_capability_score": 0.5, "api_supplier_risk": 0.2, "estimated_investment_cost": 100000, "estimated_investment_cost_norm": 0.3})
    assert "score" in res
    assert 0 <= res["score"] <= 100
