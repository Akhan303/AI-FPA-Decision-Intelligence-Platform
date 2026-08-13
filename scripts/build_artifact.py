"""Build the canonical dashboard artifact and reproducible synthetic source file."""
from __future__ import annotations
import csv, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from finance_engine import build_model

GENERATED_AT = "2026-08-13T20:00:00Z"

def write_csv(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

def source(source_id, label, path, definition):
    return {"id": source_id, "label": label, "path": path, "query": {"engine": "duckdb", "sql": f"SELECT * FROM read_csv_auto('{path}')", "description": definition, "executed_at": GENERATED_AT, "tables_used": [path], "filters": ["FY2026", "synthetic data", "USD millions"], "metric_definitions": [definition]}}

def build_artifact():
    m = build_model()
    write_csv(ROOT / "data" / "synthetic_finance_detail.csv", m["detail"])
    write_csv(ROOT / "data" / "synthetic_scenarios.csv", m["scenarios"])
    write_csv(ROOT / "data" / "synthetic_controls.csv", m["quality"])
    sources = [
        source("model", "Synthetic finance model", "data/synthetic_finance_detail.csv", "Revenue and EBITDA aggregate monthly at region grain; outlook combines six actual and six forecast months."),
        source("scenario", "Scenario model", "data/synthetic_scenarios.csv", "Scenarios apply transparent revenue, margin and working-capital assumptions to the base outlook."),
        source("controls", "Data and AI controls", "data/synthetic_controls.csv", "Control pass rate is passed checks divided by configured checks."),
    ]
    cards = [
        {"id": "revenue", "dataset": "kpis", "sourceId": "model", "description": "FY2026 outlook; six actual plus six forecast months.", "metrics": [{"label": "Revenue outlook", "field": "revenue", "format": "currency"}, {"label": "vs budget", "field": "revenue_vs_budget", "format": "percent", "signed": True}]},
        {"id": "margin", "dataset": "kpis", "sourceId": "model", "description": "EBITDA divided by full-year outlook revenue.", "metrics": [{"label": "EBITDA margin", "field": "ebitda_margin", "format": "percent"}, {"label": "EBITDA variance", "field": "ebitda_vs_budget", "format": "currency", "signed": True}]},
        {"id": "fcf", "dataset": "kpis", "sourceId": "model", "description": "EBITDA less capex, modeled tax and working-capital investment.", "metrics": [{"label": "Free cash flow", "field": "free_cash_flow", "format": "currency"}]},
        {"id": "nwc", "dataset": "kpis", "sourceId": "model", "description": "Revenue-weighted net working-capital days.", "metrics": [{"label": "NWC days", "field": "nwc_days", "format": "number"}]},
        {"id": "accuracy", "dataset": "kpis", "sourceId": "model", "description": "Illustrative one-minus-MAPE forecast accuracy.", "metrics": [{"label": "Forecast accuracy", "field": "forecast_accuracy", "format": "percent"}]},
        {"id": "controls", "dataset": "kpis", "sourceId": "controls", "description": "Share of configured deterministic controls passed.", "metrics": [{"label": "Control pass rate", "field": "control_pass_rate", "format": "percent"}]},
    ]
    charts = [
        {"id": "revenue_trend", "title": "Monthly revenue: actual, forecast and budget", "subtitle": "USD millions; actual through June, forecast from July", "type": "line", "dataset": "trend", "sourceId": "model", "encodings": {"x": {"field": "month", "type": "ordinal"}, "y": {"fields": ["actual_revenue", "forecast_revenue", "budget_revenue"], "type": "quantitative"}}, "xAxisTitle": "Month", "yAxisTitle": "Revenue (USD M)", "valueFormat": "currency", "layout": "full"},
        {"id": "region_variance", "title": "Revenue variance to budget by region", "subtitle": "USD millions; sorted from largest shortfall", "type": "bar", "dataset": "regions", "sourceId": "model", "encodings": {"x": {"field": "region", "type": "nominal"}, "y": {"field": "variance", "type": "quantitative"}}, "xAxisTitle": "Region", "yAxisTitle": "Variance (USD M)", "valueFormat": "currency", "layout": "half"},
        {"id": "ebitda_bridge", "title": "EBITDA outlook bridge", "subtitle": "USD millions; additive drivers from budget to outlook", "type": "waterfall", "intent": "decomposition", "dataset": "bridge", "sourceId": "model", "encodings": {"x": {"field": "driver", "type": "nominal"}, "y": {"field": "impact", "type": "quantitative"}}, "xAxisTitle": "Driver", "yAxisTitle": "EBITDA impact (USD M)", "valueFormat": "currency", "layout": "half"},
        {"id": "scenario_fcf", "title": "Free cash flow by scenario", "subtitle": "USD millions; transparent operating assumptions", "type": "bar", "dataset": "scenarios", "sourceId": "scenario", "encodings": {"x": {"field": "scenario", "type": "nominal"}, "y": {"field": "free_cash_flow", "type": "quantitative"}}, "xAxisTitle": "Scenario", "yAxisTitle": "Free cash flow (USD M)", "valueFormat": "currency", "layout": "half"},
        {"id": "cash_conversion", "title": "Working-capital days by region", "subtitle": "Revenue-weighted outlook; lower is better", "type": "bar", "dataset": "regions", "sourceId": "model", "encodings": {"x": {"field": "region", "type": "nominal"}, "y": {"field": "nwc_days", "type": "quantitative"}}, "xAxisTitle": "Region", "yAxisTitle": "NWC days", "valueFormat": "number", "layout": "half"},
    ]
    tables = [
        {"id": "scenario_table", "title": "Executive scenario decision table", "subtitle": "All values are synthetic and illustrative", "dataset": "scenarios", "sourceId": "scenario", "defaultSort": {"field": "revenue", "direction": "desc"}, "density": "dense", "layout": "full", "columns": [{"field": "scenario", "label": "Scenario"}, {"field": "revenue", "label": "Revenue", "format": "currency"}, {"field": "ebitda", "label": "EBITDA", "format": "currency"}, {"field": "ebitda_margin", "label": "Margin", "format": "percent"}, {"field": "free_cash_flow", "label": "FCF", "format": "currency"}, {"field": "nwc_days", "label": "NWC days", "format": "number"}, {"field": "management_posture", "label": "Management posture"}]},
        {"id": "actions_table", "title": "Prioritized risks and management actions", "subtitle": "Evidence-backed recommendations; human approval required", "dataset": "actions", "sourceId": "model", "defaultSort": {"field": "priority", "direction": "asc"}, "density": "dense", "layout": "full", "columns": [{"field": "priority", "label": "Priority", "format": "number"}, {"field": "signal", "label": "Signal"}, {"field": "evidence", "label": "Evidence"}, {"field": "recommended_action", "label": "Recommended action"}, {"field": "owner", "label": "Owner"}, {"field": "approval", "label": "Approval"}]},
        {"id": "controls_table", "title": "Data and AI control register", "subtitle": "Pre-publication checks for trustworthy finance narratives", "dataset": "quality", "sourceId": "controls", "defaultSort": {"field": "control", "direction": "asc"}, "density": "dense", "layout": "full", "columns": [{"field": "control", "label": "Control"}, {"field": "status", "label": "Status"}, {"field": "evidence", "label": "Evidence"}]},
    ]
    blocks = [
        {"id": "intro", "type": "markdown", "body": "# AI FP&A Decision Intelligence Platform\n\n**Illustrative synthetic company · FY2026 outlook · USD millions**\n\nA governed executive command center connecting rolling forecasts, variance intelligence, scenario decisions and AI-ready management narratives."},
        {"id": "kpi_strip", "type": "metric-strip", "cardIds": [c["id"] for c in cards]},
        {"id": "trend", "type": "chart", "chartId": "revenue_trend", "layout": "full"},
        {"id": "decision_context", "type": "markdown", "body": m["narrative"], "sourceId": "model"},
        {"id": "region", "type": "chart", "chartId": "region_variance", "layout": "half"},
        {"id": "bridge", "type": "chart", "chartId": "ebitda_bridge", "layout": "half"},
        {"id": "scenario_chart", "type": "chart", "chartId": "scenario_fcf", "layout": "half"},
        {"id": "cash", "type": "chart", "chartId": "cash_conversion", "layout": "half"},
        {"id": "scenario_decisions", "type": "table", "tableId": "scenario_table", "layout": "full"},
        {"id": "actions", "type": "table", "tableId": "actions_table", "layout": "full"},
        {"id": "governance", "type": "markdown", "body": "## Trust before automation\n\nThe narrative layer is grounded in reconciled model outputs. No employer data, customer data or private credentials are used. Recommendations remain drafts until a finance leader approves them. The design follows the NIST AI RMF principles of governing, mapping, measuring and managing AI risk."},
        {"id": "control_register", "type": "table", "tableId": "controls_table", "layout": "full"},
    ]
    return {"surface": "dashboard",
        "manifest": {"version": 1, "surface": "dashboard", "title": "AI FP&A Decision Intelligence Platform", "description": "A governed, synthetic executive FP&A portfolio case study.", "generatedAt": GENERATED_AT, "cards": cards, "charts": charts, "tables": tables, "sources": sources, "blocks": blocks},
        "snapshot": {"version": 1, "generatedAt": GENERATED_AT, "status": "fixture", "datasets": {"kpis": m["kpis"], "trend": m["trend"], "regions": m["regions"], "bridge": m["bridge"], "scenarios": m["scenarios"], "actions": m["actions"], "quality": m["quality"]}},
        "sources": sources}

if __name__ == "__main__":
    artifact = build_artifact()
    (ROOT / "artifact.json").write_text(json.dumps(artifact, indent=2), encoding="utf-8")
    print("Built artifact.json and synthetic source data")





