# Architecture and control model

Synthetic operational drivers flow through a validated finance model into the rolling P&L and cash outlook, variance decomposition, and scenario engine. Those governed calculations feed a narrative layer, then a human approval gate, before appearing in the executive dashboard.

## Control principles

- Reconcile source grain before calculating KPIs.
- Keep metric definitions explicit and reusable.
- Separate calculations from narrative generation.
- Show scenario assumptions rather than hiding them.
- Require human approval for recommendations.
- Preserve an audit path from every visual to its source.

The portfolio version is deterministic and credential-free. An enterprise version would replace synthetic data with controlled ERP/EPM extracts, add role-based access, and allow an approved language model to draft commentary only from validated metrics and cited evidence.

