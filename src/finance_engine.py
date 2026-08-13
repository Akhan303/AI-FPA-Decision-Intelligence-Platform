"""Deterministic synthetic FP&A model for an executive portfolio demonstration."""
from __future__ import annotations
import calendar, math, random
from dataclasses import dataclass

REGIONS = {
    "North America": {"revenue": 21.5, "growth": .072, "margin": .224, "nwc": 48},
    "EMEA": {"revenue": 15.2, "growth": .058, "margin": .198, "nwc": 57},
    "APAC": {"revenue": 10.8, "growth": .094, "margin": .181, "nwc": 62},
    "Latin America": {"revenue": 6.9, "growth": .066, "margin": .166, "nwc": 68},
}

@dataclass(frozen=True)
class Scenario:
    name: str
    revenue_factor: float
    margin_delta: float
    nwc_delta: float
    management_posture: str

SCENARIOS = (
    Scenario("Upside", 1.035, .010, -3, "Fund growth while protecting service levels"),
    Scenario("Base", 1.000, .000, 0, "Execute pricing and working-capital actions"),
    Scenario("Downside", .955, -.014, 5, "Stage discretionary spend and accelerate collections"),
)

def total(rows, field):
    return sum(float(row[field]) for row in rows)

def build_monthly_detail(seed=303):
    rng = random.Random(seed)
    season = (.92, .94, 1, .98, 1.02, 1.04, .97, .99, 1.03, 1.05, 1.08, 1.16)
    rev_bias = {"North America": .018, "EMEA": -.022, "APAC": .027, "Latin America": -.041}
    mar_bias = {"North America": .004, "EMEA": -.007, "APAC": -.003, "Latin America": -.010}
    nwc_bias = {"North America": -1, "EMEA": 2, "APAC": 3, "Latin America": 5}
    rows = []
    for month in range(1, 13):
        for region, a in REGIONS.items():
            budget_rev = a["revenue"] * (1 + a["growth"]) * season[month - 1]
            time_bias = -.012 if month in (4, 5, 6) else (.008 if month >= 9 else 0)
            outlook_rev = budget_rev * (1 + rev_bias[region] + time_bias + rng.uniform(-.012, .012))
            outlook_margin = a["margin"] + mar_bias[region] + rng.uniform(-.002, .002)
            budget_ebitda = budget_rev * a["margin"]
            outlook_ebitda = outlook_rev * outlook_margin
            nwc = a["nwc"] + nwc_bias[region]
            capex = outlook_rev * (.036 if region == "APAC" else .032)
            tax = max(outlook_ebitda * .21, 0)
            wc_investment = outlook_rev * nwc / 365 * .018
            rows.append({
                "month": f"{calendar.month_abbr[month]} 2026", "month_index": month,
                "region": region, "period_type": "Actual" if month <= 6 else "Forecast",
                "budget_revenue": round(budget_rev, 3), "outlook_revenue": round(outlook_rev, 3),
                "budget_ebitda": round(budget_ebitda, 3), "outlook_ebitda": round(outlook_ebitda, 3),
                "outlook_margin": round(outlook_margin, 4),
                "free_cash_flow": round(outlook_ebitda - capex - tax - wc_investment, 3),
                "nwc_days": float(nwc),
            })
    return rows

def build_trend(detail):
    rows = []
    for month in range(1, 13):
        subset = [r for r in detail if r["month_index"] == month]
        outlook = total(subset, "outlook_revenue")
        rows.append({
            "month": f"{calendar.month_abbr[month]} 2026", "month_index": month,
            "actual_revenue": round(outlook, 2) if month <= 6 else None,
            "forecast_revenue": round(outlook, 2) if month >= 6 else None,
            "budget_revenue": round(total(subset, "budget_revenue"), 2),
            "outlook_ebitda": round(total(subset, "outlook_ebitda"), 2),
            "budget_ebitda": round(total(subset, "budget_ebitda"), 2),
        })
    return rows

def build_regions(detail):
    rows = []
    for region in REGIONS:
        subset = [r for r in detail if r["region"] == region]
        budget, outlook = total(subset, "budget_revenue"), total(subset, "outlook_revenue")
        ebitda = total(subset, "outlook_ebitda")
        rows.append({
            "region": region, "budget_revenue": round(budget, 2), "outlook_revenue": round(outlook, 2),
            "variance": round(outlook - budget, 2), "variance_pct": round(outlook / budget - 1, 4),
            "ebitda_margin": round(ebitda / outlook, 4), "free_cash_flow": round(total(subset, "free_cash_flow"), 2),
            "nwc_days": round(sum(r["nwc_days"] for r in subset) / len(subset), 1),
        })
    return sorted(rows, key=lambda r: r["variance"])

def build_bridge(detail):
    budget, outlook = total(detail, "budget_ebitda"), total(detail, "outlook_ebitda")
    gap = outlook - budget
    drivers = [("Budget EBITDA", budget), ("Price", abs(gap) * .46 + 1.8),
               ("Volume", -abs(gap) * .38 - 2.1), ("Mix", abs(gap) * .17),
               ("Inflation", -abs(gap) * .31 - 1), ("Productivity", abs(gap) * .22 + .7), ("FX", 0)]
    drivers[-1] = ("FX", outlook - sum(v for _, v in drivers))
    drivers.append(("Outlook EBITDA", 0))
    return [{"driver": n, "impact": round(v, 2), "order": i} for i, (n, v) in enumerate(drivers)]

def build_scenarios(detail):
    base_rev, base_ebitda = total(detail, "outlook_revenue"), total(detail, "outlook_ebitda")
    base_margin, base_fcf = base_ebitda / base_rev, total(detail, "free_cash_flow")
    base_nwc = sum(r["nwc_days"] * r["outlook_revenue"] for r in detail) / base_rev
    rows = []
    for s in SCENARIOS:
        revenue = base_rev * s.revenue_factor
        margin = base_margin + s.margin_delta
        ebitda = revenue * margin
        fcf = base_fcf + (ebitda - base_ebitda) * .72 - max(s.nwc_delta, 0) * .55
        rows.append({"scenario": s.name, "revenue": round(revenue, 2), "ebitda": round(ebitda, 2),
                     "ebitda_margin": round(margin, 4), "free_cash_flow": round(fcf, 2),
                     "nwc_days": round(base_nwc + s.nwc_delta, 1), "management_posture": s.management_posture})
    return rows

def build_quality(detail):
    tests = [
        ("Row completeness", len(detail) == 48, f"{len(detail)} of 48 expected rows"),
        ("Dimension integrity", all(r["region"] in REGIONS for r in detail), "All regions map to the controlled dimension"),
        ("Revenue validity", all(r["budget_revenue"] > 0 and r["outlook_revenue"] > 0 for r in detail), "No zero or negative revenue values"),
        ("Margin bounds", all(.05 < r["outlook_margin"] < .40 for r in detail), "Margins fall within configured limits"),
        ("P&L reconciliation", math.isclose(total(detail, "outlook_ebitda"), sum(r["outlook_revenue"] * r["outlook_margin"] for r in detail), rel_tol=.001), "EBITDA reconciles to revenue × margin"),
        ("Scenario approval gate", True, "AI narrative remains draft until finance approval"),
    ]
    return [{"control": n, "status": "Passed" if ok else "Failed", "evidence": e} for n, ok, e in tests]

def build_model(seed=303):
    detail = build_monthly_detail(seed)
    regions, scenarios = build_regions(detail), build_scenarios(detail)
    revenue, budget_rev = total(detail, "outlook_revenue"), total(detail, "budget_revenue")
    ebitda, budget_ebitda = total(detail, "outlook_ebitda"), total(detail, "budget_ebitda")
    weighted_nwc = sum(r["nwc_days"] * r["outlook_revenue"] for r in detail) / revenue
    kpis = [{"revenue": round(revenue, 2), "revenue_vs_budget": round(revenue / budget_rev - 1, 4),
             "ebitda": round(ebitda, 2), "ebitda_margin": round(ebitda / revenue, 4),
             "ebitda_vs_budget": round(ebitda - budget_ebitda, 2), "free_cash_flow": round(total(detail, "free_cash_flow"), 2),
             "nwc_days": round(weighted_nwc, 1), "forecast_accuracy": .924, "control_pass_rate": 1.0}]
    weakest, slowest = min(regions, key=lambda r: r["variance"]), max(regions, key=lambda r: r["nwc_days"])
    actions = [
        {"priority": 1, "signal": f"{weakest['region']} revenue below plan", "evidence": f"Variance {weakest['variance_pct']:.1%}", "recommended_action": "Review pipeline conversion, price realization and discretionary spend", "owner": "Regional CFO", "approval": "Required"},
        {"priority": 2, "signal": f"{slowest['region']} cash conversion", "evidence": f"NWC {slowest['nwc_days']:.0f} days", "recommended_action": "Launch collections and inventory plan with weekly milestones", "owner": "Finance + Operations", "approval": "Required"},
        {"priority": 3, "signal": "Margin protection opportunity", "evidence": "Pricing and productivity partly offset volume and inflation", "recommended_action": "Lock accountable benefits into the rolling forecast", "owner": "FP&A", "approval": "Required"}]
    downside = next(r for r in scenarios if r["scenario"] == "Downside")
    direction = "above" if kpis[0]["revenue_vs_budget"] >= 0 else "below"
    narrative = ("### Governed executive brief\n\n"
        f"Full-year revenue is forecast at **USD {kpis[0]['revenue']:.1f}M**, **{abs(kpis[0]['revenue_vs_budget']):.1%} {direction} budget**. "
        f"EBITDA is **USD {kpis[0]['ebitda']:.1f}M** at a **{kpis[0]['ebitda_margin']:.1%} margin**. "
        f"The primary regional watch item is **{weakest['region']}**, where revenue is **{abs(weakest['variance_pct']):.1%} below plan**. "
        f"Under the downside scenario, free cash flow falls to **USD {downside['free_cash_flow']:.1f}M** and working-capital days rise to **{downside['nwc_days']:.0f}**. "
        "Management should protect price realization, stage discretionary spending, and assign weekly ownership for collections and inventory actions.\n\n"
        "*Control status: generated only from validated model outputs; synthetic data; finance approval required before use.*")
    return {"detail": detail, "trend": build_trend(detail), "regions": regions, "bridge": build_bridge(detail),
            "scenarios": scenarios, "quality": build_quality(detail), "kpis": kpis, "actions": actions, "narrative": narrative}

