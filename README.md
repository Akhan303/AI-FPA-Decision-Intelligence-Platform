# AI FP&A Decision Intelligence Platform

A governed executive command center for rolling forecasts, variance intelligence, scenario decisions and AI-ready management narratives.

This flagship portfolio project demonstrates how a finance leader can combine FP&A, data analytics and responsible AI to improve management decisions. It is an end-to-end application, not a disconnected notebook, and runs entirely on deterministic synthetic data.

## Executive decisions supported

- Where is the full-year outlook moving relative to budget?
- Which price, volume, mix, inflation, productivity and FX drivers explain the EBITDA gap?
- Which region requires intervention, and who should own the response?
- How do upside and downside scenarios affect revenue, margin, cash flow and working capital?
- Can an AI-generated narrative be traced to validated finance outputs and approved by a human?

## What makes this different

The project combines four capabilities usually shown separately:

1. Driver-based planning — a transparent regional operating model.
2. Decision intelligence — KPI hierarchy, variance decomposition and prioritized actions.
3. Scenario management — base, upside and downside choices with explicit assumptions.
4. Responsible AI design — grounded narrative, controls, auditability and human approval.

## Dashboard contents

- Revenue, EBITDA margin, free cash flow, NWC days and forecast-accuracy scorecard
- Monthly actual, forecast and budget trend
- Regional revenue variance and working-capital comparison
- EBITDA driver waterfall
- Scenario comparison and management posture
- Evidence-backed risks, actions and accountable owners
- Data and AI control register

Open index.html to view the self-contained recruiter-facing dashboard. No server, login, API key or external connection is required.

## Quick start

Run:

    python scripts/build_artifact.py
    python -m unittest discover -s tests -v

The source model uses only the Python standard library. No third-party package is required for the test suite.

## Repository map

- artifact.json — canonical dashboard manifest and reviewed snapshot
- index.html — portable recruiter-facing dashboard
- data/synthetic_finance_detail.csv — reproducible source data
- docs/architecture.md — enterprise architecture and control model
- scripts/build_artifact.py — artifact builder
- src/finance_engine.py — finance and scenario engine
- tests/test_finance_engine.py — reconciliation and control tests

## Metric definitions

- Revenue outlook: six actual months plus six forecast months for FY2026.
- EBITDA margin: outlook EBITDA divided by outlook revenue.
- Free cash flow: EBITDA less capex, modeled tax and working-capital investment.
- NWC days: revenue-weighted net working-capital days.
- Forecast accuracy: illustrative one-minus-MAPE control metric.
- Control pass rate: passed deterministic controls divided by configured controls.

## Responsible-AI position

The portfolio build does not send data to an external language model. Its executive brief is deterministically assembled from validated calculations, making every figure reproducible. A production implementation could add an approved model behind the same evidence boundary while preserving source citations, prompt and output logging, access controls, unsupported-claim evaluations and human approval.

This control model is informed by the NIST AI Risk Management Framework and its generative-AI profile.

## Important disclosure

All company assumptions, transactions and outputs are synthetic and illustrative. This project does not represent results delivered for a current or former employer and should not be used for investment, accounting or operating decisions.

## Author

Aftab Khan — Finance, FP&A, Data & AI Transformation Executive

Portfolio: https://github.com/Akhan303


