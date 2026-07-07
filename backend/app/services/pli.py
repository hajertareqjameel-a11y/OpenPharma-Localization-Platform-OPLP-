import json
from typing import Dict, Any

WEIGHTS_FILE = "./backend/pli_weights_v1.json"


def load_weights() -> Dict[str, float]:
    with open(WEIGHTS_FILE, "r") as f:
        cfg = json.load(f)
    return cfg.get("weights", {})


def normalize(value, min_v, max_v):
    if value is None:
        return 0.0
    try:
        v = float(value)
    except Exception:
        return 0.0
    if max_v == min_v:
        return 0.0
    return max(0.0, min(1.0, (v - min_v) / (max_v - min_v)))


def compute_pli(medicine: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
    """Compute a deterministic PLI score from a medicine record.
    medicine: dict-like with keys used below (who_essential, annual_import_estimate_usd, manufacturing_complexity)
    context: optional dict for additional values (e.g., manufacturing_capability_score)
    Returns dict with score, factor_breakdown, model_version
    """
    weights = load_weights()
    # Example normalization baselines (these could be configurable elsewhere)
    # import dependency: normalize annual_import_estimate_usd against 0..1_000_000
    import_val = medicine.get("annual_import_estimate_usd") or 0
    import_norm = normalize(import_val, 0, 1_000_000)

    who_val = 1.0 if medicine.get("who_essential") else 0.0

    # manufacturing_complexity: expected 'low'/'medium'/'high'
    complexity = medicine.get("manufacturing_complexity", "medium")
    complexity_map = {"low": 1.0, "medium": 0.5, "high": 0.0}
    complexity_norm = complexity_map.get(complexity, 0.5)

    capability = (context or {}).get("manufacturing_capability_score", 0.0)

    # api_supplier_risk: 0..1 where higher means more risk => higher priority
    api_risk = (context or {}).get("api_supplier_risk", 0.0)

    patent_status = (medicine.get("patent_status") or "unknown")
    patent_map = {"expired": 1.0, "unknown": 0.5, "active": 0.0}
    patent_norm = patent_map.get(patent_status, 0.5)

    investment_cost_norm = 1.0 - ((context or {}).get("estimated_investment_cost_norm") or 0.5)

    demand_norm = import_norm

    factors = {
        "import_dependency": {"raw": import_val, "norm": import_norm, "weight": weights.get("import_dependency", 0.2)},
        "who_essential": {"raw": who_val, "norm": who_val, "weight": weights.get("who_essential", 0.15)},
        "manufacturing_complexity": {"raw": complexity, "norm": complexity_norm, "weight": weights.get("manufacturing_complexity", 0.15)},
        "local_manufacturing_capability": {"raw": capability, "norm": capability, "weight": weights.get("local_manufacturing_capability", 0.15)},
        "api_supplier_risk": {"raw": api_risk, "norm": api_risk, "weight": weights.get("api_supplier_risk", 0.10)},
        "patent_status": {"raw": patent_status, "norm": patent_norm, "weight": weights.get("patent_status", 0.10)},
        "estimated_investment_cost": {"raw": (context or {}).get("estimated_investment_cost"), "norm": investment_cost_norm, "weight": weights.get("estimated_investment_cost", 0.10)},
        "demand_proxy": {"raw": demand_norm, "norm": demand_norm, "weight": weights.get("demand_proxy", 0.05)},
    }

    score = 0.0
    for k, v in factors.items():
        score += v["norm"] * v["weight"]

    final_score = round(score * 100, 2)

    return {
        "score": final_score,
        "factor_breakdown": factors,
        "model_version": "pli_weights_v1",
    }
