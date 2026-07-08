"""
Investment & cost-saving simulation utilities.
"""

from typing import Dict, Any
import math

def estimate_local_manufacturing_cost(import_cost_usd: float, assumed_local_cost_reduction_pct: float = 0.25) -> float:
    """
    Conservative estimate: local manufacturing cost = import_cost * (1 - reduction)
    """
    return import_cost_usd * (1 - float(assumed_local_cost_reduction_pct))

def simulate_investment(factory_size: str = "small", equipment_cost_usd: float = 500000, annual_production_units: float = 100000, unit_margin_usd: float = 0.1) -> Dict[str, Any]:
    """
    Returns estimated CAPEX/OPEX and simple payback assuming unit_margin_usd contribution.
    """
    size_map = {"small": 0.8, "medium": 1.0, "large": 1.5}
    multiplier = size_map.get(factory_size, 1.0)
    capex = equipment_cost_usd * multiplier
    annual_revenue = annual_production_units * unit_margin_usd * 365/365  # simplified
    if annual_revenue <= 0:
        payback_years = None
    else:
        payback_years = round(capex / annual_revenue, 1)
    return {
        "factory_size": factory_size,
        "capex": capex,
        "annual_revenue_est": annual_revenue,
        "payback_years": payback_years
    }
